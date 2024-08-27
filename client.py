# ======================================================== 
# Léo BECHET - Summer 2024
# Part of a client-server template for communication
# between control station and equipment overseers.
# ======================================================== 

import socket
import json



def server_success(response_data):
    print("Server reported success.")

def server_fail(response_data):
    print('Server reported an error. {}'.format(response_data.get("error")))

def fail_connect():
    print("Failed to connect to the server or the server timed out.")





def send_data(json_data, host='127.0.0.1', port=65432, debug=False):
    """
    Sends a JSON object to the server, waits for a response, and closes the connection.
    Uses a \n as delimiter in packets to avoid hanging (NOT TESTED)

    
    :param json_data: The data to be sent as a JSON object.
    :param host: The server's hostname or IP address. Defaults to '127.0.0.1'.
    :param port: The server's port number. Defaults to 65432.
    """
    # TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect 
            client_socket.connect((host, port))
            print("Connected to server at"+str(host)+":"+str(port))

            # UTF-8 encode and send JSON data with a newline at the end
            message = json.dumps(json_data) + '\n'
            client_socket.sendall(message.encode('utf-8'))  # Send data to server
            if debug: print("JSON data sent to server:", json_data)

            # Set timeout for response
            client_socket.settimeout(5)  # 5 seconds timeout

            try:
                # Wait for response from the server
                response = client_socket.recv(1024)
                response_data = json.loads(response.decode('utf-8'))
                if debug: print("Response from server:", response_data)

                # Check status field and call the appropriate function
                if response_data.get("status") == "error":
                    server_fail(response_data)
                elif response_data.get("status") == "success":
                    server_success(response_data)

            except socket.timeout:
                if debug: print("No response received from server within 5 seconds.")
                fail_connect()

        except Exception as e:
            print("An error occurred:", e)
            fail_connect()

        finally:
            # Connection will be automatically closed
            print("Connection closed.")



# Example use
if __name__ == "__main__":
   data = {
       "command_id": "test_command",
       "param1": 100,
       "param2": "this is text",
       "param3": True,
       "param4": [1,2,3,4, "text in list"]
   }

   send_data(data, host='127.0.0.1', port=65432,)