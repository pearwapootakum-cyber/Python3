import socket
from threading import Thread, Lock

HOST = '0.0.0.0'
PORT = 21001

clients = {}          
client_id_counter = 0
lock = Lock()


def broadcast(sender_id, text):
    with lock:
        for cid, c in clients.items():
            if cid != sender_id:
                try:
                    c.send(f"From {sender_id}: {text}\n".encode())
                except:
                    pass


def client_processor(conn, client_id):
    try:
        conn.send(f"Your client ID is {client_id}\n".encode())

        while True:
            data = conn.recv(4096)
            if not data:
                break

            text = data.decode().strip()
            print(f"Received from {client_id}: {text}")

            broadcast(client_id, text)

    finally:
        with lock:
            print(f"Client {client_id} disconnected")
            clients.pop(client_id, None)
        conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server listening...")

    while True:
        conn, addr = s.accept()

        with lock:
            client_id_counter += 1
            client_id = client_id_counter
            clients[client_id] = conn

        print(f"Client {client_id} connected from {addr}")
        Thread(target=client_processor, args=(conn, client_id), daemon=True).start()
