import socket
from threading import Thread
import sys

HOST = '127.0.0.1'
PORT = 21001


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("\n[Server disconnected]")
                break

            # พิมพ์ข้อความจาก server
            sys.stdout.write("\n" + data.decode())
            sys.stdout.write("\nEnter message: ")
            sys.stdout.flush()

        except:
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # รับ client ID
    print(s.recv(1024).decode().strip())

    # thread รับข้อความ
    recv_thread = Thread(target=receive_messages, args=(s,), daemon=True)
    recv_thread.start()

    while True:
        msg = input("Enter message: ")
        if msg.lower() == "exit":
            break

        s.send(msg.encode())

print("Client finished")
