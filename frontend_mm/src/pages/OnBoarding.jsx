import {useState} from "react";
import Nav from "../components/Nav.jsx";
import "../css/pages/OnBoarding.css";

const OnBoarding = () => {

    const degreeOptions = ["BACHELORS", "MASTERS", "DOCTORAL", "DIPLOMA"];
    const salaryOptions = ["Under $15,000", "$15,000 - $30,000", "$30,000 - $50,000", "Above $50,000"];

    const [formData, setFormData] = useState({
        user_id: '',
        first_name: '',
        dob_day: '',
        dob_month: '',
        dob_year: '',
        gender_identity: "woman",
        gender_interest: 'man',
        degree: '',
        salary:'',
        url: '',
        about: '',
        matches: []
    })

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Calculate age from date of birth
        const currentDate = new Date();
        const birthDate = new Date(`${formData.dob_year}-${formData.dob_month}-${formData.dob_day}`);
        const age = currentDate.getFullYear() - birthDate.getFullYear();

        // Create a new FormData object
        const formDataToSend = new FormData();
        formDataToSend.append('age', age.toString());
        formDataToSend.append('gender', formData.gender_identity);
        formDataToSend.append('career', formData.salary);
        formDataToSend.append('education', formData.degree);
        console.log(formDataToSend);

        // Make the POST request
        // TODO get user id
        try {
            const response = await fetch('http://127.0.0.1:5000/onboarding/40', {
                method: 'PUT',
                body: formDataToSend,
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.ok) {
                // Redirect to a success page or another route
                history.push('/dashboard');
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

        setFormData((prevState) => ({
            ...prevState,
            [name]: value
        }));
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
                        placeholder="first_name"
                        required={true}
                        value={formData.first_name}
                        onChange={handleChange}/>

                    <label>Birthday</label>
                    <div className="multiple-input-container">
                        <input
                            id="dob_day"
                            type="number"
                            name="dob_day"
                            placeholder="DD"
                            required={true}
                            value={formData.dob_day}
                            onChange={handleChange}/>

                        <input
                            id="dob_month"
                            type="number"
                            name="dob_month"
                            placeholder="MM"
                            required={true}
                            value={formData.dob_month}
                            onChange={handleChange}/>

                        <input
                            id="dob_year"
                            type="number"
                            name="dob_year"
                            placeholder="YY"
                            required={true}
                            value={formData.dob_year}
                            onChange={handleChange}/>
                    </div>

                    <label>Gender</label>
                    <div className="multiple-input-container">
                        <input
                            id="man-gender-identity"
                            type="radio"
                            name="gender_identity"
                            value={"man"}
                            onChange={handleChange}
                            checked={formData.gender_identity === 'man'}/>
                        <label htmlFor="man-gender-identity">Man</label>

                        <input
                            id="woman-gender-identity"
                            type="radio"
                            name="gender_identity"
                            value={"woman"}
                            onChange={handleChange}
                            checked={formData.gender_identity === 'woman'}/>
                        <label htmlFor="woman-gender-identity">Woman</label>

                        <input
                            id="more-gender-identity"
                            type="radio"
                            name="gender_identity"
                            value={"more"}
                            onChange={handleChange}
                            checked={formData.gender_identity === 'more'}/>
                        <label htmlFor="more-gender-identity">More</label>
                    </div>

                    <label>Show Me</label>
                    <div className="multiple-input-container">
                        <input
                            id="man-gender-interest"
                            type="radio"
                            name="gender_interest"
                            value={"man"}
                            onChange={handleChange}
                            checked={formData.gender_interest === 'man'}/>
                        <label htmlFor="man-gender-interest">Man</label>

                        <input
                            id="woman-gender-interest"
                            type="radio"
                            name="gender_interest"
                            value={"woman"}
                            onChange={handleChange}
                            checked={formData.gender_interest === 'woman'}/>
                        <label htmlFor="woman-gender-interest">Woman</label>

                        <input
                            id="everyone-gender-interest"
                            type="radio"
                            name="gender_interest"
                            value={"everyone"}
                            onChange={handleChange}
                            checked={formData.gender_interest === 'everyone'}/>
                        <label htmlFor="everyone-gender-interest">Everyone</label>
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
                        value={formData.salary}
                        onChange={handleChange}
                    >
                        <option value="">Select Salary Range</option>
                        {salaryOptions.map((option, index) => (
                            <option key={index} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                    <label htmlFor="about">About me</label>
                    <input
                        id="about"
                        type="text"
                        name="about"
                        required={true}
                        placeholder="I like long walks.."
                        value={formData.about}
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
                    <div className="photo-container">
                        <img src={formData.url} alt="profile pic preview"/>
                    </div>
                </section>
            </form>
        </div>
    </>)
}

export default OnBoarding