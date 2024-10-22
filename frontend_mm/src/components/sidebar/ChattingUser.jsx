import React, { useEffect, useState } from "react";
import "../../css/sidebar/ChattingUser.css";
import axios from "axios";

const ChattingUser = ({ match, handleIconClick, newMessagesId }) => {
    const [imageURL, setImageURL] = useState("https://placehold.co/50x50");
    const [iconClicked, setIconClicked] = useState(false);
    const [className, setClassName] = useState("match-icon-no-message");


    // Update the class name when newMessagesId changes
    useEffect(() => {
        if (newMessagesId === match.user_id || match.unread_count > 0) {
            console.log(match.unread_count);
            setClassName("match-icon-message");
        } else {
            setClassName("match-icon-no-message");
        }

        // the match prop does not come with an imageURL property
        // have to fetch the user data again to get the image
        async function fetchProfilePicture(userID) {
            try {
                const axiosWithCookies = axios.create({
                    withCredentials: true
                })
                const response = await axiosWithCookies.get(`http://127.0.0.1:5000/users/${userID}`);
                console.log("inside", response.data);
                const url = await response.data.user.imageURL;
                setImageURL(url);
            } catch (error) {
                console.log("Error getting image", error);
            }
        }
        fetchProfilePicture(match.user_id); 

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
                <img
                    src={imageURL}
                    alt={match.name}
                    className="match-icon-image"/>
        </div>
    );
};

export default ChattingUser;
