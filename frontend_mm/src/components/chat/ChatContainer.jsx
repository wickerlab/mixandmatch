import React, {useEffect, useState} from "react";
import ChatHeader from "./ChatHeader.jsx";
import ChatDisplay from "./ChatDisplay.jsx";

import "../../css/components/chat/ChatContainer.css";
import ChatInput from "./ChatInput.jsx";
import xmppService from "../../resource/xmppService.jsx"; // Import your xmppService

const ChatContainer = ({ user, clickedUser }) => {
    const [message, setMessage] = useState("");
    const [chatMessages, setChatMessages] = useState([]);

    useEffect(() => {
        const onMessageReceived = (msg) => {
            const body = msg.getElementsByTagName("body")[0];
            setChatMessages((prevMessages) => [
                ...prevMessages,
                { text: body.textContent, sender: clickedUser.id },
            ]);
        };

        if (clickedUser) {
            xmppService.connect(
                "your_jid@xmpp-server.com",
                "your_password",
                onMessageReceived
            );
        }

        return () => {
            xmppService.disconnect();
        };
    }, [clickedUser]);

    const handleSendMessage = () => {
        if (message.trim() !== "") {
            xmppService.sendMessage(
                `${clickedUser.id}@xmpp-server.com`, // Assuming each user's JID follows this format
                message
            );
            setChatMessages((prevMessages) => [
                ...prevMessages,
                { text: message, sender: user.id },
            ]);
            setMessage("");
        }
    };

    return (
        <div className="chat-container">
            {clickedUser ? (
                <div className="chat">
                    {chatMessages.map((chatMessage, index) => (
                        <div
                            key={index}
                            className={`message ${
                                chatMessage.sender === user.id ? "sent" : "received"
                            }`}
                        >
                            {chatMessage.text}
                        </div>
                    ))}
                    <div className="message-input">
                        <input
                            type="text"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                        />
                        <button onClick={handleSendMessage}>Send</button>
                    </div>
                </div>
            ) : (
                <div className="select-user">Select a user to start chatting</div>
            )}
        </div>
    );
};

export default ChatContainer;
