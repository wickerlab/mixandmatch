import React, {useEffect, useState} from "react";
import ChatHeader from "./ChatHeader.jsx";
import ChatDisplay from "./ChatDisplay.jsx";

import "../../css/components/chat/ChatContainer.css";
import ChatInput from "./ChatInput.jsx";

const ChatContainer = ({ currentUserId, clickedUser , setClickedUser}) => {
    const [selectedChat, setSelectedChat] = useState("matches");

    return (
        <div className="chat-container">
            <ChatHeader clickedUser={clickedUser} />
            {clickedUser ? (
                <ChatDisplay currentUserId={currentUserId} clickedUser={clickedUser} />
            ) : (
                <p>Please select a user</p>
            )}
            <ChatInput currentUserId={currentUserId} clickedUser={clickedUser} setClickedUser={setClickedUser}/>
        </div>
    );
};

export default ChatContainer;