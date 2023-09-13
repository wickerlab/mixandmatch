import React, { useEffect, useRef, useState } from "react";
import Chat from "./Chat.jsx";
import ChatInput from "./ChatInput.jsx";
import "../../css/components/chat/ChatDisplay.css";
import axios from "axios";

const ChatDisplay = ({ currentUserId, clickedUser }) => {
    const [messages, setMessages] = useState([]);
    const chatDisplayRef = useRef(null);
    const ws = useRef(null);

    useEffect(() => {
        getChatHistory().then(r => console.log("chat history", r)).catch(e => console.log("error", e));
        setupWebSocket();

        return () => {
            // Clean up WebSocket connection on component unmount
            if (ws.current) {
                ws.current.close();
            }
        };
    }, [currentUserId, clickedUser]);

    const getChatHistory = async () => {
        // Create form data
        const formData = new FormData();
        console.log("currentUserId and reciver id", currentUserId, clickedUser.user_id);
        formData.append("sender_id", currentUserId);
        formData.append("receiver_id", clickedUser.user_id);

        try {
            const response = await axios.post('http://127.0.0.1:5000/chat-history', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                withCredentials: true
            });

            if (response.status === 200) {
                const responseBody = response.data.chat_history; // Assuming the response is JSON
                console.log(responseBody);
                setMessages(responseBody);
            }
        } catch (error) {
            console.error("Error fetching chat history:", error);
        }
    };

    const setupWebSocket = () => {
        ws.current = new WebSocket(`ws://localhost:8765`);

        ws.current.onopen = () => {
            console.log("WebSocket connection opened");
        };

        ws.current.onmessage = (event) => {
            // Handle incoming WebSocket messages
            const data = JSON.parse(event.data);
            console.log("prevMessages", messages);
            console.log("Message from server: ", data);
            setMessages((prevMessages) => [...prevMessages, data]);
        };
    };

    return (
        <div className="chat-display" ref={chatDisplayRef}>
            <Chat
                messages={messages}
                currentUserId={currentUserId}
                clickedUser={clickedUser}
            />
        </div>
    );
};

export default ChatDisplay;
