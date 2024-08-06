import React, { useEffect, useState } from "react";
import "../../css/sidebar/ChattingUser.css";

const ChattingUser = ({ match, handleIconClick, newMessagesId }) => {
    const [imageLoaded, setImageLoaded] = useState(false);
    const [iconClicked, setIconClicked] = useState(false);
    const [className, setClassName] = useState("match-icon-no-message");

    // Function to preload the image and set imageLoaded to true if successful
    const preloadImage = (url) => {
        const img = new Image();
        img.src = url;
        img.onload = () => {
            setImageLoaded(true);
        };
        img.onerror = () => {
            setImageLoaded(false);
        };
    };

    // Check if character.url is valid, if not, use a placeholder image
    const imageUrl = match.photo || "https://placehold.co/50x50";

    // Preload the image
    preloadImage(imageUrl);

    // Update the class name when newMessagesId changes
    useEffect(() => {
        if (newMessagesId === match.user_id || match.unread_count > 0) {
            console.log(match.unread_count);
            setClassName("match-icon-message");
        } else {
            setClassName("match-icon-no-message");
        }
    }, [newMessagesId, match.user_id]);

    const handleIconClickWrapper = () => {
        setClassName("match-icon-no-message");
        handleIconClick(match);
    };

    return (
        <div
            key={match.user_id}
            className={className}
            onClick={handleIconClickWrapper} // Use the wrapper function
        >
            {imageLoaded ? (
                <img
                    src={imageUrl}
                    alt={match.name}
                    className="match-icon-image"/>
            ) : (
                <img
                    src="https://placehold.co/40x40"
                    alt="Placeholder"
                    className="match-icon-image"/>
            )}
        </div>
    );
};

export default ChattingUser;
