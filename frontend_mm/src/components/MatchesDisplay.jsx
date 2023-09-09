import React, { useState } from "react";
import "../css/components/MatchesDisplay.css";
import {useNavigate} from "react-router-dom";
import axios from "axios";

const MatchesDisplay = ({ matches, setClickedUser }) => {
    const [sidebarVisible, setSidebarVisible] = useState(true);
    let navigate = useNavigate();

    const handleIconClick = (userId) => {
        const currentPath = window.location.pathname;
        if (currentPath === "/dashboard") {
            // Redirect to /chatting page
            window.location.href = `/chatting`;
            // Set clicked user when already on /chatting page
            const clickedUser = matches.find((match) => match.id === userId);
            setClickedUser(clickedUser);

        } else if (currentPath === "/chatting") {
            // Set clicked user when already on /chatting page
            const clickedUser = matches.find((match) => match.id === userId);
            setClickedUser(clickedUser);
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

    const handleShowSidebar = () => {
        setSidebarVisible(true);
    };

    return (
        <div className="matches-display">
                <button className="matches-button" onClick={handleLogout}>
                    Logout
                </button>
                <div className="match-icons-container">
                    {matches.map((match) => (
                        <div
                            key={match.id}
                            className="match-icon"
                            onClick={() => handleIconClick(match.id)}
                        >
                            <img
                                src={match.profileImageUrl}
                                alt={match.name}
                                className="match-icon-image"
                            />
                        </div>
                    ))}
                </div>
        </div>
    );
};

export default MatchesDisplay;
