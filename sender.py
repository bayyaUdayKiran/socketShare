#Socket Client...
import tqdm
import socket
import os
import shutil
import sys

switch = sys.argv[1]

with open("network.txt", "rb") as f:
    data = f.readlines()

HOST = sys.argv[2]

if HOST.lower() == "realme gt":
    IP_ADDR = data[0]

elif HOST.lower() == "acer pc":
    IP_ADDR = data[0]

PORT = int(sys.argv[3])


SEPERATOR = ";"
BUFFER_SIZE = 4096

send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def file_info(switch):
    for dir in os.listdir():
        if ((dir!="recepient.py")and(dir!="sender.py")and(dir!="venv")and(dir!="socketShare.fix")and(dir!=".git")):
            the_dir = dir

    if switch == '-d':
        filename, filesize = zip(the_dir)
    elif switch == '-f':
        filename = the_dir
        filesize = os.path.getsize(filename)

    return filename, filesize

        

def zip(the_dir):
    '''
    for dir in os.listdir():
        if ((dir!="recepient.py")and(dir!="sender.py")and(dir!="venv")and(dir!="socketShare.fix")):
            the_dir = dir
    '''
    #Making an archieve from the folder..
    print("Compressing the folder " + the_dir + ", to " + the_dir + ".zip...")
    shutil.make_archive(the_dir, 'zip', the_dir)
    

    size = os.path.getsize(the_dir + ".zip")
    return the_dir + ".zip", size




def connectNsendIno(filename, filesize):
    #Establishes  a connection between the socket and host..
    print(f"[+] Connecting to {IP_ADDR}:{PORT}..")
    while True:
        try:
            send_sock.connect((IP_ADDR, PORT))
            break
        except ConnectionRefusedError:
            pass

    print("[+] Connected.")
    send_sock.send(f"{filename}{SEPERATOR}{filesize}".encode()) #Sends the file's info to the server..


def send_file(filename, filesize, switch):
    #Sends the desired file to the recepient..
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break

            send_sock.sendall(bytes_read)
            progress.update(len(bytes_read))  # update the progress bar

    send_sock.close()
    if(switch=='-d'):
        os.remove(filename) #Deleting the unwanted zip file..

    

def main():
    filename, filesize = file_info(switch)
    '''
    if switch == '-d':
        filename, filesize = zip()
    elif switch == '-f':
        for file in os.listdir():
            if ((file!="recepient.py")and(file!="sender.py")and(file!="venv")and(file!="socketShare.fix")):
                filename = file
        filesize = os.path.getsize(filename)
    '''
    connectNsendIno(filename, filesize)
    send_file(filename, filesize, switch)

    



if __name__ == "__main__":
    main()


