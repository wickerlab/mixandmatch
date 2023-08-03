import React, { useState } from "react";
import axios from "axios";
import "../../css/components/chat/ChatInput.css";

const ChatInput = ({ user, clickedUser, setMessages }) => {
    const [textArea, setTextArea] = useState("");
    const [textAreaRows, setTextAreaRows] = useState(1);

    const handleChange = (e) => {
        setTextArea(e.target.value);

        // Calculate the number of lines in the text area
        const lines = e.target.value.split("\n");
        setTextAreaRows(Math.min(5, lines.length)); // Limit to a maximum of 5 rows
    };

    const addMessage = async () => {
        const message = {
            timestamp: new Date().toISOString(),
            from_userId: user.id,
            to_userId: clickedUser.id,
            message: textArea,
        };

        try {
            await axios.post("http://localhost:8000/message", { message });
            setMessages((prevMessages) => [...prevMessages, message]);
            setTextArea("");
            setTextAreaRows(1); // Reset the rows to 1 after submitting the message
        } catch (error) {
            console.log(error);
        }
    };

    return (
            <div className="chat-input">
                <textarea className="chat-textarea"
                    rows={textAreaRows}
                    value={textArea}
                    onChange={handleChange}
                />
                <button className="sent-button" onClick={addMessage}>
                    Sent
                </button>
            </div>
    );
};

export default ChatInput;
