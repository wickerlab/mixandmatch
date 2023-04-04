import TinderCard from 'react-tinder-card'
import {useState} from "react";
import ChatContainer from '../components/ChatContainer.jsx'

const Dashboard = () => {
    const characters = [
        {
            name: 'Richard Hendricks',
            url: 'https://cataas.com/cat/says/hello%20world!'
        },
        {
            name: 'Erlich Bachman',
            url: 'https://cataas.com/cat/says/hello%20world!'
        },
        {
            name: 'Monica Hall',
            url: 'https://cataas.com/cat/says/hello%20world!'
        },
        {
            name: 'Jared Dunn',
            url: 'https://cataas.com/cat/says/hello%20world!'
        },
        {
            name: 'Dinesh Chugtai',
            url: 'https://cataas.com/cat/says/hello%20world!'
        }
    ]
    const [lastDirection, setLastDirection] = useState()

    const swiped = (direction, nameToDelete) => {
        console.log('removing: ' + nameToDelete)
        setLastDirection(direction)
    }

    const outOfFrame = (name) => {
        console.log(name + ' left the screen!')
    }

    return (
        <div className="dashboard">
            <ChatContainer/>
            <div className="swipe-container">
                <div className="card-container">
                    {characters.map((character) =>
                        <TinderCard className='swipe' key={character.name}
                                    onSwipe={(dir) => swiped(dir, character.name)}
                                    onCardLeftScreen={() => outOfFrame(character.name)}>
                            <div style={{backgroundImage: 'url(' + character.url + ')'}} className='card'>
                                <h3>{character.name}</h3>
                            </div>
                        </TinderCard>)}
                        <div className="swipe-info" >
                            {lastDirection ? <p>You swiped{lastDirection}</p>: <p/>}
                        </div>

                </div>
            </div>
        </div>
    )
}

export default Dashboard