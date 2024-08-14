import asyncio
import websockets
import json
import mysql.connector
from urllib.parse import urlparse, parse_qs
import openai

# Your OpenAI API key
OPENAI_API_KEY = 'key'

# Initialize the OpenAI API client
openai.api_key = OPENAI_API_KEY

# MySQL database configuration
db_config = {
    'user': 'mixnmatch',  # Change to 'admin1' for deployment
    'password': 'mixnmatch',
    'host': 'localhost',
    'database': 'mixnmatch'
}
# Maintain a dictionary to store WebSocket connections for each user
connected_clients = {}


def insert_message(sender_id, receiver_id, message, status, cnx):
    with cnx.cursor() as cursor:
        query = ("INSERT INTO message (sender_id, receiver_id, message, update_time, status)"
                 " VALUES (%s, %s, %s, NOW(), %s)")
        cursor.execute(query, (sender_id, receiver_id, message, status))
        cnx.commit()


async def chat_server(websocket, path):
    print(f"WebSocket client connected: {websocket.remote_address}")

    # Extract query parameters from the URL
    query_params = parse_qs(urlparse(path).query)
    sender_id = query_params.get('sender_id', [None])[0]

    # Establish a connection to the MySQL database
    cnx = mysql.connector.connect(**db_config)

    try:
        # Receive a message from the WebSocket client
        if sender_id:
            sender_id_str = str(sender_id)  # Convert sender_id to a string
            connected_clients[sender_id_str] = websocket
            print(f"Added WebSocket connection for sender_id {sender_id_str}")
            print(connected_clients)

        # Receive a message from the WebSocket client
        async for message in websocket:
            data = json.loads(message)
            sender_id = data.get('sender_id')
            receiver_id = data.get('receiver_id')
            chat_message = data.get('message')
            read_status = data.get('status')

            # Log incoming message
            print(f"Received message from {sender_id} to {receiver_id}: {chat_message}, {read_status}")

            # Save the message to the database
            with cnx.cursor() as cursor:
                query = ("INSERT INTO message (sender_id, receiver_id, message, update_time, status) "
                         "VALUES (%s, %s, %s, NOW(), %s)")
                cursor.execute(query, (sender_id, receiver_id, chat_message, read_status))
                cnx.commit()
                print("message saved")

            # Add the WebSocket connection to connected_clients if not already added
            if str(sender_id) not in connected_clients:
                connected_clients[str(sender_id)] = websocket

            # Print connected_clients
            print(connected_clients)

            # Check if the recipient is a bot
            with cnx.cursor() as cursor:
                query = "SELECT * FROM user_category WHERE user_id = %s"
                cursor.execute(query, (receiver_id,))
                result = cursor.fetchone()
                print(result)
                if result and result[1] == 'BOT':
                    user_id = str(sender_id)  # Convert sender_id to a string

                    query = "SELECT * FROM user WHERE id = %s"
                    cursor.execute(query, (user_id,))
                    user_attributes = cursor.fetchone()

                    chat_history_query = ("SELECT * FROM message WHERE (sender_id = %s AND receiver_id = %s) OR ("
                                          "receiver_id = %s AND sender_id = %s)")
                    cursor.execute(chat_history_query, (sender_id, receiver_id, sender_id, receiver_id))
                    chat_history = cursor.fetchall()
                    print(chat_history)

                    if user_attributes:
                        user_name = user_attributes[2]
                        user_age = user_attributes[4]
                        user_gender = user_attributes[5]
                        user_education = user_attributes[7]

                        # Generate a response using OpenAI GPT-3.5-turbo
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": f"IMPORTANT MESSAGE: Pretend to have normal "
                                                              f"conversation to me like others dating app user. "
                                                              f"Here are some roles that you need to follow: "
                                                              f"You are a user in an dating app called mix and match "
                                                              f"provide continuous conversation to the user base on the "
                                                              f"chat history you and the user had {chat_history}."
                                                              
                                                              f"Here is your basic information as a dating app user:"
                                                              f"for you to role play: "
                                                              f"The name of the person you are going to role play is {user_name}"
                                                              f"The age of the person you are going to role play is {user_age},"
                                                              f"The gender of the person you are going to role play is {user_gender} and "
                                                              f"The education of the person you are going to role play is{user_education}."},

                                {"role": "user", "content": chat_message}
                            ]
                        )

                        # Extract the generated message from the response
                        bot_response = response.choices[0].message["content"].strip()
                        print(bot_response)

                        # Create a message to send
                        bot_message = {
                            "sender_id": receiver_id,
                            "receiver_id": sender_id,
                            "message": bot_response,
                            "status": "unread"
                        }

                        insert_message(bot_message["sender_id"], bot_message["receiver_id"], bot_message["message"],
                                       bot_message["status"], cnx)

                        # Send the message as JSON
                        await websocket.send(json.dumps(bot_message))
                else:
                    # Send the message to the other user (recipient)
                    recipient_ws = connected_clients.get(str(receiver_id))
                    if recipient_ws:
                        await recipient_ws.send(message)

    except websockets.exceptions.ConnectionClosedError:
        pass  # Handle disconnection

    finally:
        # Remove the WebSocket connection from connected_clients when disconnected
        if sender_id in connected_clients:
            del connected_clients[sender_id]

        cnx.close()
        print(f"WebSocket client disconnected: {websocket.remote_address}")


# Start the WebSocket server on a specific port (e.g., 8765)
start_server = websockets.serve(chat_server, 'localhost', 8765)

# Run the WebSocket server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
