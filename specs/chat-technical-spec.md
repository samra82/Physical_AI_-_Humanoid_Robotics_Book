# RAG Chatbot Technical Specification

## System Overview
The RAG (Retrieval Augmented Generation) Chatbot for Physical AI & Humanoid Robotics is a conversational AI system that combines vector database retrieval with large language model generation to provide accurate, source-cited responses about humanoid robotics topics.

## Architecture

### High-Level Architecture
```
[Frontend Chat UI]
       ↓ (messages)
[API Gateway/Docusaurus]
       ↓ (HTTP requests)
[FastAPI Backend]
       ↓ (queries & responses)
[Vector Database (Qdrant)] ↔ [LLM (OpenRouter)]
```

### Component Architecture

#### 1. Frontend Layer
- **Framework**: Docusaurus
- **UI Components**:
  - ChatInterface.js: Main chat component with message history
  - FloatingChat/: Collapsible chat widget
- **API Service**: api.js: Handles all backend communication
- **Styling**: CSS modules for component-specific styling

#### 2. API Layer
- **Framework**: FastAPI
- **Endpoints**: RESTful API under `/api/v1/` path
- **Middleware**: CORS support for development
- **Models**: Pydantic models for request/response validation

#### 3. Business Logic Layer
- **RAGAgent**: Orchestrates retrieval and generation
- **RAGRetriever**: Handles vector database queries
- **External APIs**: OpenRouter for LLM, Qdrant for vectors, Cohere for embeddings

#### 4. Data Layer
- **Vector Database**: Qdrant Cloud
- **Embedding Model**: Cohere embed-multilingual-v3.0
- **Storage**: Document chunks with metadata (URL, position, timestamp)

## Data Flow

### Query Flow
1. User submits question via frontend
2. Frontend calls `/api/v1/chat` endpoint
3. Backend retrieves relevant chunks from Qdrant using Cohere embeddings
4. Backend constructs context-aware prompt with retrieved content
5. Backend calls OpenRouter API with context and question
6. Backend returns AI response with source citations
7. Frontend displays response with sources and confidence score

### Indexing Flow (Planned)
1. System scrapes content from SOURCE_URL
2. Content is chunked into manageable pieces
3. Each chunk is embedded using Cohere
4. Embeddings and metadata are stored in Qdrant
5. Chunks are indexed for fast retrieval

## API Endpoints Detailed

### Chat Endpoint (`/api/v1/chat`)
- **Method**: POST
- **Purpose**: Process user queries and return AI responses
- **Input**: User message and optional session ID
- **Output**: AI response with sources and confidence
- **Processing**:
  - Retrieve relevant context from vector database
  - Construct prompt with context
  - Generate response using OpenRouter
  - Format response with sources
  - Calculate confidence score

### Retrieve Endpoint (`/api/v1/retrieve`)
- **Method**: POST
- **Purpose**: Direct retrieval of relevant documents
- **Input**: Query text and number of results (top_k)
- **Output**: Ranked list of document chunks
- **Processing**:
  - Generate embedding for query
  - Perform vector similarity search
  - Return top-k most similar chunks

### Health Endpoint (`/api/v1/health`)
- **Method**: GET
- **Purpose**: System health monitoring
- **Output**: Service status and timestamp

## Security Considerations

### API Keys
- OpenRouter API key stored in environment variables
- Not exposed to frontend
- Server-side only access

### Input Validation
- Message length limits (2000 characters)
- Content type validation (JSON)
- Sanitization of user inputs

### Rate Limiting
- Not implemented (to be added in production)
- Could use middleware like slowapi

## Performance Considerations

### Response Time Optimization
- Vector database indexing for fast retrieval
- Caching of frequent queries (planned)
- Asynchronous processing where possible

### Scalability
- Stateless API design
- Horizontal scaling possible
- Database connection pooling

## Error Handling

### Backend Error Handling
- HTTP status codes for different error types
- Detailed error messages in responses
- Logging for debugging
- Graceful degradation when LLM unavailable

### Frontend Error Handling
- Network error detection
- User-friendly error messages
- Retry mechanisms
- Offline state handling

## Configuration

### Environment Variables
```
OPENROUTER_API_KEY: API key for OpenRouter service
COHERE_API_KEY: API key for Cohere embedding service
QDRANT_URL: URL for Qdrant vector database
QDRANT_API_KEY: API key for Qdrant database
SOURCE_URL: Base URL to scrape and index content from
```

### Runtime Configuration
- Port configuration (default 8001 for backend)
- Vector database collection names
- Retrieval parameters (top_k, threshold)
- LLM parameters (temperature, max_tokens)

## Dependencies

### Backend Dependencies
- FastAPI: Web framework
- uvicorn: ASGI server
- openai-agents: Agent framework (modified to use OpenRouter)
- cohere: Embedding service
- qdrant-client: Vector database client
- python-dotenv: Environment variable management

### Frontend Dependencies
- Docusaurus: Static site generator
- React: UI library
- Standard web APIs: fetch, localStorage, etc.

## Deployment Considerations

### Backend Deployment
- Containerization with Docker (Dockerfile provided)
- Environment variable management
- Health check endpoints
- Logging configuration

### Frontend Deployment
- Static site generation
- CDN hosting capability
- Client-side API URL configuration
- Build optimization

## Future Enhancements

### Planned Features
- URL processing endpoint implementation
- Session management improvements
- Advanced conversation memory
- Multi-language support
- Enhanced source citation formatting

### Performance Improvements
- Response caching
- Database connection pooling
- Asynchronous processing optimization
- Embedding caching

## Testing Strategy

### Backend Testing
- Unit tests for individual components
- Integration tests for API endpoints
- End-to-end tests for complete workflows
- Performance tests for response times

### Frontend Testing
- Component testing with Jest
- Integration tests for API communication
- User interface tests
- Cross-browser compatibility tests

## Monitoring and Observability

### Logging
- Structured logging with timestamps
- Different log levels (INFO, ERROR, DEBUG)
- Request/response logging for debugging

### Metrics
- Response time tracking
- Error rate monitoring
- API usage statistics
- Database performance metrics

## Maintenance

### Backup Strategy
- Vector database backup procedures
- Configuration backup
- Code versioning with Git

### Update Procedures
- API versioning strategy
- Backward compatibility considerations
- Migration procedures for schema changes