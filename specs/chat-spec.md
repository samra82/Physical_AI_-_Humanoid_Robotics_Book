# RAG Chatbot API Specification

## Overview
This document describes the API endpoints for the RAG (Retrieval Augmented Generation) Chatbot system that integrates humanoid robotics knowledge with AI-powered responses.

## Base URL
- Development: `http://localhost:8001/api/v1`
- Production: To be determined

## Authentication
No authentication required for development. In production, API keys may be required via Authorization header.

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the service is running and healthy.

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2025-12-22T19:58:30.210811",
  "service": "RAG Chatbot API"
}
```

### 2. Chat
**POST** `/chat`

Send a user message and receive an AI-generated response with source references.

#### Request Body
```json
{
  "message": "string (required) - The user's message/question",
  "session_id": "string (optional) - Session identifier for conversation continuity"
}
```

#### Response
```json
{
  "response": "string - The AI-generated response",
  "session_id": "string - Session identifier (newly created if not provided)",
  "sources": [
    {
      "id": "string - Unique identifier for the source",
      "content": "string - The content of the source",
      "source_url": "string - URL where the content was retrieved from",
      "section_title": "string - Title of the section"
    }
  ],
  "confidence_score": "number (optional) - Confidence score between 0 and 1"
}
```

#### Example Request
```bash
curl -X POST http://localhost:8001/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is humanoid robotics?"}'
```

### 3. Retrieve Context
**POST** `/retrieve`

Retrieve relevant context from the vector database based on a query.

#### Request Body
```json
{
  "query": "string (required) - The search query",
  "top_k": "number (optional, default: 5) - Number of results to return"
}
```

#### Response
```json
{
  "retrieved_chunks": [
    {
      "id": "string - Unique identifier for the chunk",
      "content": "string - The retrieved content",
      "similarity_score": "number - Similarity score between 0 and 1",
      "metadata": {
        "url": "string - Source URL",
        "position": "number - Position in the original document",
        "created_at": "string - Timestamp when stored"
      }
    }
  ]
}
```

#### Example Request
```bash
curl -X POST http://localhost:8001/api/v1/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "humanoid robotics", "top_k": 3}'
```

### 4. Process URL (Planned)
**POST** `/process-url`

Extract content from a URL, generate embeddings, and store in vector database.
*(Currently returns mock response - implementation pending)*

#### Request Body
```json
{
  "url": "string (required) - The URL to process"
}
```

#### Response
```json
{
  "status": "string - Status of the operation (success/error)",
  "message": "string - Descriptive message",
  "chunks_processed": "number (optional) - Number of content chunks processed"
}
```

## Error Handling

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid input)
- `422`: Validation Error
- `500`: Internal Server Error

### Error Response Format
```json
{
  "detail": "Error message describing the issue"
}
```

## Frontend Integration

### API Service Configuration
The frontend API service is located at `my-book/src/services/api.js` and includes:

- Base URL configuration with fallback to `http://localhost:8001/api/v1`
- Error handling and retry logic
- Session management
- CORS support for development

### Chat Interface Integration
The chat interface in `my-book/src/components/ChatInterface.js` handles:

- Message history management
- Loading states
- Error display
- Source citations
- Confidence scoring display
- Session continuity

## Technology Stack

### Backend
- FastAPI for the web framework
- OpenRouter API for LLM integration (using nvidia/nemotron-3-nano-30b-a3b:free model)
- Qdrant for vector storage
- Cohere for embeddings
- Python 3.13+

### Frontend
- Docusaurus for the documentation site
- React for the chat interface
- JavaScript ES6+ for API communication

## Environment Variables Required

### Backend (.env file)
```
OPENROUTER_API_KEY=your_openrouter_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
SOURCE_URL=the_base_url_to_scrape_content_from
```

## Deployment

### Development
1. Start backend: `cd backend && python -m uvicorn api:app --host 0.0.0.0 --port 8001`
2. Start frontend: `cd my-book && npm run start`
3. Access frontend at: `http://localhost:3000`

### Production
TBD - Configuration will depend on deployment platform and environment.