import ChattingUserDisplay from "../components/sidebar/ChattingUserDisplay.jsx";
import React, {useState} from "react";
import ChatContainer from "../components/chat/ChatContainer.jsx";
import axios from "axios";
import {useLocation} from "react-router-dom";

const Chatting = ({ descendingOrderMessages }) => {

    const location = useLocation();

    const currentUserId = location.state ? location.state.currentUserId : null;
    const selectedUser = location.state ? location.state.selectedUser : null;
    const chattingUser = location.state ? location.state.chattingUser : null;

    console.log("Current User Id: ", currentUserId);
    console.log("Selected User: ", selectedUser);
    console.log(chattingUser);

    const [clickedUser, setClickedUser] = useState(selectedUser);

    return (
        <div className="dashboard">
            <ChattingUserDisplay/>
            <ChatContainer currentUserId={currentUserId} clickedUser={selectedUser} setClickedUser={setClickedUser}/>
        </div>
    );
}

export default Chatting;
