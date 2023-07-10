// Dashboard.jsx

import TinderCard from 'react-tinder-card'
import React, {useMemo, useState} from "react";
import ChatContainer from '../components/ChatContainer.jsx'
import SwipingCard from "../components/SwipeCard.jsx";

const Dashboard = () => {
    const characters = [
        {
            name: 'Richard Hendricks',
            url: 'https://cataas.com/cat/says/hello%20world!'
        },
        {
            name: 'Erlich Bachman',
            url: 'https://cataas.com/cat/says/hello%20world!'
        },
        {
            name: 'Monica Hall',
            url: 'https://cataas.com/cat/says/hello%20world!'
        },
        {
            name: 'Jared Dunn',
            url: 'https://cataas.com/cat/says/hello%20world!'
        },
        {
            name: 'Dinesh Chugtai',
            url: 'https://cataas.com/cat/says/hello%20world!'
        }
    ]
    const [lastDirection, setLastDirection] = useState()

    const childRefs = useMemo(
        () =>
            Array(characters.length)
                .fill(0)
                .map((i) => React.createRef()),
        []
    )

    const handleSwipe = (direction, nameToDelete) => {
        console.log('Removing: ' + nameToDelete);
        setLastDirection(direction);
    }

    const handleCardLeftScreen = (name) => {
        console.log(name + ' left the screen!');
    }

    const swipe = async (dir, index) => {
        await childRefs[index].current.swipe(dir)
    }

    return (
        <div className="dashboard">
            <ChatContainer />
            <div className="swipe-container">
                <div className="card-container">
                    {characters.map((character, index) => (
                        <SwipingCard
                            key={character.name}
                            character={character}
                            handleSwipe={handleSwipe}
                            handleCardLeftScreen={handleCardLeftScreen}
                            ref={childRefs[index]}
                            swipe={(dir) => swipe(dir, index)}
                        />
                    ))}
                    <div className="swipe-info">
                        {lastDirection ? <p>You swiped {lastDirection}</p> : null}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
