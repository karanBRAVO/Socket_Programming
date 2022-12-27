import socket
import sys
import threading # to run multiple processes at same time

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())  # host IP
PORT = 12345  # server port
ADDR = (IP, PORT)

print("""
** type [!DISCONNECT] to exit
""")

def askFORmsg():  # messaging
    while True:
        msg = input(">> ")
        SOCKET.send(msg.encode())
        if msg == "!DISCONNECT":
            break

def checkMsg():  # infinitely checks for any message
    while True:
        SERVER_DATA = (SOCKET.recv(1024)).decode()
        if SERVER_DATA:
            if SERVER_DATA == "[DISCONNECTED] disconnected from the server":
                print(" --Disconnected")
                break
            print(SERVER_DATA)
    SOCKET.close()

def connectTOserver(addr):  # making connection to the server
    print("[CONNECTING] connecting to server ...")
    try:
        SOCKET.connect(addr)
        print("-- connected")
    except socket.error:
        print("[!NOT CONNECTING] No host is found")
        sys.exit()

    thread1 = threading.Thread(target=askFORmsg)
    thread1.start()

    thread2 = threading.Thread(target=checkMsg)
    thread2.start()

if __name__ == "__main__":
    connectTOserver(addr=ADDR)
