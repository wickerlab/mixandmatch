import React, { useState } from "react";

const MatchesDisplay = ({ matches, setClickedUser }) => {
    const [sidebarVisible, setSidebarVisible] = useState(true);

    const handleIconClick = (userId) => {
        setClickedUser(userId);
        setSidebarVisible(false);
    };

    const handleHideSidebar = () => {
        setSidebarVisible(false);
    };

    const handleShowSidebar = () => {
        setSidebarVisible(true);
    };

    return (
    <div className="matches-display" >
        {!sidebarVisible && (
            <button className="matches-button" onClick={handleShowSidebar}>
                SHOW
            </button>
        )}
        <div className={`matches-display ${sidebarVisible ? "" : "hidden"}`}>

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
