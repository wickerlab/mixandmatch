// SwipingCard.jsx

import TinderCard from "react-tinder-card";
import React, {useState} from "react";

const SwipingCard = React.forwardRef(({ character, handleSwipe, handleCardLeftScreen, swipe }, ref) => {

    const salaryMapping = {
        "UNDER15": "Under $15k",
        "15TO30": "$15k - $30k",
        "30TO50": "$30k - $50k",
        "OVER50": "Above $50k"
    };

    const genderMapping = {
        "MALE": "Man",
        "FEMALE": "Woman",
    };

    const educationMapping = {
        "BACHELORS": "Bachelors",
        "MASTERS": "Masters",
        "DOCTORAL": "Doctoral",
        "DIPLOMA": "Diploma"
    };

    const handleDislikeButtonClick = () => {
        swipe('left');
    };

    const handleLikeButtonClick = () => {
        swipe('right');
    };

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
    const imageUrl = character.url || "https://placehold.co/600x400";

    // Preload the image
    preloadImage(imageUrl);

    return (
        <TinderCard
            ref={ref}
            className='swipe'
            key={character.id}
            preventSwipe={['up', 'down']}
            onSwipe={(dir) => handleSwipe(dir, character.name, character.id)}
            onCardLeftScreen={() => handleCardLeftScreen(character.id)}
        >
            <div className='card'>
                <div className='image-half'>
                    {imageLoaded ? (
                        <img src={imageUrl} alt={character.name} />
                    ) : (
                        <img src="https://placehold.co/600x400" alt="Placeholder" />
                    )}
                </div>
                <div className='info-half'>
                    <div className='info-content'>
                        <h3 className='info-title'>{character.name}</h3>
                        <p className='info-attr-age'>Age: {character.age}</p>
                        <p className='info-attr-gender'>Gender: {genderMapping[character.gender] || "[Error: invalid gender]"}</p>
                        <p className='info-attr-career'>Career: {salaryMapping[character.career] || "[Error: invalid salary]"}</p>
                        <p className='info-attr-education'>Education: {educationMapping[character.education] || "[Error: invalid education]"}</p>
                    </div>
                    <div className="button-container">
                        <button className="dislike-button" onClick={handleDislikeButtonClick}>
                            <img src="src/images/broken-heart.png" alt="Disike Button Image" className="dislike-button-image" />
                        </button>
                        <button className="like-button" onClick={handleLikeButtonClick}>
                            <img src="src/images/heart.png" alt="Like Button Image" className="like-button-image" />
                        </button>
                    </div>
                </div>
            </div>
        </TinderCard>
    );
});

export default SwipingCard;
