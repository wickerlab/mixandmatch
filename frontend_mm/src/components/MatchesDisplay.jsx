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
        <div className={`matches-display ${sidebarVisible ? "" : "hidden"}`}>
            {!sidebarVisible && (
                <button className="show-sidebar-button" onClick={handleShowSidebar}>
                    Show Sidebar
                </button>
            )}
            <button className="hide-sidebar-button" onClick={handleHideSidebar}>
                Hide Sidebar
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
