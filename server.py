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
            print("[RECEIVED] message received")

            if CLIENT_DATA.find("joined[#123$456&789(0)]") != -1:
                if (threading.activeCount() - 1 - 1) == 1:
                    MESSAGE = f"\n\t[SERVER]: {threading.activeCount() - 1 - 1} user is already here"
                else:
                    MESSAGE = f"\n\t[SERVER]: {threading.activeCount() - 1 - 1} users are here"
                conn.send(MESSAGE.encode())
                CLIENT_NAME = CLIENT_DATA.removesuffix(" joined[#123$456&789(0)]")
                CLIENT_DATA = " new user joined"

            print(f"Client[{addr[1]}]  data: ", CLIENT_DATA)

            if len(conn_list) > 1:
                for i in range(0, len(conn_list)):
                    if conn_list[i] != conn:
                        print("[SENDING] sending messages ...")
                        if CLIENT_DATA == "!DISCONNECT":
                            MESSAGE = f"\n\t[{addr[1]}] [{CLIENT_NAME}]: left"
                        else:
                            MESSAGE = f"\n\t[{addr[1]}] [{CLIENT_NAME}]: {CLIENT_DATA}"
                        conn_list[i].send(MESSAGE.encode())
                        print("[SENT] message sent")

            if CLIENT_DATA == "!DISCONNECT":
                MESSAGE = "[DISCONNECTED] disconnected from the server"
                conn.send(MESSAGE.encode())
                conn_list.pop(conn_list.index(conn))
                break
                    
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
