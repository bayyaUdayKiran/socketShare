import argparse
import socket
import os
import tqdm
from zipfile import ZipFile
import shutil

BUFFER_SIZE = 4096
SEPARATOR = ";"

class Lib:
    def manarger(self):
        parser = argparse.ArgumentParser(prog='Sockshare', description='Simple File/Directory sharing software', epilog='Made with Love:)', allow_abbrev=False)
        parser.add_argument('host', metavar='Host', type=str, help='IP Address of the Host, to listen or connect')
        parser.add_argument('-p', '--port', metavar='Port', type=int, help="Port to bind or to connect")
        parser.add_argument('-t', '--type', metavar='File type', type=str, help="File type f[file] or d[directory]") 
        args = parser.parse_args()
        theargs = [args.host, args.port, args.type]

        return theargs 


    def getfinfo(self, sock):
        fdata = sock.recv(BUFFER_SIZE).decode()
        filename, filesize = fdata.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        return filename, filesize

            

    def runserver(self, port, type):
        #Initializes Server...
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if port:
            server.bind(('', int(port)))
            server.listen(5)
            print(f"[*] Waiting for the sender at [any]:{port}")
            client, clientIP = server.accept()
            print(f"[+] {clientIP} is connected.")
            #Receives file...
            filename, filesize = self.getfinfo(client)
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                while True:
                    bytes_read = client.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    #update the progress bar
                    progress.update(len(bytes_read))
                    #Terminate connection...
            client.close()
            server.close()
        else:
            server.bind(('', 9999))
            server.listen(5)
            print("[*] Waiting for the sender at [any]:9999")
            client, clientIP = server.accept()
            print(f"[+] {clientIP} is connected.")
            #Receives file...
            filename, filesize = self.getfinfo(client)
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                while True:
                    bytes_read = client.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    #update the progress bar
                    progress.update(len(bytes_read))
                    #Terminate connection...
            client.close()
            server.close()

        

        if type == 'd' or type == 'directory':
            #Unzipping...
            with ZipFile(filename, 'r') as zip:
                print('Unzipping the folder now...')
                zip.extractall()
                print('Done!')
                os.remove(filename)
            dirname = filename.replace('.zip', '')

            #Directorise...
            files = []
            for file in os.listdir():
                if (file!="lib.py")and(file!="sock.py"):
                    if(os.path.isfile(file)):
                        files.append(file)
            os.mkdir(dirname)
            for file in files:
                shutil.move(file, dirname)

        

    def runclient(self, host, port, type):
        filename = ''
        filesize = 0

        #Initialize client...
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for dir in os.listdir():
            if (dir!='sock.py')and(dir!="lib.py")and(dir!="__pycache__"):
                the_dir = dir

        if type == 'd' or type == 'directorise':
            print("Compressing the folder " + the_dir + ", to " + the_dir + ".zip...")
            shutil.make_archive(the_dir, 'zip', the_dir)
            size = os.path.getsize(the_dir + ".zip")
            filename =  the_dir + ".zip"
            filesize =  size

        else:
            filename = the_dir
            filesize = os.path.getsize(the_dir)


        if port:
            print(f"[+] Connecting to {host}:{port}..")
            while True:
                try:
                    client.connect((host, int(port)))
                    break
                except ConnectionRefusedError:
                    pass
        
        else:
            print(f"[+] Connecting to {host}:9999..")
            while True:
                try:
                    client.connect((host, 9999))
                    break
                except ConnectionRefusedError:
                    pass

        print("[+] Connected.")
        client.send(f"{filename}{SEPARATOR}{filesize}".encode()) 

        #Sending file...
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break

                client.sendall(bytes_read)
                progress.update(len(bytes_read))  # update the progress bar

        client.close()
        if type=='d' or type == 'directory':
            os.remove(filename)


        