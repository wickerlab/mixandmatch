import React, { useState } from "react";
import "../css/components/MatchesDisplay.css";
import {useNavigate} from "react-router-dom";
import axios from "axios";

const ChattingUserDisplay = ({ chattingUser }) => {
    const [sidebarVisible, setSidebarVisible] = useState(true);
    let navigate = useNavigate();

    const handleIconClick = (userId) => {
        console.log(chattingUser);
        navigate('/chatting', { state: { userId, chattingUser } });
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
                        <div
                            key={match.user_id}
                            className="match-icon"
                            onClick={() => handleIconClick(match.user_id)}
                        >
                            <img
                                src={match.photo}
                                alt={match.name}
                                className="match-icon-image"
                            />
                        </div>
                    ))}
                </div>
        </div>
    );
};

export default ChattingUserDisplay;
