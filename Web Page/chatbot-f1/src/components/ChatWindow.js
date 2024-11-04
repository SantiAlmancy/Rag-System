import React, { useEffect, useRef } from 'react';
import Message from './Message';
import InputBox from './InputBox';
import './ChatWindow.css';
import modelLogo from '../items/model.png';
import userLogo from '../items/user.jpg';

const ChatWindow = ({ messages, onAddMessage }) => {
  const messagesEndRef = useRef(null);

  const addMessage = (text, sender = "user") => {
    const newMessage = { text, sender, avatar: sender === "user" ? userLogo : modelLogo };
    onAddMessage(newMessage);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} avatar={msg.avatar} />
        ))}
        <div ref={messagesEndRef} /> {}
      </div>
      <div className="input-area">
        <InputBox onSend={addMessage} />
      </div>
    </div>
  );
};

export default ChatWindow;