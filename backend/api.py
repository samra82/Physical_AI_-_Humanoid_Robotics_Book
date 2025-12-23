import os
import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import logging
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the existing RAG agent functionality
from agent import RAGAgent
from retrieving import RAGRetriever

# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot for Physical AI - Humanoid Robotics Book",
    description="API for RAG Chatbot with document retrieval and question answering",
    version="1.0.0"
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for the API v1 endpoints
class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    session_id: Optional[str] = None

class Source(BaseModel):
    """Model for source information in chat response"""
    id: str
    content: str
    source_url: Optional[str] = None
    section_title: Optional[str] = None

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    session_id: str
    sources: List[Source] = []
    confidence_score: Optional[float] = None

class ProcessUrlRequest(BaseModel):
    """Request model for process URL endpoint"""
    url: str

class ProcessUrlResponse(BaseModel):
    """Response model for process URL endpoint"""
    status: str
    message: str
    chunks_processed: Optional[int] = None

class RetrieveRequest(BaseModel):
    """Request model for retrieve context endpoint"""
    query: str
    top_k: Optional[int] = 5

class RetrievedChunk(BaseModel):
    """Model for retrieved chunks in retrieve response"""
    id: str
    content: str
    similarity_score: float
    metadata: Dict[str, Any]

class RetrieveResponse(BaseModel):
    """Response model for retrieve context endpoint"""
    retrieved_chunks: List[RetrievedChunk]

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    service: str

# Pydantic models for the original /ask endpoint
class QueryRequest(BaseModel):
    query: str

class MatchedChunk(BaseModel):
    content: str
    url: str
    position: int
    similarity_score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    matched_chunks: List[MatchedChunk]
    error: Optional[str] = None
    status: str  # "success", "error", "empty"
    query_time_ms: Optional[float] = None
    confidence: Optional[str] = None

# Global RAG agent instance
rag_agent = None
rag_retriever = None

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG agent and retriever on startup"""
    global rag_agent, rag_retriever
    logger.info("Initializing RAG Agent and Retriever...")
    try:
        rag_agent = RAGAgent()
        rag_retriever = RAGRetriever()
        logger.info("RAG Agent and Retriever initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG Agent and Retriever: {e}")
        raise

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    from datetime import datetime
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        service="RAG Chatbot API"
    )

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Send a user query and receive an AI-generated response with source references
    """
    logger.info(f"Processing chat request: {request.message[:50]}...")

    try:
        # Validate input
        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        if len(request.message) > 2000:
            raise HTTPException(status_code=400, detail="Message too long, maximum 2000 characters")

        # Process query through RAG agent
        response = rag_agent.query_agent(request.message, request.session_id)

        # Generate a session ID if not provided
        session_id = request.session_id or f"session_{int(time.time())}"

        # Format sources
        sources = []
        if response.get("matched_chunks"):
            for chunk in response.get("matched_chunks", []):
                # Create a unique ID for the source
                chunk_content_preview = chunk.get("content", "")[:30] if chunk.get("content") else "unknown"
                chunk_url = chunk.get("url", "unknown")
                # Create a simple unique ID using content preview and URL
                import uuid
                source_id = str(uuid.uuid4())[:8]  # Use UUID for unique ID

                sources.append(Source(
                    id=source_id,
                    content=chunk.get("content", ""),
                    source_url=chunk.get("url", ""),
                    section_title="Retrieved Content"
                ))

        # Calculate confidence score based on similarity scores
        confidence_score = None
        if response.get("matched_chunks"):
            avg_score = sum(
                chunk.get("similarity_score", 0.0)
                for chunk in response.get("matched_chunks", [])
            ) / len(response.get("matched_chunks", []))
            confidence_score = avg_score

        # Format response
        formatted_response = ChatResponse(
            response=response.get("answer", "I couldn't find a good answer to your question."),
            session_id=session_id,
            sources=sources,
            confidence_score=confidence_score
        )

        logger.info(f"Chat request processed successfully")
        return formatted_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.post("/api/v1/process-url", response_model=ProcessUrlResponse)
async def process_url_endpoint(request: ProcessUrlRequest):
    """
    Extract content from a URL, generate embeddings, and store in vector database
    """
    logger.info(f"Processing URL: {request.url}")

    try:
        # Validate input
        if not request.url or len(request.url.strip()) == 0:
            raise HTTPException(status_code=400, detail="URL cannot be empty")

        # TODO: Implement URL processing logic here
        # This would involve:
        # 1. Extracting content from the URL
        # 2. Generating embeddings
        # 3. Storing in vector database

        # For now, return a mock response
        return ProcessUrlResponse(
            status="success",
            message=f"URL {request.url} processed successfully",
            chunks_processed=0  # TODO: Return actual number of chunks processed
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing URL: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")

@app.post("/api/v1/retrieve", response_model=RetrieveResponse)
async def retrieve_context_endpoint(request: RetrieveRequest):
    """
    Retrieve relevant context from the vector database based on a query
    """
    logger.info(f"Retrieving context for query: {request.query[:50]}...")

    try:
        # Validate input
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Use the RAG retriever to get relevant chunks
        json_response = rag_retriever.retrieve(
            query_text=request.query,
            top_k=request.top_k or 5
        )

        response_dict = json.loads(json_response)

        # Format retrieved chunks
        retrieved_chunks = []
        for result in response_dict.get("results", []):
            retrieved_chunks.append(RetrievedChunk(
                id=result.get("chunk_id", ""),
                content=result.get("content", ""),
                similarity_score=result.get("similarity_score", 0.0),
                metadata={
                    "url": result.get("url", ""),
                    "position": result.get("position", 0),
                    "created_at": result.get("created_at", "")
                }
            ))

        return RetrieveResponse(retrieved_chunks=retrieved_chunks)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving context: {str(e)}")

@app.post("/ask", response_model=QueryResponse)
async def ask_rag(request: QueryRequest):
    """
    Process a user query through the RAG agent and return the response
    """
    logger.info(f"Processing query: {request.query[:50]}...")

    try:
        # Validate input
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.query) > 2000:
            raise HTTPException(status_code=400, detail="Query too long, maximum 2000 characters")

        # Process query through RAG agent
        response = rag_agent.query_agent(request.query)

        # Format response
        formatted_response = QueryResponse(
            answer=response.get("answer", ""),
            sources=response.get("sources", []),
            matched_chunks=[
                MatchedChunk(
                    content=chunk.get("content", ""),
                    url=chunk.get("url", ""),
                    position=chunk.get("position", 0),
                    similarity_score=chunk.get("similarity_score", 0.0)
                )
                for chunk in response.get("matched_chunks", [])
            ],
            error=response.get("error"),
            status="error" if response.get("error") else "success",
            query_time_ms=response.get("query_time_ms"),
            confidence=response.get("confidence")
        )

        logger.info(f"Query processed successfully in {response.get('query_time_ms', 0):.2f}ms")
        return formatted_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return QueryResponse(
            answer="",
            sources=[],
            matched_chunks=[],
            error=str(e),
            status="error"
        )

@app.get("/health", response_model=HealthResponse)
async def legacy_health_check():
    """
    Legacy health check endpoint
    """
    from datetime import datetime
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        service="RAG Chatbot API"
    )

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)