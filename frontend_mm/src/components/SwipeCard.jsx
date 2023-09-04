// SwipingCard.jsx

import TinderCard from "react-tinder-card";
import React from "react";

const SwipingCard = React.forwardRef(({ character, handleSwipe, handleCardLeftScreen, swipe }, ref) => {
    return (
        <TinderCard
            ref={ref}
            className='swipe'
            key={character.id}
            preventSwipe={['up', 'down']}
            onSwipe={(dir) => handleSwipe(dir, character.name, character.id)}
            onCardLeftScreen={() => handleCardLeftScreen(character.name)}
        >
            <div className='card'>
                <div className='image-half'>
                    <img src={character.url} alt={character.name} />
                </div>
                <div className='info-half'>
                    <div className='info-content'>
                        <h3 className='info-title'>{character.name}</h3>
                        <p className='info-about'>Hey, I'm a cat! I enjoy hiking and photography.</p>
                        <p className='info-attr-age'>Age: {character.age}</p>
                        <p className='info-attr-gender'>Gender : {character.gender}</p>
                        <p className='info-attr-career'>Career: {character.career}</p>
                        <p className='info-attr-education'>Education: {character.education}</p>
                    </div>
                    <div className="button-container">
                        <button className="dislike-button" onClick={() => swipe('left')}>
                            <img src="src/images/broken-heart.png" alt="Disike Button Image" className="dislike-button-image" />
                        </button>
                        <button className="like-button" onClick={() => swipe('right')}>
                            <img src="src/images/heart.png" alt="Like Button Image" className="like-button-image" />
                        </button>
                    </div>
                </div>
            </div>
        </TinderCard>
    );
});

export default SwipingCard;
