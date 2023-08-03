import React, { useState } from "react";
import ChatHeader from "./ChatHeader.jsx";
import ChatDisplay from "./ChatDisplay.jsx";

import "../../css/components/chat/ChatContainer.css";
import ChatInput from "./ChatInput.jsx";

const ChatContainer = ({ user, clickedUser , setClickedUser}) => {
    const [selectedChat, setSelectedChat] = useState("matches");

    return (
        <div className="chat-container">
            <ChatHeader clickedUser={clickedUser} />
            {clickedUser ? (
                <ChatDisplay user={user} clickedUser={clickedUser} />
            ) : (
                <p>Please select a user</p>
            )}
            <ChatInput user={user} clickedUser={clickedUser} setClickedUser={setClickedUser}/>
        </div>
    );
};

export default ChatContainer;
