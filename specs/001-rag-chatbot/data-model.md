# Data Model: RAG Chatbot for Physical AI - Humanoid Robotics Book

## Knowledge Chunk
Represents a segment of the Physical AI - Humanoid Robotics Book content with associated metadata and vector embeddings

**Fields**:
- `id` (string): Unique identifier for the knowledge chunk
- `content` (string): The actual text content from the book
- `embedding` (array[float]): Vector representation of the content
- `metadata` (object): Additional information about the source
  - `source_url` (string): URL where the content was extracted from
  - `section_title` (string): Title of the book section
  - `page_number` (integer): Page number in the original book (if applicable)
  - `created_at` (datetime): Timestamp when chunk was created
  - `updated_at` (datetime): Timestamp when chunk was last updated

**Relationships**: None

## Query Session
Tracks a user's interaction history including questions, responses, and contextual state

**Fields**:
- `id` (string): Unique identifier for the session
- `user_id` (string): Identifier for the user (optional for anonymous sessions)
- `created_at` (datetime): Timestamp when session started
- `updated_at` (datetime): Timestamp when session was last updated
- `context_window` (array[object]): History of query-response pairs
  - `query` (string): User's question
  - `response` (string): AI-generated response
  - `timestamp` (datetime): When the interaction occurred
  - `retrieved_context` (array[string]): IDs of knowledge chunks used

**Relationships**:
- References multiple Knowledge Chunk objects via `retrieved_context`

## Retrieved Context
Represents relevant portions of the book content retrieved from the vector database to answer a specific query

**Fields**:
- `id` (string): Unique identifier for the retrieved context
- `query` (string): Original user query
- `relevant_chunks` (array[object]):
  - `chunk_id` (string): ID of the knowledge chunk
  - `content` (string): Content of the chunk
  - `similarity_score` (float): Similarity score between query and chunk
- `retrieval_timestamp` (datetime): When the retrieval was performed

**Relationships**:
- References multiple Knowledge Chunk objects via `relevant_chunks`

## Generated Response
AI-generated answer that combines retrieved context with language model capabilities

**Fields**:
- `id` (string): Unique identifier for the response
- `session_id` (string): Reference to the query session
- `query` (string): Original user query
- `response_text` (string): Generated response text
- `source_chunks` (array[string]): IDs of knowledge chunks used to generate response
- `generation_timestamp` (datetime): When the response was generated
- `confidence_score` (float): Confidence level of the response (0-1)

**Relationships**:
- Belongs to a Query Session via `session_id`
- References multiple Knowledge Chunk objects via `source_chunks`