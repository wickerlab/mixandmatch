import React, { useEffect, useRef } from "react";
import Chat from "./Chat.jsx";
import ChatInput from "./ChatInput.jsx";
import "../../css/components/chat/ChatDisplay.css";
import axios from "axios";

const ChatDisplay = ({ currentUserId, clickedUser, messages }) => {
    const chatDisplayRef = useRef(null);

    // Scroll to the bottom of the chat container when messages change
    useEffect(() => {
        if (chatDisplayRef.current) {
            chatDisplayRef.current.scrollTop = chatDisplayRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="chat-display" ref={chatDisplayRef}>
            <Chat
                messages={messages}
                currentUserId={currentUserId}
                clickedUser={clickedUser}
            />
        </div>
    );
};

export default ChatDisplay;
