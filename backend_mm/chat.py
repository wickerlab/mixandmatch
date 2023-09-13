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
# Maintain a dictionary to store WebSocket connections for each user
connected_clients = {}


async def chat_server(websocket, path):
    print(f"WebSocket client connected: {websocket.remote_address}")

    # Establish a connection to the MySQL database
    cnx = mysql.connector.connect(**db_config)

    try:
        # Receive a message from the WebSocket client
        async for message in websocket:
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

            # Add the WebSocket connection to connected_clients if not already added
            if sender_id not in connected_clients:
                connected_clients[sender_id] = websocket

            # Print connected_clients
            print(connected_clients)

            # Send the message to the other user (recipient)
            recipient_ws = connected_clients.get(receiver_id)
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
