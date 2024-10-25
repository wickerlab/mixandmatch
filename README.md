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


Please ensure you have MySQL set up before you run these scripts \
Read `SQL.md` before proceeding \
You can setup either with the [Setup Script](#setup-script) or [manually](#manual-setup-no-scripts)

### Setup Script

Run the command below to use a script to create a virtual environment and install dependencies 
#### Windows:
```bash
& "C:\Program Files\Git\bin\bash.exe" ./setup.sh
```

#### Mac:
```bash
sh ./setup.sh
```


### Manual Setup (no scripts)
If the scripts do not work, do the following steps from the root folder to create a virtual environment and install dependencies:
#### Windows Setup
```bash
# Backend setup
cd backend_mm
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt 
cd ..

# Frontend setup
cd frontend_mm
npm i    

```
#### Mac Setup
```bash
# Backend setup
cd backend_mm
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend setup
cd frontend_mm
npm i
```


-----------------------------------------

## MySQL setup
After completing the above setup (`SQL.md`, installing frontend and backend dependencies), ensure the following before continuing:
1. Ensure MySQL is running (go to services and start it)
3. Set up local SQL mixnmatch database and user access to that database (make user, password and database all called "mixnmatch"), as in `SQL.md`
4. source the SQL dump file (`./backend_mm/mysql_database/dump.sql`) into your local mixnmatch database to set it up

### Note
For chat to work, both sides need to match first and chat.py needs to be running

# Running local dev
Once you have setup with either the scripts or manual setup above, either use the [Run Script](#run-script) or [manually run](#manual-run-no-scripts) MixnMatch.
### Run Script

#### Windows:
```bash
& "C:\Program Files\Git\bin\bash.exe" ./run.sh
```

#### Mac:
```bash
sh ./run.sh
```

### Manual Run (no scripts)

1. Start venv from `./backend_mm`:
   1. Windows: `.venv\Scripts\activate`
   2. Mac: `source .venv/bin/activate`
2. Run `python app.py` in `./backend_mm` in a new console
3. Run `python chat.py` in `./backend_mm` in a new console
4. Run  `npm run start:frontend` in `./frontend_mm` directory in a console
5.  If there are persistent 401 errors, go to application tab in developer tools (under same tab as console), go to cookies, and delete all cookies, then try again. There appears to be a problem with duplicate cookies


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