import React, { useState, useEffect } from "react";
import Nav from "../components/Nav.jsx";
import "../css/pages/OnBoarding.css";
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from "axios";

const OnBoarding = () => {
    const degreeOptions = ["BACHELORS", "MASTERS", "DOCTORAL", "DIPLOMA"];
    const salaryOptions = ["Under $15,000", "$15,000 - $30,000", "$30,000 - $50,000", "Above $50,000"];

    const salaryMapping = {
        "Under $15,000": "UNDER15",
        "$15,000 - $30,000": "15TO30",
        "$30,000 - $50,000": "30TO50",
        "Above $50,000": "OVER50"
    };

    const navigate = useNavigate();
    const location = useLocation();
    const userId = location.state ? location.state.userId : null;

    const [formData, setFormData] = useState({
        user_id: '',
        first_name: '',
        age: '',
        gender_identity: '',
        degree: '',
        salary: '',
        url: '',
        bio: '',
    });

    const [ageValidation, setAgeValidation] = useState({
        ageValid: true,
        ageErrorMessage: ""
    });

    const validateAge = (age) => {
        if (age < 18 || age > 100) {
            setAgeValidation({
                ageValid: false,
                ageErrorMessage: "Age must be between 18 and 100"
            });
        } else {
            setAgeValidation({
                ageValid: true,
                ageErrorMessage: ""
            });
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formDataToSend = new FormData();
        formDataToSend.append('age', formData.age);
        // if (formData.gender_identity === 'man') {
        //     formDataToSend.append('gender', 'MALE');
        // }  else {
        //     formDataToSend.append('gender', "FEMALE");
        // }
        formDataToSend.append('gender', formData.gender_identity);
        formDataToSend.append('career', formData.salary);
        formDataToSend.append('education', formData.degree);
        formDataToSend.append('photo', formData.url);
        formDataToSend.append('bio', formData.bio);

        // Make the POST request
        try {
            if (!userId) {
                console.error('User ID not found');
                return;
            }
            console.log(formDataToSend);
             const response = await axios.post(`http://127.0.0.1:5000/onboarding/${userId}`, formDataToSend,{
                 headers: {
                     'Content-Type': 'multipart/form-data'
                 },
                 withCredentials: true
            });

            const success = response.status === 200;
            if (success) {
                alert("Successfully created account! Please log in")
                navigate('/');
            } else {
                // Handle error
                console.error('Error submitting form data');
            }
        } catch (error) {
            console.error('Error submitting form data', error);
        }
    }

    const handleChange = (e) => {
        const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        const name = e.target.name;

        if (name === 'age') {
            const age = parseInt(value, 10);
            validateAge(age);
        }

        if (name === 'salary') {
            // Map the selected salary option to the desired format
            const mappedSalary = salaryMapping[value] || '';
            setFormData((prevState) => ({
                ...prevState,
                [name]: mappedSalary
            }));
        } else {
            setFormData((prevState) => ({
                ...prevState,
                [name]: value
            }));
        }
        console.log(formData)
    }


    return (<>
        <Nav
            minimal={true}
            setShowModal={() => {
            }}
            showModal={false}
        />
        <div className="onboarding">
            <h2>Create Account</h2>
            <form onSubmit={handleSubmit}>
                <section>
                    <label htmlFor="first_name">First Name</label>
                    <input
                        id="first_name"
                        type="text"
                        name="first_name"
                        placeholder="First Name"
                        required={true}
                        value={formData.first_name}
                        onChange={handleChange}/>

                    <label htmlFor="Age">Age</label>
                    {!ageValidation.ageValid && <p className="error-message">{ageValidation.ageErrorMessage}</p>}
                    <input
                        id="age"
                        type="number"
                        name="age"
                        placeholder="Age"
                        required={true}
                        value={formData.age}
                        onChange={handleChange}
                    />

                    <label>Gender</label>
                    <div className="multiple-input-container">
                        <input
                            id="man-gender-identity"
                            type="radio"
                            name="gender_identity"
                            value={"MALE"}
                            onChange={handleChange}
                            checked={formData.gender_identity === 'MALE'}/>
                        <label htmlFor="man-gender-identity">Man</label>

                        <input
                            id="woman-gender-identity"
                            type="radio"
                            name="gender_identity"
                            value={"FEMALE"}
                            onChange={handleChange}
                            checked={formData.gender_identity === 'FEMALE'}/>
                        <label htmlFor="woman-gender-identity">Woman</label>

                    </div>

                    <label htmlFor="degree">Degree</label>
                    <select
                        id="degree"
                        name="degree"
                        required={true}
                        value={formData.degree}
                        onChange={handleChange}
                    >
                        <option value="">Select Degree</option>
                        {degreeOptions.map((option, index) => (
                            <option key={index} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>

                    <label htmlFor="salary">Salary</label>
                    <select
                        id="salary"
                        name="salary"
                        required={true}
                        value={formData.salary in salaryMapping ? formData.salary : Object.keys(salaryMapping).find(key => salaryMapping[key] === formData.salary)}
                        onChange={handleChange}
                    >
                        <option value="">Select Salary Range</option>
                        {salaryOptions.map((option, index) => (
                            <option key={index} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                    <label htmlFor="bio">About me</label>
                    <input
                        id="bio"
                        type="text"
                        name="bio"
                        required={true}
                        placeholder="I like long walks.."
                        value={formData.bio}
                        onChange={handleChange}
                    />
                    <input type="submit"/>
                </section>

                <section>
                    <label htmlFor="profile_picture">Profile Picture</label>
                    <input
                        type="url"
                        name="url"
                        id="url"
                        onChange={handleChange}
                        required={true}
                    />
                    <p className="message">Upload a photo of yourself with a url link</p>
                    <div className="photo-container">
                        <img src={formData.url}/>
                    </div>
                </section>
            </form>
        </div>
    </>)
}

export default OnBoarding