import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import ApiService from '@site/src/services/api';
import styles from './ChatInterface.module.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending a message
  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputMessage.trim()) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await ApiService.sendMessage(inputMessage, sessionId);

      // Update session ID if new session was created
      if (response.session_id && !sessionId) {
        setSessionId(response.session_id);
      }

      // Add AI response to chat
      const aiMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'ai',
        sources: response.sources || [],
        confidence: response.confidence_score,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Check if it's a network error or API is not running
      let errorMessageText = 'Sorry, I encountered an error processing your request. Please try again.';

      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        errorMessageText = 'Unable to connect to the AI service.';
      } else if (error.message.includes('404') || error.message.includes('405')) {
        errorMessageText = 'The AI service endpoint is not available. Please check if the backend is properly configured.';
      } else if (error.message.includes('500')) {
        errorMessageText = 'The AI service encountered an error. Please try again or contact support.';
      }

      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: errorMessageText,
        sender: 'system',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Format sources for display
  const formatSources = (sources) => {
    if (!sources || sources.length === 0) return null;

    return (
      <div className={styles.sources}>
        <h4>Sources:</h4>
        <ul>
          {sources.map((source, index) => (
            <li key={index}>
              <a href={source.source_url} target="_blank" rel="noopener noreferrer">
                {source.section_title || 'Source'}
              </a>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.welcomeMessage}>
            <p>Hello! I'm your Humanoid Robotics Assistant.</p>
            <p>Ask me any questions about Physical AI, Humanoid Robotics, or the content from the book.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`${styles.message} ${styles[message.sender]}`}
            >
              <div className={styles.messageContent}>
                {message.sender === 'ai' ? (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      // Custom components for better rendering
                      p: ({node, ...props}) => <p {...props} />,
                      strong: ({node, ...props}) => <strong {...props} />,
                      em: ({node, ...props}) => <em {...props} />,
                      h1: ({node, ...props}) => <h1 {...props} className={styles.markdownH1} />,
                      h2: ({node, ...props}) => <h2 {...props} className={styles.markdownH2} />,
                      h3: ({node, ...props}) => <h3 {...props} className={styles.markdownH3} />,
                      h4: ({node, ...props}) => <h4 {...props} className={styles.markdownH4} />,
                      h5: ({node, ...props}) => <h5 {...props} className={styles.markdownH5} />,
                      h6: ({node, ...props}) => <h6 {...props} className={styles.markdownH6} />,
                      ul: ({node, ...props}) => <ul {...props} className={styles.markdownUl} />,
                      ol: ({node, ...props}) => <ol {...props} className={styles.markdownOl} />,
                      li: ({node, ...props}) => <li {...props} className={styles.markdownLi} />,
                      blockquote: ({node, ...props}) => <blockquote {...props} className={styles.markdownBlockquote} />,
                      code: ({node, inline, ...props}) => {
                        if (inline) {
                          return <code {...props} className={styles.inlineCode} />;
                        } else {
                          return <code {...props} className={styles.codeBlock} />;
                        }
                      },
                      pre: ({node, ...props}) => <pre {...props} className={styles.preBlock} />,
                      table: ({node, ...props}) => <table {...props} className={styles.markdownTable} />,
                      thead: ({node, ...props}) => <thead {...props} />,
                      tbody: ({node, ...props}) => <tbody {...props} />,
                      tr: ({node, ...props}) => <tr {...props} className={styles.markdownTableRow} />,
                      th: ({node, ...props}) => <th {...props} className={styles.markdownTableHeader} />,
                      td: ({node, ...props}) => <td {...props} className={styles.markdownTableCell} />,
                    }}
                  >
                    {message.text}
                  </ReactMarkdown>
                ) : (
                  <p>{message.text}</p>
                )}
                {message.sender === 'ai' && formatSources(message.sources)}
                {message.confidence && (
                  <small className={styles.confidence}>
                    Confidence: {(message.confidence * 100).toFixed(1)}%
                  </small>
                )}
              </div>
              <small className={styles.timestamp}>
                {new Date(message.timestamp).toLocaleTimeString()}
              </small>
            </div>
          ))
        )}
        {isLoading && (
          <div className={`${styles.message} ${styles.ai} ${styles.thinking}`}>
            <div className={styles.messageContent}>
              <p>Thinking<span className={styles.typingIndicator}>...</span></p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className={styles.inputForm}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask a question about humanoid robotics..."
          disabled={isLoading}
          className={styles.input}
        />
        <button type="submit" disabled={isLoading} className={styles.sendButton}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;