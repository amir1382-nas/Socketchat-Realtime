import socket
import threading
from config import HOST , PORT , BUFFER_SIZE
from utils import encode_message, decode_message


def handle_receive(sock: socket.socket, stop_event: threading.Event):
    """Thread dedicated to receiving messages from server."""
    try:
        while not stop_event.is_set():
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("[CLIENT] Server disconnected.")
                stop_event.set()
                break

            message = decode_message(data)
            print(f"[SERVER] {message}")

    except Exception as e:
        print(f"[CLIENT] Receive Error: {e}")
        stop_event.set()


def start_client():
    """Connect to server and open full-duplex chat."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(f"[CLIENT] Connection failed: {e}")
        return

    print(f"[CLIENT] Connected to {HOST}:{PORT}. Type /quit to exit.")

    stop_event = threading.Event()

    # Start receiver thread
    receiver = threading.Thread(
        target=handle_receive,
        args=(sock, stop_event),
        daemon=True
    )
    receiver.start()

    try:
        while not stop_event.is_set():
            user_input = input()

            if user_input.lower() in ("/quit", "/exit"):
                print("[CLIENT] Closing connection...")
                stop_event.set()
                break

            sock.sendall(encode_message(user_input))

    finally:
        stop_event.set()
        sock.close()
        print("[CLIENT] Socket closed. Goodbye.")


if __name__ == "__main__":
    start_client()