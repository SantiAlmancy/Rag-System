// Sidebar.js
import React, { useState, useEffect } from 'react';
import logo from '../items/logo1.png';
import './Sidebar.css';

const Sidebar = ({ onSelectConversation, onNewConversation }) => {
  const [conversations, setConversations] = useState([]);

  // Load conversations from localStorage when the component mounts
  useEffect(() => {
    const storedConversations = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith('conversation_')) {
        const conversation = JSON.parse(localStorage.getItem(key));
        storedConversations.push({ id: key, messages: conversation });
      }
    }
    setConversations(storedConversations);
  }, []);

  const handleNewConversation = () => {
    const newConversation = { id: `conversation_${Date.now()}`, messages: [] };
    localStorage.setItem(newConversation.id, JSON.stringify(newConversation.messages)); // Store in localStorage
    setConversations((prev) => [...prev, newConversation]);
    onNewConversation(newConversation); // Trigger the new conversation in the ChatWindow
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <img 
          src={logo}
          alt="Logo"
          className="sidebar-logo"
        />
        <span className="sidebar-text">Chatbot</span>
      </div>
      <div className="sidebar-body">
        <span className="sidebar-conversation">Conversations</span>
        <button className="new-conversation-button" onClick={handleNewConversation}>
          New Conversation
        </button>
        <div className="conversation-list">
          {conversations.map((conversation) => (
            <div 
              key={conversation.id} 
              className="conversation-item" 
              onClick={() => onSelectConversation(conversation)}
            >
              {conversation.id.replace('conversation_', 'Conversation ')}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
