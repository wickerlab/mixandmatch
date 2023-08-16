import {useState} from "react";
import axios from 'axios';
import {useNavigate} from "react-router-dom";
import { useCookies } from 'react-cookie';
import "../css/components/AuthModal.css";

const AuthModal = ({setShowModal, isSignUp}) =>{
    const [email, setEmail] = useState(null)
    const [username, setUsername] = useState(null)
    const [password, setPassword] = useState(null)
    const [confirmPassword, setConfirmPassword] = useState(null)
    const [error, setError] = useState(null)
    const [cookie,setCookie, removeCookie] = useCookies('user')
    const [isSignUpMode, setIsSignUpMode] = useState(isSignUp); // Track the mode


    let navigate = useNavigate()


    const handleClick =()=>{
        setShowModal(false)
    }

    const handleTest =()=>{
        fetchMatches();
    }

    async function fetchMatches() {
        try {

            // const authToken = ''; // Replace with your actual authentication token
            const axiosWithCookies = axios.create({
                withCredentials: true
            });

            const response = await axiosWithCookies.get("http://127.0.0.1:5000/matches", {
                headers:{
                }

            });

            console.log(response);

            console.log(response.data.recommended_users);

        } catch (error) {
            console.error("Error fetching matches:", error);
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isSignUpMode && (password !== confirmPassword)) {
                setError('Password not matching');
                return;
            }

            const formData = new FormData();

            if (isSignUpMode && (password.length < 8)) {
                formData.append('email', email);
                formData.append('username', username);
                formData.append('password', password);

                const response = await axios.post('http://127.0.0.1:5000/signup', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    withCredentials: true
                });

                console.log(response.headers.get("Set-Cookie"));

                // setCookie('Email', response.data.email);
                // setCookie('userId', response.data.userId);
                // setCookie('AuthToken', response.data.token);

                const success = response.status === 201;
                if (success) {
                    navigate('/onboarding');
                }
            }
            else if(!isSignUpMode){
                formData.append('email', email);
                formData.append('password', password);

                const response = await axios.post('http://127.0.0.1:5000/login', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    withCredentials: true
                });


                const success = response.status === 200;
                if (success) {
                    console.log(response.headers.get("Set-Cookie"));
                    // navigate('/dashboard');
                }
            }

        } catch (error) {
            console.log(error);
        }
    };

    const handleModeToggle = () => {
        setError(null); // Clear any previous error messages
        setIsSignUpMode((prevMode) => !prevMode); // Toggle the mode
    };


    return(
        <div className="auth-modal">
            <div className="close-icon" onClick={handleClick}>x</div>
            <h2>{isSignUpMode ?'CREATE ACCOUNT':'LOG IN'}</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    id="email"
                    name="email"
                    placeholder="email"
                    required={true}
                    onChange={e => setEmail(e.target.value)}
                />
                { isSignUpMode && <input
                    type="username"
                    id="username"
                    id="username"
                    name="username"
                    placeholder="username"
                    required={true}
                    onChange={e => setUsername(e.target.value)}
                />}
                <input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="password"
                    required={true}
                    onChange={e => setPassword(e.target.value)}
                />
                {isSignUpMode && <input
                    type="password"
                    id="password-check"
                    name="password-check"
                    placeholder="confirm password"
                    required={true}
                    onChange={e => setConfirmPassword(e.target.value)}
                />}
                <input className="secondary-button" type="submit"/>
                <button className="secondary-button" type="button" onClick={handleModeToggle}>
                    {isSignUpMode ? 'Log In' : 'Sign Up'}
                </button>
                <button className="secondary-button" type="button" onClick={handleTest}>
                    Test
                </button>
                <p>{error}</p>
            </form>
        </div>
    )
}

export default AuthModal