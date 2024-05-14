from src.infrastructure.sockets.user import UserSocket


class SocketManager:
    def __init__(self, socket):
        self.socket = socket

        @self.socket.on('connect')
        def initialize_events():
            self.setup_socket_events()

    def setup_socket_events(self):
        UserSocket(self.socket)
