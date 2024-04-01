import socket

#default hosts , change later
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080

target_host = "127.0.0.1"
target_port = 8080

#create basic socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect client
client.connect((target_host,target_port))

#start sending data
client.send(b"hhhh")

#recieve data
response = client.recv(4096)
print(response.decode())
client.close()
