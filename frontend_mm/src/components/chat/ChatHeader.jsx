import { useCookies } from 'react-cookie'
import '../../css/components/chat/ChatHeader.css'
import '../../css/pages/Dashboard.css'

const ChatHeader = ({ clickedUser }) => {
    const [ cookies, setCookie, removeCookie ] = useCookies(['user'])



    return (
        <div className="chat-container-header">
            <div className="profile">
                <h3 className="info-title">{clickedUser.username}</h3>
            </div>
        </div>
    )
}

export default ChatHeader