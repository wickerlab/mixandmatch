import React, {useEffect, useState} from "react";
import "../../css/components/MatchesDisplay.css";
import {useNavigate} from "react-router-dom";
import axios from "axios";
import ChattingUser from "./ChattingUser.jsx";

const ChattingUserDisplay = ({newMessagesId}) => {
    const [sidebarVisible, setSidebarVisible] = useState(true);
    const [chattingUser, setChattingUser] = useState([]);
    const [currentUserId, setCurrentUserId] = useState(0);
    let navigate = useNavigate();

    const handleIconClick = (selectedUser) => {
        navigate('/chatting', { state: { currentUserId, selectedUser, chattingUser } });
    };

    useEffect(() => {
        // Fetch chatting user data when the component mounts
        fetchChatUsers().then(() => {
        });
    }, []);

    const fetchChatUsers = async () => {
        try {
            const axiosWithCookies = axios.create({
                withCredentials: true
            });

            // Fetch matches from the /chat endpoint
            const response = await axiosWithCookies.get("http://127.0.0.1:5000/chat");
            const chatUsers = response.data.chat_users;
            const currentUserId = response.data.user_id;

            // Update the matches state with the fetched data
            setChattingUser(chatUsers);
            setCurrentUserId(currentUserId);
        } catch (error) {
            console.error("Error fetching matches:", error);
        }
    };

    const handleLogout = async () => {
        const axiosWithCookies = axios.create({
            withCredentials: true
        });

        const response = await axiosWithCookies.get("http://127.0.0.1:5000/logout");
        const success = response.status === 200;
        if (success) {
            navigate('/');
        }

    };

    return (
        <div className="matches-display">
                <button className="matches-button" onClick={handleLogout}>
                    Logout
                </button>
                <div className="match-icons-container">
                    {chattingUser?.map((match) => (
                        <ChattingUser
                            key={match.user_id}
                            match={match}
                            handleIconClick={handleIconClick}
                            newMessagesId={newMessagesId}
                        />
                    ))}
                </div>
        </div>
    );
};

export default ChattingUserDisplay;
