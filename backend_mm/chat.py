import asyncio
import websockets
import json
import mysql.connector

# MySQL database configuration
db_config = {
    'user': 'root',  # Change to 'admin1' for deployment
    'password': 'mixnmatchmysql',
    'host': 'localhost',
    'database': 'mixnmatch'
}


# Function to retrieve all chat history between two users
def get_chat_history(sender_id, receiver_id):
    cnx = mysql.connector.connect(**db_config)
    try:
        with cnx.cursor() as cursor:
            query = "SELECT sender_id, receiver_id, message, update_time FROM message WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY update_time ASC"
            cursor.execute(query, (sender_id, receiver_id, receiver_id, sender_id))
            history = []
            for row in cursor.fetchall():
                history.append({
                    'sender_id': row[0],
                    'receiver_id': row[1],
                    'message': row[2],
                    'update_time': row[3].isoformat()  # Convert timestamp to ISO format
                })
            return history
    finally:
        cnx.close()


async def chat_server(websocket, path):
    # Establish a connection to the MySQL database
    cnx = mysql.connector.connect(**db_config)

    try:
        async for message in websocket:
            # Assuming the message is received in JSON format
            data = json.loads(message)
            sender_id = data.get('sender_id')
            receiver_id = data.get('receiver_id')
            chat_message = data.get('message')

            # Log incoming message
            print(f"Received message from {sender_id} to {receiver_id}: {chat_message}")

            # Save the message to the database
            with cnx.cursor() as cursor:
                query = "INSERT INTO message (sender_id, receiver_id, message, update_time) VALUES (%s, %s, %s, NOW())"
                cursor.execute(query, (sender_id, receiver_id, chat_message))
                cnx.commit()

            # Send the message to the other user
            # You'll need to implement logic to determine the recipient and send the message

    finally:
        cnx.close()


# Start the WebSocket server on a specific port (e.g., 8765)
start_server = websockets.serve(chat_server, 'localhost', 8765)

# Run the WebSocket server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
