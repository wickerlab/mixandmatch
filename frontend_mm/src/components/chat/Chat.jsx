import React from "react";
import "../../css/components/chat/Chat.css";

const isLastMessageFromUser = (index, messages, userId) => {
    for (let i = index + 1; i < messages.length; i++) {
        if (messages[i].sender_id === userId) {
            return false;
        }
    }
    return true;
};

const Chat = ({ messages, currentUserId, clickedUser }) => {
    return (
        <div className="chat-bubble-container">
            {messages.map((message, index) => (
                <div
                    key={index}
                    className={`chat-bubble ${message.sender_id === currentUserId ? "sent" : "received"} ${isLastMessageFromUser(index, messages, message.sender_id) ? "" : "noTail"}`}
                >
                    <p className="chat-text">{message.message}</p>
                </div>
            ))}
        </div>
    );
};

export default Chat;
