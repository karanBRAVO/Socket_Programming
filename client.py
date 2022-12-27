import socket
import sys
 
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())  # host IP
PORT = 12345  # server port
ADDR = (IP, PORT)
CONNECTION = True

print("""
** type [!DISCONNECT] to exit
** type [!CHECK_MSG] to check for any messages
""")

def connectTOserver(addr):
    global CONNECTION

    print("[CONNECTING] connecting to server ...")
    try:
        SOCKET.connect(addr)
        print("-- connected")
    except socket.error:
        print("[!NOT CONNECTING] No host is found")
        sys.exit()

    while CONNECTION:
        msg = input(">>> ")
        SOCKET.send(msg.encode())

        DATA = (SOCKET.recv(1024)).decode()
        if DATA:
            if DATA == "[DISCONNECTED] disconnected from the server":
                print(" --Disconnected")
                CONNECTION = False
            print(DATA)
    
    SOCKET.close()

if __name__ == "__main__":
    connectTOserver(addr=ADDR)
