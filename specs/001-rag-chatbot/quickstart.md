# Quickstart: RAG Chatbot for Physical AI - Humanoid Robotics Book

## Prerequisites
- Python 3.11+
- Node.js 18+ (if my-book directory contains a Node.js application)
- Access to OpenAI API key
- Access to Cohere API key
- Qdrant vector database (as specified by user)

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `.env` file in the backend directory:

**Backend (.env):**
```env
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_url
SOURCE_URL=https://your-book-website-url.com
```

## Running the Application

### 1. Start the Backend
```bash
cd backend
python -m src.api.main
```
The backend will start on `http://localhost:8000`

### 2. Start the Frontend
```bash
cd my-book
# Follow the existing instructions in the my-book directory to start the frontend
# This may be: npm start, yarn start, or other depending on the existing setup
```

## Initial Content Processing

### 1. Extract Content from Website
```bash
python -m src.scripts.extract_content --url https://your-book-website-url.com
```

### 2. Generate Embeddings
```bash
python -m src.scripts.generate_embeddings
```

### 3. Store in Vector Database
```bash
python -m src.scripts.store_embeddings
```

## Usage

1. Ensure both backend and frontend applications are running
2. Open the frontend application (in my-book directory) in your browser
3. Type your question about humanoid robotics in the chat interface
4. The system will retrieve relevant information from the book and generate a response
5. View the source references to see which parts of the book informed the response

## API Endpoints

### Health Check
- `GET /health` - Check if the service is running

### Chat
- `POST /chat` - Send a message and receive a response
- Request body: `{"message": "your question", "session_id": "optional session id"}`
- Response: `{"response": "generated response", "session_id": "session id", "sources": ["source ids"]}`

### Content Processing
- `POST /process-url` - Process content from a URL and store embeddings
- Request body: `{"url": "https://your-book-website-url.com"}`