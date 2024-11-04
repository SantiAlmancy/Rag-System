import React from 'react';
import './Message.css';

const Message = ({ text, sender, avatar }) => {
  return (
    <div className={`message ${sender}`}>
      <img src={avatar} alt={`${sender} avatar`} className="avatar" />
      <div className="message-text">{text}</div>
    </div>
  );
};

export default Message;
