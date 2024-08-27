# ======================================================== 
# Léo BECHET - Summer 2024
# Part of a client-server template for communication
# between control station and equipment overseers.
# ======================================================== 

import socket
import json


def interact(data):
    # Example of what to do with json data :

    if data["command_id"] == "test_command":
        print("Received data is the following : ",data)

        print("Data of param1 : ", data["param1"])
        print("Data of param2 : ", data["param2"])
        print("Data of param3 : ", data["param3"])
        print("Data of param4 : ", data["param4"])






def start_server(host='127.0.0.1', port=65432, debug=False):
    #    Uses a \n as delimiter in packets to avoid hanging (NOT TESTED)


    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to a public host and a port
        server_socket.bind((host, port))
        # Start listening for incoming connections
        server_socket.listen()
        print(f"Server started and listening on {host}:{port}")

        while True:
            # Wait for a connection
            client_socket, client_address = server_socket.accept()
            with client_socket:
                if debug: print(f"Connected by {client_address}")
                buffer = b''

                while True:
                    chunk = client_socket.recv(1024)
                    if not chunk:
                        break
                    buffer += chunk
                    
                    # Check if a full message is received (delimited by newline)
                    if b'\n' in buffer:
                        data, buffer = buffer.split(b'\n', 1)  # Split by delimiter and keep the rest
                        
                        # Decode the data and parse JSON
                        try:
                            json_data = json.loads(data.decode('utf-8'))
                            if debug: print("Received JSON data:", json_data)

                            # Interact with DDS
                            try:
                                interact(json_data)
                                # Update client with success 
                                response = json.dumps({"status": "success"}) + '\n'
                                client_socket.sendall(response.encode('utf-8'))

                            except Exception as e:
                                if debug: print(e)
                                response = json.dumps({"status": "failed", "error": str(e)}) + '\n'
                                client_socket.sendall(response.encode('utf-8'))

                        except json.JSONDecodeError as e:
                            print("Failed to decode JSON:", e)
                            # Update client with failure 
                            response = json.dumps({"status": "failed", "error": str(e)}) + '\n'
                            client_socket.sendall(response.encode('utf-8'))

                        # Break out after processing one message
                        break

                # Close the connection after receiving the message
                if debug: print(f"Closing connection with {client_address}")

if __name__ == "__main__":
    start_server(host="127.0.0.1", port=65432)