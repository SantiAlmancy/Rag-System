import React, { useState } from 'react';
import './InputBox.css';
import { askFormula1 } from '../services/Question';

const InputBox = ({ onSend, isDisabled }) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleKeyPress = async (event) => {
    if (event.key === 'Enter' && inputValue.trim() !== '' && !isDisabled) {
      onSend(inputValue);
      setInputValue('');

      try {
        const aiResponse = await askFormula1(inputValue, "");
  
        onSend(aiResponse, "ai");
        setInputValue('');
      } catch (error) {
        console.error("Error fetching AI response:", error);
        onSend("Error getting the AI response. Please try again.", "ai");
        setInputValue('');
      } finally {
      }
    }
  };

  const handleSendClick = async () => {
    if (inputValue.trim() !== '' && !isDisabled) {
      onSend(inputValue);
      setInputValue('');

      try {
        const aiResponse = await askFormula1(inputValue, "");
  
        onSend(aiResponse, "ai");
        setInputValue('');
      } catch (error) {
        console.error("Error fetching AI response:", error);
        onSend("Error getting the AI response. Please try again.", "ai");
        setInputValue('');
      } 
    }
  };

  return (
    <div className="input-box">
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
        disabled={isDisabled}
      />
      <button onClick={handleSendClick} disabled={isDisabled}>
        {isDisabled ? "Waiting..." : "Send"} {}
      </button>
    </div>
  );
};

export default InputBox;
