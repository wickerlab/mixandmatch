import whiteLogo from '../images/logo.png'
import colourLogo from '../images/logo.png'
import '../css/components/Navbar.css'

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