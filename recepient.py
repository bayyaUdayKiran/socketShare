#Socket Server...

import socket
import tqdm
import os
from zipfile import ZipFile
import shutil
import sys

IP_ADDR = ''
switch = sys.argv[1]
PORT = int(sys.argv[2])

BUFFER_SIZE = 4096
SEPARATOR = ";"

recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def accept_sender():
    recv_sock.bind((IP_ADDR, PORT))
    recv_sock.listen(5)
    print(f"[*] Waiting for the sender at [any]:{PORT}")
    send_sock, send_addr = recv_sock.accept()
    # if below code is executed, that means the sender is connected
    print(f"[+] {send_addr} is connected.")
    return send_sock


def recv_file_info(send_sock):
    received = send_sock.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    return filename, filesize


def recv_file(filename, filesize, send_sock):
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            bytes_read = send_sock.recv(BUFFER_SIZE)
            if not bytes_read:
                break
        
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the client socket
    send_sock.close()
    # close the server socket
    recv_sock.close()


def unzip(filename):
    with ZipFile(filename, 'r') as zip:
        print('Unzipping the folder now...')
        zip.extractall()
        print('Done!')
    


def directorise(dirname):
    files = []
    for file in os.listdir():
        if ((file!="recepient.py")and(file!="sender.py")and(file!="venv")and(file!="socketShare.fix")):
            if(os.path.isfile(file)):
                files.append(file)

    os.mkdir(dirname)

    for file in files:
        shutil.move(file, dirname)





def main():
    send_sock = accept_sender()
    filename, filesize = recv_file_info(send_sock)
    recv_file(filename, filesize, send_sock)
    if switch == '-d':
        unzip(filename)
        dirname = filename.replace('.zip', '')
        directorise(dirname)

   

        


    

if __name__ == "__main__":
    main()




    

