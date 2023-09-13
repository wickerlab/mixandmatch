import React, { useEffect, useRef, useState } from "react";
import Chat from "./Chat.jsx";
import ChatInput from "./ChatInput.jsx";
import "../../css/components/chat/ChatDisplay.css";
import axios from "axios";

const ChatDisplay = ({ currentUserId, clickedUser, messages }) => {

    const chatDisplayRef = useRef(null);




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
