import React, { useState } from "react";
import "../css/components/MatchesDisplay.css";

const MatchesDisplay = ({ matches, setClickedUser }) => {
    const [sidebarVisible, setSidebarVisible] = useState(true);

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

    const handleHideSidebar = () => {
        setSidebarVisible(false);
    };

    const handleShowSidebar = () => {
        setSidebarVisible(true);
    };

    return (
        <div className="matches-display">
            {!sidebarVisible && (
                <button className="matches-button" onClick={handleShowSidebar}>
                    SHOW
                </button>
            )}
            <div className={`matches-list ${sidebarVisible ? "" : "hidden"}`}>
                <button className="matches-button" onClick={handleHideSidebar}>
                    HIDE
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
        </div>
    );
};

export default MatchesDisplay;