import React, { useEffect, useRef, useState } from "react";
import ChatHeader from "./ChatHeader.jsx";
import ChatDisplay from "./ChatDisplay.jsx";
import ChatInput from "./ChatInput.jsx";
import axios from "axios";
import { w3cwebsocket as W3CWebSocket } from "websocket"; // Import the WebSocket library
import "../../css/components/chat/ChatContainer.css";

const ChatContainer = ({ currentUserId, clickedUser }) => {
    const [messages, setMessages] = useState([]);
    const ws = useRef(null);

    useEffect(() => {
        getChatHistory().then(r => console.log("chat history", r)).catch(e => console.log("error", e));
        setupWebSocket();
        return () => {
            // Clean up WebSocket connection on component unmount
            if (ws.current) {
                console.log("closing websocket")
                ws.current.close();
            }
        };
    }, [currentUserId, clickedUser]);

    const getChatHistory = async () => {
        // Create form data
        const formData = new FormData();
        console.log("currentUserId and receiver id", currentUserId, clickedUser.user_id);
        formData.append("current_user_id", currentUserId);
        formData.append("clicked_user_id", clickedUser.user_id);

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
        // Create a WebSocket client and connect to your WebSocket server
        ws.current = new W3CWebSocket(`ws://localhost:8765?sender_id=${currentUserId}`); // Include sender_id in the URL

        ws.current.onopen = () => {
            console.log("WebSocket Client Connected");
            // WebSocket connection is open, you can handle any initialization here
        };

        ws.current.onclose = () => {
            // Handle the WebSocket connection closing, if needed
        };

        ws.current.onerror = (error) => {
            console.error("WebSocket Error: ", error);
        };

        ws.current.onmessage = (message) => {
            // Handle incoming WebSocket messages
            const dataFromServer = JSON.parse(message.data);
            console.log("Message from server in chat container: ", dataFromServer);

            if (dataFromServer.sender_id === clickedUser.user_id) {
                // If the sender_id matches the currentUserId, update the chat
                setMessages(prevMessages => [...prevMessages, dataFromServer]);
                // change the message status to read

            } else {
                // If sender_id doesn't match, trigger an alert
                console.log("dataFromServer.sender_id", dataFromServer.sender_id);
                console.log("clickedUser.id", clickedUser.user_id);
                alert("You have an unread message.");
            }
        };
    };

    return (
        <div className="chat-container">
            <ChatHeader clickedUser={clickedUser} />
            {clickedUser ? (
                <ChatDisplay currentUserId={currentUserId} clickedUser={clickedUser} messages={messages} />
            ) : (
                <p>Please select a user</p>
            )}
            <ChatInput currentUserId={currentUserId} clickedUser={clickedUser} setMessages={setMessages} ws={ws}/>
        </div>
    );
};

export default ChatContainer;
