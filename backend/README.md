# Physical AI & Humanoid Robotics - Backend

This backend serves as the foundation for the Physical AI & Humanoid Robotics textbook project, providing a RAG (Retrieval-Augmented Generation) chatbot API that allows users to query the textbook content using natural language.

## Overview

The backend implements a RAG system that:
- Crawls and indexes content from the Docusaurus-based textbook
- Stores embeddings in a Qdrant vector database
- Provides a FastAPI-based API for querying the indexed content
- Uses Cohere for embedding generation and OpenRouter for LLM responses

## Architecture

The system consists of several key components:

- **main.py**: Docusaurus Embedding Pipeline that crawls the textbook site, extracts content, chunks it, and stores embeddings in Qdrant
- **agent.py**: RAG Agent that handles query processing using OpenRouter's free model with integrated reporting
- **retrieving.py**: RAG Retriever that queries the vector database for relevant content
- **api.py**: FastAPI application that exposes the RAG functionality through REST endpoints
- **reports.py**: Comprehensive reporting system for tracking usage, performance, and quality metrics
- **generate_reports.py**: CLI tool for generating various reports

## Features

- **Content Indexing**: Automatically crawls and indexes content from the deployed Docusaurus textbook
- **Vector Search**: Uses Cohere embeddings and Qdrant vector database for semantic search
- **API Endpoints**: Provides both legacy and v1 API endpoints for chat and content retrieval
- **Health Checks**: Built-in health check endpoints for monitoring
- **Docker Support**: Containerized deployment with Docker
- **Comprehensive Reporting**: Detailed analytics on query performance, user feedback, and system metrics
- **Session Tracking**: Tracks user sessions for better analytics and personalization

## API Endpoints

### v1 Endpoints
- `GET /api/v1/health` - Health check
- `POST /api/v1/chat` - Chat with the RAG system
- `POST /api/v1/process-url` - Process and index a URL (TODO)
- `POST /api/v1/retrieve` - Retrieve context based on query

### Legacy Endpoints
- `POST /ask` - Query the RAG system
- `GET /health` - Health check

## Requirements

- Python 3.8+
- Qdrant vector database (local or remote)
- Cohere API key for embeddings
- OpenRouter API key for LLM responses

## Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (see `.env` file)

## Environment Variables

Create a `.env` file with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
SOURCE_URL=your_docusaurus_site_url
```

## Reporting System

The backend includes a comprehensive reporting system that tracks:

### Query Logging
- All queries with their responses, sources, and metadata
- Query execution time and confidence scores
- Retrieved chunks and context length
- User feedback when provided

### Metrics Tracking
- Total queries processed
- Average response time
- Average confidence scores
- Average context length and retrieved chunks
- User feedback distribution

### Report Types
- **Daily Reports**: Summary of daily usage and performance
- **Feedback Reports**: Analysis of user feedback and common issues
- **Metrics Reports**: Comprehensive system performance metrics

### Generating Reports
Run the report generator script:
```bash
python generate_reports.py --type daily --date 2025-12-22
python generate_reports.py --type feedback
python generate_reports.py --type metrics
```

To export reports to files:
```bash
python generate_reports.py --type daily --output daily_report_2025-12-22.json
```

## Running the Application

### Direct execution
```bash
# Start the API server
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Or run the main pipeline to index content
python main.py
```

### Using Docker
```bash
# Build the image
docker build -t rag-chatbot .

# Run the container
docker run -p 8000:8000 rag-chatbot
```

## Usage

1. First, run the main pipeline to index your textbook content:
   ```bash
   python main.py
   ```

2. Start the API server:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

3. Query the API:
   ```bash
   curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is ROS2?"}'
   ```

## Project Structure

```
backend/
├── main.py              # Docusaurus embedding pipeline
├── agent.py             # RAG agent for query processing with reporting
├── retrieving.py        # RAG retriever for vector database queries
├── api.py               # FastAPI application
├── reports.py           # Reporting system for analytics
├── generate_reports.py  # CLI tool for generating reports
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── .env                 # Environment variables
├── reports/             # Generated reports directory
└── tests/               # Test files
```

## Dependencies

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `cohere`: Embedding generation
- `qdrant-client`: Vector database client
- `fastapi`: Web framework
- `python-dotenv`: Environment variable management

## Testing

Run the test suite:
```bash
pytest tests/
```

## Deployment

The backend can be deployed:
1. As a Docker container
2. On a cloud platform supporting Python applications
3. Directly on a server with Python installed

## Deployed Instance

The backend is deployed and accessible at: https://samra82-book-chatbot.hf.space/

API documentation is available at: https://samra82-book-chatbot.hf.space/docs

You can test the API endpoints directly at the deployed URL:
- Health check: https://samra82-book-chatbot.hf.space/api/v1/health
- Chat endpoint: https://samra82-book-chatbot.hf.space/api/v1/chat
- Legacy ask endpoint: https://samra82-book-chatbot.hf.space/ask

## Troubleshooting

- If you encounter issues with API keys, verify your `.env` file is properly configured
- For Qdrant connection issues, ensure the Qdrant service is running and accessible
- For embedding issues, verify your Cohere API key has sufficient quota

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

See the main project repository for licensing information.