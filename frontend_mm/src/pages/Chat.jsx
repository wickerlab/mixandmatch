import MatchesDisplay from "../components/MatchesDisplay.jsx";
import React from "react";

const Chat = ({ descendingOrderMessages }) => {

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
            },
            {
                id: "3",
                name: "Alex Johnson",
                age: 30,
                gender: "non-binary",
                location: "San Francisco",
                bio: "Hey, I'm Alex! I'm passionate about photography and exploring different cultures.",
                profileImageUrl: "https://cataas.com/cat/says/Alex%20Johnson!"
            },
            // Add 10 more matches
            {
                id: "4",
                name: "Emma Thompson",
                age: 27,
                gender: "female",
                location: "New York",
                bio: "Hi, I'm Emma! I enjoy painting and playing the piano.",
                profileImageUrl: "https://cataas.com/cat/says/Emma%20Thompson!"
            },
            {
                id: "5",
                name: "Michael Johnson",
                age: 32,
                gender: "male",
                location: "Los Angeles",
                bio: "Hello, I'm Michael! I love playing basketball and traveling.",
                profileImageUrl: "https://cataas.com/cat/says/Michael%20Johnson!"
            },
            {
                id: "6",
                name: "Sophie Wilson",
                age: 24,
                gender: "female",
                location: "London",
                bio: "Hey, I'm Sophie! I enjoy hiking and photography.",
                profileImageUrl: "https://cataas.com/cat/says/Sophie%20Wilson!"
            },
            {
                id: "7",
                name: "Daniel Anderson",
                age: 29,
                gender: "male",
                location: "San Francisco",
                bio: "Hi, I'm Daniel! I'm passionate about coding and exploring new technologies.",
                profileImageUrl: "https://cataas.com/cat/says/Daniel%20Anderson!"
            },
            {
                id: "8",
                name: "Olivia Rodriguez",
                age: 25,
                gender: "female",
                location: "Miami",
                bio: "Hello, I'm Olivia! I enjoy dancing and going to the beach.",
                profileImageUrl: "https://cataas.com/cat/says/Olivia%20Rodriguez!"
            },
            {
                id: "9",
                name: "Matthew Campbell",
                age: 31,
                gender: "male",
                location: "Toronto",
                bio: "Hey, I'm Matthew! I'm a foodie and love trying out new restaurants.",
                profileImageUrl: "https://cataas.com/cat/says/Matthew%20Campbell!"
            },
            {
                id: "10",
                name: "Isabella Martinez",
                age: 28,
                gender: "female",
                location: "Barcelona",
                bio: "Hi, I'm Isabella! I enjoy traveling and learning new languages.",
                profileImageUrl: "https://cataas.com/cat/says/Isabella%20Martinez!"
            },
            {
                id: "11",
                name: "David Thompson",
                age: 33,
                gender: "male",
                location: "Sydney",
                bio: "Hello, I'm David! I'm a nature enthusiast and love going on hikes.",
                profileImageUrl: "https://cataas.com/cat/says/David%20Thompson!"
            },
            // Add more matches here...
        ]
    };


    const dummyChatMessages = [
        {
            id: "1",
            name: "John Doe",
            message: "Hello!",
            img: "https://cataas.com/cat/says/John%20Doe!"
        },
        {
            id: "2",
            name: "Jane Smith",
            message: "Hi John! How are you?",
            img: "https://cataas.com/cat/says/Jane%20Smith!"
        },
        // Add more chat messages here...
    ];


    return (
        <div className="dashboard">
            <MatchesDisplay matches={user.matches} setClickedUser={user}/>
            <div className="chat-display">
                {descendingOrderMessages && descendingOrderMessages.map((message, _index) => (
                    <div key={_index}>
                        <div className="chat-message-header">
                            <div className="img-container">
                                <img src={message.img} alt={message.name + ' profile'}/>
                            </div>
                            <p>{message.name}</p>
                        </div>
                        <p>{message.message}</p>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Chat;
