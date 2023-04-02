import ChatHeader from "./ChatHeader.jsx";
import MatchesDisplay from "./MatchesDisplay.jsx";
import ChatDisplay from "./ChatDisplay.jsx";

const ChatContainer = () =>{
    return <div className="chat-container">
        <ChatHeader/>

        <div>
            <button className="option">Matches</button>
            <button className="option">Chat</button>
        </div>

        <MatchesDisplay/>

        <ChatDisplay/>

    </div>
}

export default ChatContainer