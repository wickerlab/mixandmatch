// Dashboard.jsx

import TinderCard from 'react-tinder-card'
import React, {useEffect, useMemo, useState} from "react";
import SwipingCard from "../components/SwipeCard.jsx";
import MatchesDisplay from "../components/MatchesDisplay.jsx";
import "../css/pages/Dashboard.css"
import axios from "axios";



const Dashboard = () => {

   // const [user, setUser] = useState(null); // Mock user data, replace with actual user data
    const [matches, setMatches] = useState([]); // State to hold fetched matches

    // Use the mock data you provided
    const recommendedUsers = [
        {
            attr_age: 22,
            attr_career: '30TO50',
            attr_education: 'MASTERS',
            attr_gender: 'FEMALE',
            email: 'viableuser5@gmail.com',
            id: 9,
            password: 'viableuser5',
            username: 'viableuser5',
        },
        // ...other recommended users
    ];

    useEffect(() => {
        // Mock user data, replace with actual user data
    //         setMatches(recommendedUsers);
    //
    // }, []);

        // Fetch matches from the API
        async function fetchMatches() {
            try {

                // const authToken = ''; // Replace with your actual authentication token
                const axiosWithCookies = axios.create({
                    withCredentials: true
                });

                const response = await axiosWithCookies.get("http://127.0.0.1:5000/matches", {
                    headers:{
                    }

                });

                console.log(response);

                console.log(response.data.recommended_users);

                setMatches(response.data.recommended_users);
            } catch (error) {
                console.error("Error fetching matches:", error);
            }
        }

        fetchMatches();
        }, []);

        const getCharacterData = () => {
            // Return recommended users data
            return recommendedUsers.map((user) => ({
                name: user.username,
                // TODO CHANGE TO PHOTO CALL
                url: "https://cataas.com/cat/says/John%20Doe!",
            }));
        };

        //Mock user data delete later
    const user = {
        id: "1",
        name: "John Doe",
        age: 28,
        gender: "male",
        location: "New York",
        bio: "Hello, I'm John! I enjoy long walks on the beach and exploring new places. Looking for someone who shares similar interests.",
        profileImageUrl: "https://cataas.com/cat/says/John%20Doe!",
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
                profileImageUrl: "https://cataas.com/cat/says/Jane%20Smith!"
            }
        ]
    };


    const [lastDirection, setLastDirection] = useState()

    const childRefs = useMemo(
        () =>
            Array(getCharacterData().length)
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
                    {getCharacterData().map((character, index) => (
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
                        {/*{lastDirection ? <p>You swiped {lastDirection}</p> : null}*/}
                    </div>
            </div>
        </div>
    );
}

export default Dashboard;
