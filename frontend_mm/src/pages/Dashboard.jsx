import React, { useEffect, useState } from "react";
import SwipingCard from "../components/SwipeCard.jsx";
import ChattingUserDisplay from "../components/sidebar/ChattingUserDisplay.jsx";
import axios from "axios";
import {Loading} from "@minchat/react-chat-ui";

const Dashboard = () => {
    const [matches, setMatches] = useState([]);
    const [hasFetchedMatches, setHasFetchedMatches] = useState(false);
    const [allMatchesSwiped, setAllMatchesSwiped] = useState(false);
    const [isLoading, setIsLoading] = useState(true); // Initialize as true to show loading initially

    const userId = location.state ? location.state.userId : null;

    useEffect(() => {
        if (!hasFetchedMatches) {
            // Fetch matches only once when the component mounts
            fetchMatches().then(() => {
                console.log("Fetched matches user effect triggered");
                setHasFetchedMatches(true);
                setIsLoading(false);
            });
        }
    }, [hasFetchedMatches]);

    useEffect(() => {
        if (matches.length < 1 && hasFetchedMatches) {
            console.log(matches.length);
            // Fetch more users when all users have been swiped
            fetchMatches().then(() => {
                console.log("Fetched more matches");
                setAllMatchesSwiped(false);
                setIsLoading(false);
            });
        }
    }, [matches, hasFetchedMatches]);

    const fetchMatches = async () => {
        try {
            const axiosWithCookies = axios.create({
                withCredentials: true
            });

            const response = await axiosWithCookies.get("https://mixandmatch.wickerlab.org/api/matches");
            const newMatches = response.data.recommended_users;

            setMatches(newMatches);

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

            if (userId === undefined) {
                console.error("userId is undefined");
            }

            formData.append('match_decision', decision);
            // TODO delete this
            formData.append('match_time', fakeTimeStamp);

            //TODO change this to the actual url
            const response = await axios.post(`https://mixandmatch.wickerlab.org/api/matches/${userId}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                withCredentials: true
            });

            // Check if all matches have been swiped
            if (matches.length === 1) {
                // Fetch more matches if necessary
                await fetchMatches();
                console.log("Fetched more matches");
            }
        } catch (error) {
            console.error("Error handling swipe:", error);
        }
    };

    const handleCardLeftScreen = (userId) => {
        console.log(`User ${name} left the screen!`);
        const updatedMatches = matches.filter(match => match.id !== userId);
        setMatches(updatedMatches);
    };

    const swipe = async (dir, index) => {
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
                category: user.category,
                url: user.photo,
            }));
    };

    const childRefs = matches.map(() => React.createRef());

    return (
        <div className="dashboard">
            <ChattingUserDisplay/>
            <div className="swipe-container">
                {isLoading ? ( // Conditional rendering for loading SwipingCard section
                    <Loading />
                ) : (
                    getCharacterData().map((character, index) => (
                        <SwipingCard
                            key={character.id}
                            character={character}
                            handleSwipe={handleSwipe}
                            handleCardLeftScreen={handleCardLeftScreen}
                            ref={childRefs[index]}
                            swipe={(dir) => swipe(dir, index)}
                        />
                    ))
                )}
            </div>
        </div>
    );
};

export default Dashboard;