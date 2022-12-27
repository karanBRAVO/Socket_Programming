import socket
import threading # to run multiple processes at same time

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (IP, PORT)

SOCKET.bind(ADDR)

conn_list = []

def handle_client(conn, addr, conn_list):
    print(f"\n[NEW CLIENT] <{addr[0]} : {addr[1]}> connected.")

    while True:
        CLIENT_DATA = (conn.recv(1024)).decode()

        if CLIENT_DATA:
            if CLIENT_DATA == "!DISCONNECT":
                MESSAGE = "[DISCONNECTED] disconnected from the server"
                conn.send(MESSAGE.encode())
                conn_list.pop(conn_list.index(conn))
                break

            print("[RECEIVED] message received")
            print(f"Client[{addr[1]}]  data: ", CLIENT_DATA)

            for i in range(0, len(conn_list)):
                if conn_list[i] != conn:
                    print("[SENDING] sending messages ...")
                    MESSAGE = f"\n[{addr[1]}] {CLIENT_DATA}"
                    conn_list[i].send(MESSAGE.encode())
                    
    print(f"[CLOSING] closing connection for client[{addr[1]}] ...")
    conn.close()
    print(" --closed")

def startServer():
    SOCKET.listen()
    print(f"[LISTENING] on port: {PORT}")

    while True:
        print("[WAITING] waiting for connections ...")
        conn, addr = SOCKET.accept()
        print(f"[NEW CONNECTION]: {conn}")
        conn_list.append(conn)

        thread = threading.Thread(target=handle_client, args=(conn, addr, conn_list))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    print("[STARTING] server is starting ...")
    startServer()
