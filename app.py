import argparse
import socket


class Netcat():
    def __init__(self, host, port, mode):
        self.host = host
        self.port = port
        self.mode = mode

    def run(self):
        # Determine whether to act as a server (listening) or a client (connecting)
        if self.mode == "server":
            self.server_mode()
        else:
            self.client_mode()

    def server_mode(self):
        # Create a TCP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SOL_SOCKET + SO_REUSEADDR allows immediate reuse of the port after closing
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the address and port
        server.bind((self.host, self.port))

        # Listen for incoming connections (queue up to 2)
        server.listen(2)
        print(f"[*] Server is listening on {self.host}:{self.port}")

        # Accept a connection - this blocks until a client connects
        conn, addr = server.accept()
        print(f"[*] Connection from {addr}")

        # Loop to continuously receive data from the connected client
        while True:
            data = conn.recv(1024)
            # If recv returns empty bytes, the client has disconnected
            if not data:
                break
            print(f"[*] Received message: {data.decode()}")
            conn.send(b"Message received")

        # Close the connection
        conn.close()

    def client_mode(self):
        # Create a TCP socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client.connect((self.host, self.port))
        print(f"[*] Client connected to {self.host}:{self.port}")

        # Send a message to the server
        client.send(b"Hello from client!")

        # Receive data from the server
        data = client.recv(1024)
        print(f"[*] Received data: {data.decode()}")

        # Close the socket
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Netcat Utility")
    parser.add_argument("-m", "--mode", choices=["server", "client"], required=True, help="Mode: server or client")
    parser.add_argument("-t", "--host", default="127.0.0.1", help="Target host")
    parser.add_argument("-p", "--port", type=int, required=True, help="Target port")
    args = parser.parse_args()

    nc = Netcat(args.host, args.port, args.mode)
    nc.run()