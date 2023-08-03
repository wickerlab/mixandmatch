import MatchesDisplay from "../components/MatchesDisplay.jsx";
import React, {useState} from "react";
import ChatContainer from "../components/chat/ChatContainer.jsx";

const Chatting = ({ descendingOrderMessages }) => {

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
            {
                id: "4",
                name: "Emma Thompson",
                age: 27,
                gender: "female",
                location: "New York",
                bio: "Hi, I'm Emma! I enjoy painting and playing the piano.",
                profileImageUrl: "https://cataas.com/cat/says/Emma%20Thompson!"
            }

        ]
    };

    const [clickedUser, setClickedUser] = useState(null);

    return (
        <div className="dashboard">
            <MatchesDisplay
                matches={user.matches}
                setClickedUser={setClickedUser}
            />
            <ChatContainer user={user} clickedUser={clickedUser} setClickedUser={setClickedUser}/>
        </div>
    );
}

export default Chatting;
