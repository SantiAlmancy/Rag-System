// Sidebar.js
import React from 'react';
import logo from '../items/logo1.png';
import './Sidebar.css';

const Sidebar = ({ conversations, onSelectConversation, onNewConversation, onClearConversations }) => {

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
        <button className="sidebar-button" onClick={onNewConversation}>
          New Conversation
        </button>
        <button className="sidebar-button" onClick={onClearConversations}>
          Clear Conversations
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
