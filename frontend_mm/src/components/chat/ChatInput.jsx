import React, { useState } from "react";
import "../../css/components/chat/ChatInput.css";
import { w3cwebsocket as W3CWebSocket } from "websocket"; // Import the WebSocket library

const ChatInput = ({ currentUserId, clickedUser, setMessages, ws }) => {
    const [textArea, setTextArea] = useState("");
    const [textAreaRows, setTextAreaRows] = useState(1);

    const handleChange = (e) => {
        setTextArea(e.target.value);

        // Calculate the number of lines in the text area
        const lines = e.target.value.split("\n");
        setTextAreaRows(Math.min(5, lines.length)); // Limit to a maximum of 5 rows
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            // Prevent the default Enter key behavior (new line)
            e.preventDefault();
            addMessage();
        }
    };

    const addMessage = () => {
        // Check if the message is empty
        if (textArea.trim() === "") {
            return;
        }
        // Check if the currentUserId and clickedUser are defined
        if (!currentUserId || !clickedUser) {
            console.log("currentUserId or clickedUser is undefined");
            return;
        }

        // Send the message to the WebSocket server
        const message = {
            sender_id: currentUserId,
            receiver_id: clickedUser.user_id,
            message: textArea,
            status: "unread",
        };

        ws.current.send(JSON.stringify(message));
        setMessages((prevMessages) => [...prevMessages, message]);

        // Clear the text area after sending the message
        setTextArea("");
        setTextAreaRows(1);
    };

    return (
        <div className="chat-input">
      <textarea
          className="chat-textarea"
          rows={textAreaRows}
          value={textArea}
          onChange={handleChange}
          onKeyPress={handleKeyPress} // Add the keypress event listener
      />
            <button className="primary-button" onClick={addMessage}>
                Sent
            </button>
        </div>
    );
};

export default ChatInput;
