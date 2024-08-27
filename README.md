# Client-Server template

The following is an explananation on how to use the client-server template provided. The template uses sockets (default python lib) to send JSON data between 2 computers. This is taken out of the DDS to ARTIQ link made during the summer 2024.

Successfully used alongside ARTIQ 5 integration.

## Server.py

Server.py contains the code to be run on the host machine. It stays on running and waits for data from the client.

### Doc

#### start_server
> Starts the server, infinite loop and always listening.
- **host='127.0.0.1'** : IP to on which the server is running, default to localhost for internal tests
- **port=65432** : Port on which the server is running, defaults to 65432, arbitrary, however avoid common ports and make sure it is not already in use.
- **debug=False** : If sets to *True*, prints debug messages, check code for more information.

**Usage example**
```PYTHON
if __name__ == "__main__":
    start_server(host="127.0.0.1", port=65432)
```

#### interact
> Called upon receiving data.
- **data** : JSON object already parsed.

To get parameters passed in the JSON object use the following : `data["parameter_name"]`.
Additional informations on JSONs can be found in the [Official Documentation](https://docs.python.org/fr/3/library/json.html).

**Usage example**
```PYTHON
def interact(data):
    # Example of what to do with json data :
    if data["command_id"] == "test_command":
        print("Received data is the following : ",data)
        print("Data of param1 : ", data["param1"])
        print("Data of param2 : ", data["param2"])
        print("Data of param3 : ", data["param3"])
        print("Data of param4 : ", data["param4"])
```

## Client.py
Client.py contains the code to be run on the client machine. Connection and deconnection is performed at each data exchange to avoid hanging.
### Doc
#### send_data
> Function used to send data to a server.
- **json_data** : JSON data to send to the server.
- **host='127.0.0.1'** : IP of the host machine of the server. Defaults to localhost for internal tests
- **port=65432** : Port on which the server is running, defaults to 65432, check the server configuration.
- **debug=False** : If sets to *True*, prints debug messages, check code for more information.

Additional informations on JSONs can be found in the [Official Documentation](https://docs.python.org/fr/3/library/json.html).

**Usage example**
```PYTHON
if __name__ == "__main__":
   data = {
       "command_id": "test_command",
       "param1": 100,
       "param2": "this is text",
       "param3": True,
       "param4": [1,2,3,4, "text in list"]
   }

   send_data(data, host='127.0.0.1', port=65432,)
```

#### server_success
> Function called when the server reports operation success.

- **response_data** : JSON data returned by the server. Add your own code handling success here. No feedback inside the data, you can implement your own.

**Usage example**

```PYTHON
def server_success(response_data):
    print("Server reported success.")
```

#### server_fail
> Function called when the server reports operation failure.

- **response_data** : JSON data returned by the server. Add your own code handling failure here. No feedback inside the data, you can implement your own.

**Usage example**

```PYTHON
def server_fail(response_data):
    print('Server reported an error. {}'.format(response_data.get("error")))
```

#### fail_connect
> Function called when the server client cannot connect/contact the server.

- *No parameters*

**Usage example**

```PYTHON
def fail_connect():
    print("Failed to connect to the server or the server timed out.")
```

## Real-life application examples

Please check `Linking DDS to ARTIQ` of E-Lab, which is where this template is extracted from.