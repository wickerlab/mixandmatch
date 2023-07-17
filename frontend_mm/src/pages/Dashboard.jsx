// Dashboard.jsx

import TinderCard from 'react-tinder-card'
import React, {useMemo, useState} from "react";
import ChatContainer from '../components/ChatContainer.jsx'
import SwipingCard from "../components/SwipeCard.jsx";
import MatchesDisplay from "../components/MatchesDisplay.jsx";

const Dashboard = () => {

    //const [user, setUser] = useState(null)

    //Mock user data delete later
    const user = {
        id: "1",
        name: "John Doe",
        age: 28,
        gender: "male",
        location: "New York",
        bio: "Hello, I'm John! I enjoy long walks on the beach and exploring new places. Looking for someone who shares similar interests.",
        profileImageUrl: "https://example.com/profile_images/john_doe.jpg",
        swipes: {
            liked: [],
            disliked: []
        },
        matches: [
            {
                id: "2",
                name: "Jane Smith",
                age: 26,
                gender: "female",
                location: "Los Angeles",
                bio: "Hi, I'm Jane! I love hiking and trying out new recipes. Let's connect!",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            {
                id: "3",
                name: "Alex Johnson",
                age: 30,
                gender: "non-binary",
                location: "San Francisco",
                bio: "Hey, I'm Alex! I'm passionate about photography and exploring different cultures.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            // Add 10 more matches
            {
                id: "4",
                name: "Emma Thompson",
                age: 27,
                gender: "female",
                location: "New York",
                bio: "Hi, I'm Emma! I enjoy painting and playing the piano.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            {
                id: "5",
                name: "Michael Johnson",
                age: 32,
                gender: "male",
                location: "Los Angeles",
                bio: "Hello, I'm Michael! I love playing basketball and traveling.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            {
                id: "6",
                name: "Sophie Wilson",
                age: 24,
                gender: "female",
                location: "London",
                bio: "Hey, I'm Sophie! I enjoy hiking and photography.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            {
                id: "7",
                name: "Daniel Anderson",
                age: 29,
                gender: "male",
                location: "San Francisco",
                bio: "Hi, I'm Daniel! I'm passionate about coding and exploring new technologies.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            {
                id: "8",
                name: "Olivia Rodriguez",
                age: 25,
                gender: "female",
                location: "Miami",
                bio: "Hello, I'm Olivia! I enjoy dancing and going to the beach.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            {
                id: "9",
                name: "Matthew Campbell",
                age: 31,
                gender: "male",
                location: "Toronto",
                bio: "Hey, I'm Matthew! I'm a foodie and love trying out new restaurants.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            {
                id: "10",
                name: "Isabella Martinez",
                age: 28,
                gender: "female",
                location: "Barcelona",
                bio: "Hi, I'm Isabella! I enjoy traveling and learning new languages.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            {
                id: "11",
                name: "David Thompson",
                age: 33,
                gender: "male",
                location: "Sydney",
                bio: "Hello, I'm David! I'm a nature enthusiast and love going on hikes.",
                profileImageUrl: "https://cataas.com/cat/says/hello%20world!"
            },
            // Add more matches here...
        ]
    };



    const characters = [
        {
            name: 'Richard Hendricks',
            url: 'https://media.discordapp.net/attachments/1093846572145582111/1130356342494863440/IMG_6151.png?width=406&height=878'
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
            url: 'https://media.discordapp.net/attachments/1093846572145582111/1130356342494863440/IMG_6151.png?width=406&height=878'
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
            <MatchesDisplay matches={user.matches} setClickedUser={user}/>
            <div className="swipe-container">
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
    );
}

export default Dashboard;
