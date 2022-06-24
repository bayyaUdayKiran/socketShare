#Socket Client...
import tqdm
import socket
import os
import shutil


IP_ADDR = input("Recepient's IP Address: ")
PORT = int(input("Recepient's Port Number:"))

SEPERATOR = ";"
BUFFER_SIZE = 4096

send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def zip():
    for dir in os.listdir():
        if ((dir!="recepient.py")and(dir!="sender.py")and(dir!="venv")):
            the_dir = dir

    #Making an archieve from the folder..
    print("Compressing the folder " + the_dir + ", to " + the_dir + ".zip...")
    shutil.make_archive(the_dir, 'zip', 'movies')
    

    size = os.path.getsize(the_dir + ".zip")
    return the_dir + ".zip", size


'''
def file_info():
    #Returns, filename & filesize..
    the_file = None
    for file in os.listdir():
        if ((file!="recepient.py")and(file!="sender.py")):
            if(os.path.isfile(file)):
                the_file = file
                size = os.path.getsize(the_file)
    return the_file, size

'''

def connect(filename, filesize):
    #Establishes  a connection between the socket and host..
    print(f"[+] Connecting to {IP_ADDR}:{PORT}..")
    send_sock.connect((IP_ADDR, PORT))
    print("[+] Connected.")
    send_sock.send(f"{filename}{SEPERATOR}{filesize}".encode())


def send_file(filename, filesize):
    #Sends the desired file to the recepient..
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=4096)
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
    filename, filesize = zip()
    connect(filename, filesize)
    send_file(filename, filesize)
    os.remove("movies.zip")



if __name__ == "__main__":
    main()


