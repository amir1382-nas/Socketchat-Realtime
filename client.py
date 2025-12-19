import socket
import threading
from config import HOST , PORT , BUFFER_SIZE
from server import handle_receive
from utils import encode_message, decode_message

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(f"[CLIENT] connection failed: {e}")
        return

    print(f"[CLIENT] connected to {HOST}:{PORT}. Type /quit to exit.")
    stop_event = threading.Event()

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
                print("[CLIENT] closing connection...")
                stop_event.set()
                break

            try:
                sock.sendall(encode_message(user_input))
            except BrokenPipeError:
                print("[CLIENT] connection lost while sending.")
                stop_event.set()
                break

    finally:
        stop_event.set()
        sock.close()
        print("[CLIENT] socket closed. Bye.")

