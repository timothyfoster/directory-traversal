import socket
import sys

# Ask user for IP address and port number
ip = input("Please enter the IP to connect to (press enter for localhost): ")
if ip == "":
    ip = 'localhost'
port = int(input("Please enter a port to connect to: "))

# Try to connect to socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.settimeout(5)
server_address = (ip, port)
try:
    print('connecting to {} on port {}'.format(*server_address))
    socket.connect(server_address)
except Exception:
    print("The server is not running.")
    sys.exit()

# Receive and print out the initial welcome message from the server
localCmd = [""]
received = str(socket.recv(1024), "utf-8")
print(received)

# Ask the user for their command and pause
while localCmd[0] != "exit":
    cmd = input(":")
    localCmd = cmd.split(" ", 1)

	# Disregard typo's
    if len(cmd) < 2:
        continue

	# Send command to server and print response
    try:
        socket.sendall(bytes(cmd, "utf-8"))
        received = str(socket.recv(1024), "utf-8")
        print('\033[93m' + received + '\033[0m')

    except Exception:
        print("Error sending to server.")
        sys.exit()

	# If the user wants to exit, close the socket
    if localCmd[0] == "exit":
        print('\033[93m' + "Closing socket" + '\033[0m')
        received = str(socket.recv(1024), "utf-8")
        socket.close()
        break;

print('\033[93m' + "Goodbye!" + '\033[0m')
sys.exit()
