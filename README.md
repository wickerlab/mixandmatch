# Mix and Match - Research Code Repository

Welcome to the Mix and Match research code repository. This repository contains the codebase for the Mix and Match platform, which explores the interplay between user behavior and recommendation algorithms in the context of online dating applications. Below, you'll find an overview of the repository structure and key components.

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

To run the Mix and Match platform and explore the research code, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone <repository_url>
   cd path/to/mixandmatch
   ```

2. Install the required dependencies for the frontend:

   ```bash
   npm install
   ``

3. Start the frontend development server:

   ```bash
   npm run start:frontend
   ```

4. Install the required dependencies for the Flask API:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask API:

   ```bash
   python app.py
   ```
   
5. Run the WebSocket:

   ```bash
   python chat.py
   ```

   

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

- **Match Endpoints:**
  - `POST /matches/<int:other_user_id>`: Match with another user.
  - `GET /matches`: Get recommended users for matchmaking.
 
# Deployment

This project is manually deployed to an Ubuntu server, and the deployment process involves several steps to ensure that the latest codebase is updated, the front end is built, and the necessary services are restarted. Follow these steps for a successful deployment:

1. **Update the Codebase on the Ubuntu Machine:**
   - SSH into your Ubuntu server using your preferred method.
   - Navigate to the project directory on your server:

     ```bash
     cd /path/to/mixandmatch
     ```

   - Update the codebase from the remote repository:

     ```bash
     git pull
     ```

2. **Build the Frontend:**
   - If you have changed the frontend code, you may need to rebuild it.
   - Navigate to the frontend directory:

     ```bash
     cd /path/to/mixandmatch/frontend
     ```

   - Build the frontend:

     ```bash
     npm run build
     ```

3. **Restart Apache2:**
   - Apache2 is used for serving the web application. Restart it to apply any changes:

     ```bash
     sudo service apache2 restart
     ```

4. **Restart the PM2 Bot:**
   - The PM2 process manager is used to manage the backend services efficiently. Restart the bot service:

     ```bash
     pm2 restart bot
     ```

5. **Restart the PM2 Chat:**
   - Similarly, restart the chat service managed by PM2:

     ```bash
     pm2 restart chat
     ```

Your Mix and Match platform should now be updated and running with the latest code changes. Please ensure that you perform these deployment steps whenever you make updates or changes to the project to keep it up-to-date and running smoothly.


## Additional Information

- The project uses various API communication technologies, including React, Flask, and Axios. The Flask API provides user authentication, user profile management, and matchmaking capabilities.
- This codebase is a part of a research project focused on studying user behaviour and recommendation algorithms in online dating applications.

You can explore the code, make improvements, and contribute to the ongoing research project. If you have any questions or need assistance, please don't hesitate to contact the project team.

Thank you for being so interested in Mix and Match!
