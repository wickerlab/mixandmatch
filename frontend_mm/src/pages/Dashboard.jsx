import React, { useEffect, useState } from "react";
import SwipingCard from "../components/SwipeCard.jsx";
import MatchesDisplay from "../components/MatchesDisplay.jsx";
import axios from "axios";

const Dashboard = () => {
    const [matches, setMatches] = useState([]);
    const [hasFetchedMatches, setHasFetchedMatches] = useState(false);

    useEffect(() => {
        if (!hasFetchedMatches) {
            // Fetch matches only once when the component mounts
            fetchMatches().then(() => {
                console.log("Fetched matches user effect triggered");
                setHasFetchedMatches(true);
            });
        }
    }, [hasFetchedMatches]);

    useEffect(() => {
        if (matches.length === 0 && hasFetchedMatches) {
            // Fetch more users when all users have been swiped
            fetchMatches().then(() => console.log("Fetched more matches"));
        }
    }, [matches]);

    const fetchMatches = async () => {
        try {
            const axiosWithCookies = axios.create({
                withCredentials: true
            });

            const response = await axiosWithCookies.get("http://127.0.0.1:5000/matches");
            const newMatches = response.data.recommended_users;

            setMatches((prevMatches) => [...prevMatches, ...newMatches]);

            // Reset the flag after fetching matches
            setHasFetchedMatches(false);
        } catch (error) {
            console.error("Error fetching matches:", error);
        }
    };

    const handleSwipe = async (direction, nameToDelete, userId) => {
        try {
            if (!hasFetchedMatches) {
                await fetchMatches();
                setHasFetchedMatches(true);
            }

            const formData = new FormData();
            const decision = direction === 'left' ? 'reject' : 'accept';
            let fakeTimeStamp = 0.1;

            console.log(userId);
            if (userId === undefined) {
                console.error("userId is undefined");
            }

            formData.append('match_decision', decision);
            // TODO delete this
            formData.append('match_time', fakeTimeStamp);

            //TODO change this to the actual url
            const response = await axios.post(`http://127.0.0.1:5000/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                withCredentials: true
            });

            console.log(response.data);

            if (matches.length === 0) {
                fetchMatches().then(() => console.log("Fetched more matches"));
            }
        } catch (error) {
            console.error("Error handling swipe:", error);
        }
    };

    const handleCardLeftScreen = (name) => {
        console.log(name + ' left the screen!');
    };

    const swipe = async (dir, index) => {
        console.log("reached swipe function", matches[index].id);
        try {
            await handleSwipe(dir, matches[index].username, matches[index].id);
        }
        catch(error) {
            console.error("Error in swipe:", error);
        };
        childRefs[index].current.swipe(dir);
    };

    const getCharacterData = () => {
        const uniqueIds = new Set();
        return matches
            .filter(user => {
                if (uniqueIds.has(user.id)) {
                    return false; // Skip users with duplicate IDs
                }
                uniqueIds.add(user.id); // Add the ID to the set to mark it as seen
                return true; // Include users with unique IDs
            })
            .map((user) => ({
                id: user.id,
                name: user.username,
                age: user.attr_age,
                gender: user.attr_gender,
                career: user.attr_career,
                education: user.attr_education,
                // TODO: Change this to the actual URL
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
