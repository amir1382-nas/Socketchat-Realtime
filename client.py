import socket
import threading
from config import HOST , PORT , BUFFER_SIZE
from utils import encode_message, decode_message

def handle_recive(sock: socket.socket, stop_event:threading.Event):
    """thread dedicated to receiving messages from server."""
    try:
        while not stop_event.is_set():
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("[CLIENT] server disconnected.")
                stop_event.set()
                break

            message = decode_message(data)
            print(f"[CLIENT] {message}")

    except Exception as e:
        print(f"[CLIENT] receive error: {e}")
        stop_event.set()

def start_client():
    """connect to server and open full-duplex chat."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(f"[CLIENT] connection failed: {e}")
        return

    print(f"[CLIENT] connected to {HOST}:{PORT}. Type /quit to exit.")
    stop_event = threading.Event()

    #start reciver thread
    reciver = threading.Thread(
        target=handle_recive,
        args=(sock, stop_event),
        daemon=True
    )
    reciver.start()

    try:
        while not stop_event.is_set():
            user_input = input()

            if user_input.lower() in ("/quit" , "/exit"):
                print("[CLIENT] closing connection...")
                stop_event.set()
                break
            sock.sendall(encode_message(user_input))

    finally:
        stop_event.set()
        sock.close()
        print("[CLIENT] socket closed . byyyye")
if __name__ == "__main__":
    start_client()
