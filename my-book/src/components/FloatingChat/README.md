# Floating Chatbot for Docusaurus

## Overview
This component provides a floating chatbot that appears on the bottom right of every page in your Docusaurus site. It connects to a backend RAG system to provide AI-powered responses about your content.

## Features
- 🟢 **Floating Design**: Appears on bottom right of every page
- 🟢 **Professional UI**: Modern gradient design with animations
- 🟢 **Responsive**: Works on desktop and mobile devices
- 🟢 **Minimizable**: Can be minimized while keeping the conversation
- 🟢 **Smooth Animations**: Includes floating, slide-in, and fade-in effects

## Backend Setup

To use the chatbot, you need to run the backend server:

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_URL=your_qdrant_url
   ```

4. Run the backend server:
   ```bash
   python -m src.api.main
   ```

The backend will start on `http://localhost:8000`.

## API Configuration

The chatbot connects to `http://localhost:8000/api/v1` by default. To configure a different API URL, you can set a global variable:

```javascript
// In your Docusaurus config or a script tag
window.DOCUSAURUS_API_CONFIG = {
  baseUrl: 'https://your-api-url.com/api/v1'
};
```

## Customization

### Colors
You can customize the color scheme by modifying the gradient values in:
- `FloatingChat.module.css` (buttons, header, etc.)
- `ChatInterface.module.css` (message bubbles)

### Size
Adjust the chat window dimensions by modifying the width/height values in `FloatingChat.module.css`.

### Animations
The component includes several animations:
- Floating button animation
- Slide-in animation for chat window
- Fade-in animation for messages
- Typing indicator animation

## Troubleshooting

### Common Issues:

1. **"Unable to connect to the AI service"**
   - Make sure the backend server is running on `http://localhost:8000`
   - Check that the API endpoints are accessible

2. **"API service endpoint not available"**
   - Verify that the backend is properly configured
   - Check the API routes in your backend

3. **CORS Issues**
   - Make sure your backend allows requests from your frontend domain
   - The backend should have CORS configured to allow your site's origin