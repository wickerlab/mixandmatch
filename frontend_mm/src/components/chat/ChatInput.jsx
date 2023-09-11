import React, { useState } from "react";
import "../../css/components/chat/ChatInput.css";
import { w3cwebsocket as W3CWebSocket } from "websocket"; // Import the WebSocket library

const ChatInput = ({ user, clickedUser, setMessages }) => {
    const [textArea, setTextArea] = useState("");
    const [textAreaRows, setTextAreaRows] = useState(1);

    const handleChange = (e) => {
        setTextArea(e.target.value);

        // Calculate the number of lines in the text area
        const lines = e.target.value.split("\n");
        setTextAreaRows(Math.min(5, lines.length)); // Limit to a maximum of 5 rows
    };

    const addMessage = () => {
        const message = {
            sender_id: "5",
            receiver_id: "6",
            message: textArea,
        };

        // Create a WebSocket client and connect to your WebSocket server
        const client = new W3CWebSocket("ws://localhost:8765"); // Replace with your WebSocket server URL

        client.onopen = () => {
            // Send the message as a JSON string when the WebSocket connection is open
            client.send(JSON.stringify(message));
        };

        client.onclose = () => {
            // Handle the WebSocket connection closing, if needed
        };

        client.onerror = (error) => {
            console.error("WebSocket Error: ", error);
        };

        client.onmessage = (message) => {
            // Handle incoming WebSocket messages, if needed
        };

        setMessages((prevMessages) => [...prevMessages, message]);
        setTextArea("");
        setTextAreaRows(1); // Reset the rows to 1 after submitting the message
    };

    return (
        <div className="chat-input">
            <textarea
                className="chat-textarea"
                rows={textAreaRows}
                value={textArea}
                onChange={handleChange}
            />
            <button className="primary-button" onClick={addMessage}>
                Sent
            </button>
        </div>
    );
};

export default ChatInput;
