
import os
import sys
import itertools
import filecmp
import socketserver
import argparse

welcomeMsg = (
    "--------------------------------------------------------------\n"
    "Welcome to the directory traversal and file comparison client.\n"
    "The following commands are available:\n"
    " cd [dir] - Traverse to directory 'dir'\n"
    " ls       - will print out the contents of the current directory\n"
    "            and perform file comparison\n"
    " pwd      - will print your current location\n"
    " help     - will reprint this welcome message\n"
    " exit     - terminate the application\n"
    "--------------------------------------------------------------")

# Create a request handler to manage client connections
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
		# Send welcome message as soon as a client connects
        print("Connection accepted from " + str(self.client_address[0]))
        self.request.sendall(bytes(welcomeMsg, "utf-8"))

        while True:
            # Receive the user's command and split into args
            self.cmd = self.request.recv(1024).strip().decode("utf-8").split(" ", 1) # We only expect 1 command and 1 argument max
            out = " ".join(self.cmd)

            if len(self.cmd[0]) < 2:
                continue

            print(str(self.client_address[0]) + " | cmd: " + out)

			# Process commands from the user
            if self.cmd[0] == "help":
                self.request.sendall(bytes(welcomeMsg, "utf-8"))

            elif self.cmd[0] == "pwd":
                self.request.sendall(bytes(os.getcwd(), "utf-8"))

            elif self.cmd[0] == "ls":
                files = os.listdir(".")
                fileComparison = dict.fromkeys(files, False)

				# Compare all the files in the directory against each other
				# Make a note of files that are duplicates
                for a, b in itertools.combinations(files, 2):
                    if filecmp.cmp(a, b) == True:
                        fileComparison[a] = b
                        fileComparison[b] = a

                outputBuffer = ""
                for f in fileComparison:
                    if fileComparison[f] == False:
                        outputBuffer += f + "\n"
                    else:
                        outputBuffer += f + " => duplicates " + fileComparison[f] + "\n"
                self.request.sendall(bytes(outputBuffer.rstrip(), "utf-8"))

            elif self.cmd[0] == "cd":
                if len(self.cmd) > 1:
                    if len(self.cmd[1]) > 0 and os.path.isfile(self.cmd[1]) == False and os.path.exists(self.cmd[1]) == True:
                        os.chdir(self.cmd[1])
                        self.request.sendall(bytes(os.getcwd(), "utf-8"))
                    elif len(self.cmd[1]) == 0:
                        os.chdir(os.environ['HOME'])
                        self.request.sendall(bytes(os.getcwd(), "utf-8"))
                    elif os.path.isfile(self.cmd[1]):
                        self.request.sendall(bytes("Not a directory.", "utf-8"))
                    else:
                        self.request.sendall(bytes("No such file or directory.", "utf-8"))
                else:
                    self.request.sendall(bytes("Command is missing arguments.", "utf-8"))

            elif self.cmd[0] == "exit":
                break;

            else:
                self.request.sendall(bytes("Command not recognised. Please type 'help' for a list of supported commands.", "utf-8"))

def main():
	# Get port number when the script starts
    parser = argparse.ArgumentParser(description='File comparison and directory traversal SERVER')
    parser.add_argument('server_port', type=int, help='Your server requires a port to start on')
    args = parser.parse_args()
    if args.server_port is None:
        parser.error("You must enter a port to start the server on")
        sys.exit()
    if args.server_port <= 1024:
        parser.error("Please do not use a reserved port number")
        sys.exit()

	# Start the server
    server = socketserver.TCPServer(('localhost', int(args.server_port)), MyTCPHandler)
    print('Server listening on localhost with port ' + str(args.server_port))
    server.serve_forever()


main()
