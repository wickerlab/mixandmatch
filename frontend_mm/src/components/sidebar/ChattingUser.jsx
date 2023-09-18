// Match.jsx
import React, {useState} from "react";

const ChattingUser = ({ match, handleIconClick }) => {

    const [imageLoaded, setImageLoaded] = useState(false);

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
    const imageUrl = match.photo || "https://placehold.co/600x400";

    const iconClassName = match.unread_count > 0 ? "match-icon-message" : "match-icon-no-message";

    // Preload the image
    preloadImage(imageUrl);

    return (
        <div
            key={match.user_id}
            className={iconClassName}
            onClick={() => handleIconClick(match)}
        >
            {imageLoaded ? (
                <img src={imageUrl} alt={match.name}  className="match-icon-image"/>
            ) : (
                <img src="https://placehold.co/600x400" alt="Placeholder" className="match-icon-image"/>
            )}
        </div>
    );
};

export default ChattingUser;
