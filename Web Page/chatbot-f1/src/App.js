// App.js
import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]); // Ensure it's always an array

  const addMessageToCurrentConversation = (newMessage) => {
    const updatedMessages = [...(messages || []), newMessage]; // Safely handle undefined messages
    setMessages(updatedMessages);

    const currentConversationId = `conversation_${Date.now()}`; // Create a unique ID for saving
    localStorage.setItem(currentConversationId, JSON.stringify(updatedMessages)); // Store the updated messages
  };

  const loadConversation = (conversation) => {
    const loadedMessages = conversation.messages || []; // Load messages or set as empty array if undefined
    setMessages(loadedMessages);
  };

  return (
    <div className="app-container">
      <Sidebar 
        onSelectConversation={loadConversation} 
        onNewConversation={() => setMessages([])} // Reset messages for a new conversation
      />
      <ChatWindow messages={messages} onAddMessage={addMessageToCurrentConversation} />
    </div>
  );
}

export default App;
