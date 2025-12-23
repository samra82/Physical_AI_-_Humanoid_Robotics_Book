import React, { useState } from 'react';
import ChatInterface from '@site/src/components/ChatInterface';
import styles from './FloatingChat.module.css';

const FloatingChat = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(true);

  const toggleChat = () => {
    if (!isOpen) {
      setIsOpen(true);
      setIsMinimized(false);
    } else {
      setIsMinimized(!isMinimized);
    }
  };

  const closeChat = () => {
    setIsOpen(false);
    setIsMinimized(true);
  };

  return (
    <div className={styles.floatingChatContainer}>
      {isOpen && !isMinimized && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <div className={styles.chatTitle}>Humanoid Robotics Assistant</div>
            <div className={styles.chatControls}>
              <button
                className={styles.minimizeButton}
                onClick={() => setIsMinimized(true)}
                aria-label="Minimize chat"
              >
                −
              </button>
              <button
                className={styles.closeButton}
                onClick={closeChat}
                aria-label="Close chat"
              >
                ×
              </button>
            </div>
          </div>
          <div className={styles.chatBody}>
            <ChatInterface />
          </div>
        </div>
      )}

      {(isOpen && isMinimized) && (
        <div className={styles.minimizedChat}>
          <button
            className={styles.minimizedButton}
            onClick={toggleChat}
            aria-label="Open chat"
          >
            <img src="\img\sparkle.svg" alt="icon" /> Humanoid Robotics Assistant
          </button>
        </div>
      )}

      {!isOpen && (
        <button
          className={styles.floatingButton}
          onClick={toggleChat}
          aria-label="Open chat"
        >
          <img src="\img\sparkle.svg" alt="icon" />
        </button>
      )}
    </div>
  );
};

export default FloatingChat;