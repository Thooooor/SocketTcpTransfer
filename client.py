import sys
import os
import time
from utils import *

dir_path = "upload_file/"   # windows using '\\'
buf_length = 1024


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port=8000):
        server_address = (host, port)
        self.sock.connect(server_address)
        print(sys.stderr, "connecting to %s port %s" % server_address)

    def upload(self, file_name):
        file_path = dir_path + file_name
        if not os.path.exists(file_path):
            print(sys.stderr, "path '%s' dose't exist." % file_path)
            return
        try:
            msg = "upload %s" % file_name
            self.sock.send(msg.encode('utf-8'))
            print(sys.stderr, 'sending: "%s"' % msg)
            time.sleep(1)
            with open(file_path, mode='rb') as f:
                while True:
                    line = f.read(buf_length)
                    if len(line) == 0:
                        break
                    self.sock.send(line)
            self.sock.shutdown(socket.SHUT_WR)
            while True:
                print("waiting")
                feedback = self.sock.recv(buf_length).decode('utf-8')
                if feedback == 'end':
                    print("upload succeeded.")
                    break
        finally:
            self.sock.close()

    def download(self, file_name):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        file_path = dir_path + file_name
        if os.path.exists(file_path):
            os.remove(file_path)
            print(sys.stderr, "file '%s' already exists. It will be rewritten." % file_name)
        msg = "download %s" % file_name
        print(sys.stderr, "sending: '%s'" % msg)
        self.sock.send(msg.encode('utf-8'))
        try:
            with open(file_path, mode='wb') as f:
                while True:
                    data = self.sock.recv(buf_length)
                    if len(data) == 0:
                        break
                    f.write(data)
        finally:
            print("download succeeded.")
            self.sock.close()


def shell():
    print("1. upload\n"
          "2. download\n"
          "3. exit")
    while True:
        choice = input("Input 1~3:")
        if choice == '1':
            client = Client()
            client.connect("39.107.251.174", 8000)
            file_name = input("File name you want to upload:")
            client.upload(file_name)
        elif choice == '2':
            client = Client()
            client.connect("39.107.251.174", 8000)
            file_name = input("File name you want to download:")
            client.download(file_name)
        elif choice == '3':
            break
        else:
            print("Wrong input")


if __name__ == '__main__':
    shell()
