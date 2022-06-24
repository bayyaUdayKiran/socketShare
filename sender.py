#Socket Client...
import tqdm
import socket
import os

IP_ADDR = input("Recepient's IP Address: ")
PORT = int(input("Recepient's Port Number:"))

SEPERATOR = ";"
BUFFER_SIZE = 4096

send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def file_info():
    #Returns, filename & filesize..
    the_file = None
    for file in os.listdir():
        if ((file!="recepient.py")and(file!="sender.py")):
            if(os.path.isfile(file)):
                the_file = file
                size = os.path.getsize(the_file)
    return the_file, size


def connect(filename, filesize):
    #Establishes  a connection between the socket and host..
    print(f"[+] Connecting to {IP_ADDR}:{PORT}..")
    send_sock.connect((IP_ADDR, PORT))
    print("[+] Connected.")
    send_sock.send(f"{filename}{SEPERATOR}{filesize}".encode())


def send_file(filename, filesize):
    #Sends the desired file to the recepient..
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break

            send_sock.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    send_sock.close()

def main():
    filename, filesize = file_info()
    connect(filename, filesize)
    send_file(filename, filesize)


if __name__ == "__main__":
    main()


