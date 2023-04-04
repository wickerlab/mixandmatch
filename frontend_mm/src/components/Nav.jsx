import whiteLogo from '../images/images.webp'
import colourLogo from '../images/images.png'

const Nav = ({minimal, setShowModal, showModal, setIsSignUp}) =>{

    const handleClick =() =>{
        setShowModal(true)
        setIsSignUp(false)
    }

    const authToken = true

    return(
        <nav>
            <div className="logo-container">
                <img className="logo" src ={minimal ? colourLogo : whiteLogo} />
            </div>

            {!authToken && !minimal && <button
                className="nav-button"
                onClick={handleClick}
                disabled={showModal}
            >Log in</button>}
        </nav>
    )
}

export default Nav