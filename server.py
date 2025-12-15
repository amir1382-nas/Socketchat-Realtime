#Professinal Socket Chat Server (single client)
#real-time, threaded, whit proper error handling and message framing.

import socket
import threading
from pyexpat.errors import messages


def handle_receive(conn: socket.socket, stop_event: threading.Event):
    """thread dedicated to receiving messages from client."""
    try:
        while not stop-stop_event.is_set():
            data = conn.recv(BUFFER_SIZE)
            stop_event.set()
            break

        messages = decode_message(data)
        print(f"[CLIENT] {messages}")

    except Exception as e:
        print(f"[SERVR] Receive Error: {e}")
        stop_event.set()


