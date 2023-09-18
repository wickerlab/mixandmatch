import asyncio
import websockets
import json
import mysql.connector
from urllib.parse import urlparse, parse_qs

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
                query = "INSERT INTO message (sender_id, receiver_id, message, update_time, status) VALUES (%s, %s, %s, NOW(), %s)"
                cursor.execute(query, (sender_id, receiver_id, chat_message, read_status))
                cnx.commit()

            # Add the WebSocket connection to connected_clients if not already added
            if str(sender_id) not in connected_clients:
                connected_clients[str(sender_id)] = websocket

            # Print connected_clients
            print(connected_clients)

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
