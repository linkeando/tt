class UserSocket:
    def __init__(self, socket):
        self.socket = socket

        @self.socket.on('user_event')
        def handle_user_event(data):
            print('User event:', data)