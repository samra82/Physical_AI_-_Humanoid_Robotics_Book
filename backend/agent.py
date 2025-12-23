import os
import json
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv
import asyncio
import time
import requests
from reports import RAGReportGenerator, QueryReport

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGAgent:
    def __init__(self):
        # Use OpenRouter API with free model
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        # Import the RAG retriever for context retrieval
        from retrieving import RAGRetriever
        self.retriever = RAGRetriever()

        # Initialize reporting
        self.reporter = RAGReportGenerator()

        logger.info("RAG Agent initialized with OpenRouter and RAG Retriever")

    def query_agent(self, query_text: str, session_id: str = None) -> Dict:
        """
        Process a query through the RAG agent and return structured response
        """
        start_time = time.time()

        logger.info(f"Processing query through RAG agent: '{query_text[:50]}...'")

        try:
            # Retrieve relevant context from the knowledge base
            json_response = self.retriever.retrieve(query_text=query_text, top_k=5, threshold=0.3)
            results = json.loads(json_response)

            # Extract matched chunks from results
            matched_chunks = []
            for result in results.get('results', []):
                matched_chunks.append({
                    'content': result.get('content', ''),
                    'url': result.get('url', ''),
                    'position': result.get('position', 0),
                    'similarity_score': result.get('similarity_score', 0.0)
                })

            # Generate a response using OpenRouter, incorporating the retrieved context
            context_text = "\n".join([chunk['content'] for chunk in matched_chunks[:5]])  # Use top 5 chunks for more comprehensive context

            if context_text.strip():
                # Create a prompt that includes the context
                messages = [
                    {
                        "role": "system",
                        "content": "You are a comprehensive and helpful assistant for humanoid robotics and AI. Use the provided context to answer questions thoroughly and accurately. Always cite your sources when possible. Provide detailed explanations based on the context."
                    },
                    {
                        "role": "user",
                        "content": f"Context: {context_text}\n\nQuestion: {query_text}\n\nPlease provide a comprehensive, detailed answer based on the context provided, citing sources where appropriate. Include relevant examples, explanations, and details from the context."
                    }
                ]
            else:
                # If no context found, just answer the question
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant for humanoid robotics and AI."
                    },
                    {
                        "role": "user",
                        "content": f"Question: {query_text}\n\nPlease provide a helpful answer."
                    }
                ]

            # Call OpenRouter API with the free model
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "nvidia/nemotron-3-nano-30b-a3b:free",  # Using the free model you specified
                "messages": messages,
                "max_tokens": 2000,  # Increased token limit for longer, more comprehensive responses
                "temperature": 0.7,
                "top_p": 0.9,
                "presence_penalty": 0.1,
                "frequency_penalty": 0.1
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                response_data = response.json()
                answer = response_data['choices'][0]['message']['content'].strip()
            else:
                logger.warning(f"OpenRouter API failed: {response.status_code} - {response.text}")
                answer = f"I received your question: '{query_text}'. Based on the available information, I can tell you that this is related to humanoid robotics. For more specific details, please check the relevant documentation or resources."

            # Calculate confidence based on similarity scores
            confidence = self._calculate_confidence(matched_chunks)

            # Calculate query time
            query_time_ms = (time.time() - start_time) * 1000

            # Format the response
            response = {
                "answer": answer,
                "sources": list(set([chunk['url'] for chunk in matched_chunks if chunk['url']])),  # Unique sources
                "matched_chunks": matched_chunks,
                "query_time_ms": query_time_ms,
                "confidence": confidence
            }

            # Generate and log report
            similarity_scores = [chunk['similarity_score'] for chunk in matched_chunks]
            query_report = QueryReport(
                query_id=f"query_{int(time.time())}_{hash(query_text) % 10000}",
                query_text=query_text,
                response=answer,
                sources=response['sources'],
                confidence_score=self._calculate_average_confidence(matched_chunks),
                query_time_ms=query_time_ms,
                timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
                similarity_scores=similarity_scores,
                retrieved_chunks_count=len(matched_chunks),
                context_length=len(context_text),
                session_id=session_id
            )

            self.reporter.log_query(query_report)
            self.reporter.update_metrics(query_report)

            logger.info(f"Query processed in {query_time_ms:.2f}ms")
            return response

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": "Sorry, I encountered an error processing your request.",
                "sources": [],
                "matched_chunks": [],
                "error": str(e),
                "query_time_ms": (time.time() - start_time) * 1000
            }

    def _calculate_average_confidence(self, matched_chunks: List[Dict]) -> float:
        """
        Calculate average confidence based on similarity scores
        """
        if not matched_chunks:
            return 0.0

        avg_score = sum(chunk.get('similarity_score', 0.0) for chunk in matched_chunks) / len(matched_chunks)
        return avg_score

    def _calculate_confidence(self, matched_chunks: List[Dict]) -> str:
        """
        Calculate confidence level based on similarity scores and number of matches
        """
        if not matched_chunks:
            return "low"

        avg_score = sum(chunk.get('similarity_score', 0.0) for chunk in matched_chunks) / len(matched_chunks)

        if avg_score >= 0.7:
            return "high"
        elif avg_score >= 0.4:
            return "medium"
        else:
            return "low"


def query_agent(query_text: str) -> Dict:
    """
    Convenience function to query the RAG agent
    """
    agent = RAGAgent()
    return agent.query_agent(query_text)


def run_agent_sync(query_text: str) -> Dict:
    """
    Synchronous function to run the agent for direct usage
    """
    agent = RAGAgent()
    return agent.query_agent(query_text)


def main():
    """
    Main function to demonstrate the RAG agent functionality
    """
    logger.info("Initializing RAG Agent...")

    try:
        # Initialize the agent
        agent = RAGAgent()

        # Example queries to test the system
        test_queries = [
            "What is ROS2?",
            "Explain humanoid design principles",
            "How does VLA work?",
            "What are simulation techniques?",
            "Explain AI control systems"
        ]

        print("RAG Agent - Testing Queries")
        print("=" * 50)

        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}: {query}")
            print("-" * 30)

            # Process query through agent
            response = agent.query_agent(query)

            # Print formatted results
            print(f"Answer: {response['answer']}")

            if response.get('sources'):
                print(f"Sources: {len(response['sources'])} documents")
                for source in response['sources'][:3]:  # Show first 3 sources
                    print(f"  - {source}")

            if response.get('matched_chunks'):
                print(f"Matched chunks: {len(response['matched_chunks'])}")
                for j, chunk in enumerate(response['matched_chunks'][:2], 1):  # Show first 2 chunks
                    content_preview = chunk['content'][:100] + "..." if len(chunk['content']) > 100 else chunk['content']
                    print(f"  Chunk {j}: {content_preview}")
                    print(f"    Source: {chunk['url']}")
                    print(f"    Score: {chunk['similarity_score']:.3f}")

            print(f"Query time: {response['query_time_ms']:.2f}ms")
            print(f"Confidence: {response.get('confidence', 'unknown')}")

            if i < len(test_queries):  # Don't sleep after the last query
                time.sleep(1)  # Small delay between queries
    except Exception as e:
        print(f"Error initializing agent: {e}")


if __name__ == "__main__":
    main()