// SwipingCard.jsx

import TinderCard from "react-tinder-card";
import React from "react";

const SwipingCard = React.forwardRef(({ character, handleSwipe, handleCardLeftScreen, swipe }, ref) => {
    return (
        <TinderCard
            ref={ref}
            className='swipe'
            key={character.name}
            preventSwipe={['up', 'down']}
            onSwipe={(dir) => handleSwipe(dir, character.name)}
            onCardLeftScreen={() => handleCardLeftScreen(character.name)}
        >
            <div className='card'>
                <div className='image-half'>
                    <img src={character.url} alt={character.name} />
                </div>
                <div className='info-half'>
                    <div className='info-content'>
                        <h3>{character.name}</h3>
                        <p>Age: {character.age}</p>
                        <p>Location: {character.location}</p>
                        <button className="pressable" onClick={() => swipe('right')}>Button</button>
                    </div>
                </div>
            </div>
        </TinderCard>
    );
});

export default SwipingCard;
