# Mix and Match - Research Code Repository

Welcome to the Mix and Match research code repository. This repository contains the codebase for the Mix and Match platform, which explores the interplay between user behavior and recommendation algorithms in the context of online dating applications. Below, you'll find an overview of the repository structure and key components.

This branch has been heavily edited by the Unsupervised Learners Capstone Team (2024 Sem 2) (Team 36)

## Repository Structure

The repository is organized into the following key components:

1. **API Code (Flask):**
   - The main Flask application handles user authentication, user profiles, matches, and recommendation algorithms.
   - Includes user and match-related endpoints.

2. **Frontend Code (Vite & React):**
   - The Mix and Match dating platform's user interface and client-side code.
   - Built using Vite and React for a responsive and interactive user experience.

3. **Dependency Configuration (package.json):**
   - Contains the project dependencies, including React libraries, Axios for API requests, and others.

## Getting Started


Please ensure you have MySQL set up before you run these scripts
Read `SQL.md` before proceeding

### Scripts

Use the script to set up:
windows:
`& "C:\Program Files\Git\bin\bash.exe" ./setup.sh`

mac:
`sh ./setup.sh`

Use the script to run:
windows:
`& "C:\Program Files\Git\bin\bash.exe" ./run.sh`

mac:
`sh ./run.sh`


-----------------------------------------

# Setting up local dev
1. ensure venv is set up before installing requirements.txt, so no conflicts occur
2. ensure SQL is running (go to services and start it)
3. set up local SQL mixnmatch database and user access to that database (make user, password and database all called "mixnmatch")
4. source the SQL dump file into your local mixnmatch database

# Note
For chat to work, both sides need to match first and chat.py needs to be running

# Running local dev
1. start venv 
   1. windows: `.venv\Scripts\activate`
   2. mac: `source venv/bin/activate`
2. run `npm run start:frontend` in frontend directory in a console
3. run `python app.py` in backend in a new console
4. run `python chat.py` in backend in a new console
5.  if persistent 401 errors, go to application tab in developer tools (under same tab as console), go to cookies, and delete all cookies, then try again. There appears to be a problem with duplicate cookies


-----------------------------------------
   

The Mix and Match platform will be accessible at `http://localhost:5173`, and the API endpoints can be accessed locally at `http://localhost:5000` and WebSocket at `http://localhost:8765`.



## Key Endpoints

- **User Endpoints:**
  - `GET /users/<int:user_id>`: Get user information by user ID.
  - `PUT /users/<int:user_id>`: Update user information.
  - `POST /login`: User login.
  - `GET /logout`: User logout.
  - `POST /signup`: User registration.
  - `POST /onboarding/<int:user_id>`: Complete user onboarding.
  - `GET /chat`: Get user's chat conversations.
  - `POST /chat-history`: Get chat history.
  - `POST /reset-chat/<int:user_id>`: Resets the users chat history
  - `POST /delete-user/<int:user_id>`: Removes user from mixnmatch db

- **Match Endpoints:**
  - `POST /matches/<int:other_user_id>`: Match with another user.
  - `GET /matches`: Get recommended users for matchmaking.
  - `POST /reset-matches/<int:user_id>`: Resets users match history in db
