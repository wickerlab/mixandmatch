import React, { useEffect, useState } from "react";
import SwipingCard from "../components/SwipeCard.jsx";
import MatchesDisplay from "../components/MatchesDisplay.jsx";
import axios from "axios";

const Dashboard = () => {
    const [matches, setMatches] = useState([]);
    const [lastDirection, setLastDirection] = useState();

    const fetchMatches = async () => {
        try {
            const axiosWithCookies = axios.create({
                withCredentials: true
            });

            const response = await axiosWithCookies.get("http://127.0.0.1:5000/matches");
            setMatches(response.data.recommended_users);
        } catch (error) {
            console.error("Error fetching matches:", error);
        }
    };

    useEffect(() => {
        fetchMatches().then(r => console.log("Fetched matches"));
    }, []);

    const handleSwipe = async (direction, nameToDelete, userId) => {

        const formData = new FormData();
        const decision = direction === 'left' ? 'reject' : 'accept';
        let fakeTimeStamp = 0.1;

        formData.append('match_decision', decision);
        //TODO delete this
        formData.append('match_time', fakeTimeStamp);

        const response = await axios.post(`http://127.0.0.1:5000/matches/${userId}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            withCredentials: true
        });

        console.log(response.headers.get("Set-Cookie"));


        console.log('Removing: ' + nameToDelete);
        setLastDirection(direction);
    };

    const handleCardLeftScreen = (name) => {
        console.log(name + ' left the screen!');
    };

    const swipe = async (dir, index) => {
        console.log(matches);
        await childRefs[index].current.swipe(dir);
    };

    const getCharacterData = () => {
        return matches.map((user) => ({
            id: user.id,
            name: user.username,
            url: `https://cataas.com/cat/says/${user.username}`
        }));
    };

    const childRefs = matches.map(() => React.createRef());

    const mockUser = {
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

    return (
        <div className="dashboard">
            <MatchesDisplay matches={mockUser.matches} setClickedUser={mockUser} />
            <div className="swipe-container">
                {getCharacterData().map((character, index) => (
                    <SwipingCard
                        key={character.id}
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
};

export default Dashboard;
