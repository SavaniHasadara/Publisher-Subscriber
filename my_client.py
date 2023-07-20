import socket
import sys


class MyClientApp:
    def __init__(self, server_ip, port, client_type, topic):
        self.server_ip = server_ip
        self.port = int(port)
        self.client_type = client_type
        self.topic = topic
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.server_ip, self.port)
        self.client_socket.connect(server_address)
        print(f"Connected to server: {server_address}")
        self.client_socket.sendall(self.client_type.encode())
        # Send the topic to the server
        client_info = f"{self.client_type}|{self.topic}"
        self.client_socket.sendall(client_info.encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

    def receive_message(self):
        message = self.client_socket.recv(1024).decode()
        print(f"Received from server: {message}")

    def disconnect(self):
        self.client_socket.sendall("terminate".encode())
        self.client_socket.close()
        print("Client connection closed")

    def run_publisher(self):
        self.connect()

        while True:
            message = input("Type a message to publish: ")
            # Send the topic along with the message
            self.send_message(f"{self.topic}:{message}")

            if message.lower() == "terminate":
                break

        self.disconnect()

    def run_subscriber(self):
        self.connect()

        while True:
            self.receive_message()

        self.disconnect()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python my_client_app.py <server_ip> <port> <client_type> <topic>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = sys.argv[2]
    client_type = sys.argv[3]
    topic = sys.argv[4]
    client_app = MyClientApp(server_ip, port, client_type, topic)

    if client_type == "PUBLISHER":
        client_app.run_publisher()
    elif client_type == "SUBSCRIBER":
        client_app.run_subscriber()
