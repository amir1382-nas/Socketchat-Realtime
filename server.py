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


def start_server():
    """start TCP server and handle one client in full-duplex mode."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"[SERVER] listening on {HOST}:{PORT} ...")
    conn, addr = server_socket.accept()
    print(f"[SERVER] connection accepted from {addr}")

    stop_event = threading.Event()
    #start receiving threa
    receiver = threading.Thread(
        target=handle_receive,
        args=(conn, stop_event),
        daemon=True
    )
    receiver.start()

    try:
        while not stop_event.is_set():
            user_input = input()

            if user_input.lower() in ("/quit", "/exit"):
                print("[SERVER] shutting down...")
                stop_event.set()
                break

            conn.sendall(encod_message(user_input))

    finally:
        stop_event.set()
        conn.close()
        server_socket.close()
        print("[SERVER] closed all sockets. Byyyyye.")


if __name__=="__main__":
    start_server()