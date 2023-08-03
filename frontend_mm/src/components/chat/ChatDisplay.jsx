import React, {useEffect, useRef, useState} from "react";
import Chat from "./Chat.jsx";
import ChatInput from "./ChatInput.jsx";
import axios from "axios";
import "../../css/components/chat/ChatDisplay.css";

const ChatDisplay = ({ user, clickedUser }) => {
    const [messages, setMessages] = useState([]);
    const chatDisplayRef = useRef(null);

    useEffect(() => {
        if (user && clickedUser) {
            const fetchMessages = async () => {
                try {
                    const response = await axios.get(
                        `http://localhost:8000/messages`,
                        {
                            params: {
                                userId: user.id,
                                correspondingUserId: clickedUser.id,
                            },
                        }
                    );
                    setMessages(response.data);
                } catch (error) {
                    console.log(error);
                }
            };
            fetchMessages();
        }
    }, [user, clickedUser]);

    // Dummy messages for testing purposes
    const dummyMessages = [
        {
            id: "1",
            fromUserId: user.id,
            toUserId: clickedUser.id,
            message: "hey",
            timestamp: "2023-07-31T12:00:00.000Z",
        },
        {
            id: "2",
            fromUserId: clickedUser.id,
            toUserId: user.id,
            message: "Hello! How are you?",
            timestamp: "2023-07-31T12:05:00.000Z",
        },
        {
            id: "0",
            fromUserId: clickedUser.id,
            toUserId: user.id,
            message: "test",
            timestamp: "2023-07-31T12:05:30.000Z",
        },
        {
            id: "0",
            fromUserId: clickedUser.id,
            toUserId: user.id,
            message: "test2",
            timestamp: "2023-07-31T12:05:30.000Z",
        },
    ];

    return (
        <div className="chat-display" ref={chatDisplayRef}>
            <Chat
                messages={messages.length > 0 ? messages : dummyMessages}
                user={user}
                clickedUser={clickedUser}
            />
        </div>
    );
};

export default ChatDisplay;
