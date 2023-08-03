import React from "react";
import "../../css/components/chat/Chat.css";

const isLastMessageFromUser = (index, messages, userId) => {
    for (let i = index + 1; i < messages.length; i++) {
        if (messages[i].fromUserId === userId) {
            return false;
        }
    }
    return true;
};

const Chat = ({ messages, user, clickedUser }) => {
    return (
        <div className="chat-bubble-container">
            {messages.map((message, index) => (
                <div
                    key={index}
                    className={`chat-bubble ${message.fromUserId === user.id ? "sent" : "received"} ${isLastMessageFromUser(index, messages, message.fromUserId) ? "" : "noTail"}`}
                >
                    <p className="chat-text">{message.message}</p>
                </div>
            ))}
        </div>
    );
};

export default Chat;
