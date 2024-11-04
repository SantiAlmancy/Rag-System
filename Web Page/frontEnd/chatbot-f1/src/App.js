import React, { useState, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    const loadedConversations = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith('conversation_')) {
        const conversation = JSON.parse(localStorage.getItem(key));
        loadedConversations.push({ id: key, messages: conversation });
      }
    }
    setConversations(loadedConversations);
  }, []);

  const addMessageToCurrentConversation = (newMessage) => {
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages, newMessage];

      if (!currentConversationId) {
        const newConversationId = `conversation_${Date.now()}`;
        setCurrentConversationId(newConversationId);
        const newConversation = { id: newConversationId, messages: updatedMessages };
        
        setConversations((prevConversations) => [...prevConversations, newConversation]);
        
        localStorage.setItem(newConversationId, JSON.stringify(updatedMessages));
      } else {
        localStorage.setItem(currentConversationId, JSON.stringify(updatedMessages));

        setConversations((prevConversations) =>
          prevConversations.map((conversation) =>
            conversation.id === currentConversationId
              ? { ...conversation, messages: updatedMessages }
              : conversation
          )
        );
      }

      return updatedMessages;
    });
  };

  const loadConversation = (conversation) => {
    setMessages(conversation.messages || []);
    setCurrentConversationId(conversation.id);
  };

  const handleNewConversation = () => {
    const newConversationId = `conversation_${Date.now()}`;
    setMessages([]);
    setCurrentConversationId(newConversationId);
    const newConversation = { id: newConversationId, messages: [] };
    
    setConversations((prevConversations) => [...prevConversations, newConversation]);
    localStorage.setItem(newConversationId, JSON.stringify([]));
  };

  const clearAllConversations = () => {
    localStorage.clear();
    setConversations([]);
    setMessages([]);
    setCurrentConversationId(null);
  };

  return (
    <div className="app-container">
      <Sidebar 
        conversations={conversations}
        onSelectConversation={loadConversation} 
        onNewConversation={handleNewConversation} 
        onClearConversations={clearAllConversations}
      />
      <ChatWindow messages={messages} onAddMessage={addMessageToCurrentConversation} />
    </div>
  );
}

export default App;
