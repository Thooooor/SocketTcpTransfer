import os
import sys
import time
from threading import Thread

from utils import *

buf_length = 1024
store_path = "files/"
FLAGS = {
    1: "Error Please enter right number of argv.",
    2: "Error Parameter Not Founded.",
    3: "Error File dose't not exist.",
}


class ClientThread(Thread):
    def __init__(self, client_address, sock):
        Thread.__init__(self)
        self.ip, self.port = client_address
        self.sock = sock
    
    def run(self):
        print("Thread:%d\tNew thread started for %s:%s" % (self.ident, self.ip, str(self.port)))
        while True:
            buf = self.sock.recv(buf_length).decode()
            argv, argc = parse_argv(buf)
            print(sys.stderr, "received '%s'" % buf)

            if argv[0] == 'download':
                self.send(argv[1])
            elif argv[0] == 'upload':
                self.receive(argv[1])
            else:
                break

    def receive(self, file_name):
        print("receive file name: %s" % file_name)
        if not os.path.exists(store_path):
            os.mkdir(store_path)

        file_path = store_path + file_name
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, mode='wb') as f:
            print("open file")
            while True:
                data = self.sock.recv(buf_length)
                if len(data) == 0:
                    break
                f.write(data)
        time.sleep(1)
        print("sending: 'end'")
        self.sock.send(b'end')

    def send(self, file_name):
        file_path = store_path + file_name
        if not os.path.exists(file_path):
            return

        with open(file_path, mode='rb') as f:
            while True:
                line = f.read(buf_length)
                if len(line) == 0:
                    break
                self.sock.send(line)
        self.sock.shutdown(socket.SHUT_WR)
        print("end")

    def send_flag(self, flag):
        self.sock.send(FLAGS[flag].encode())
    

class Server:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.threads = []

    def start(self):
        while True:
            self.sock.listen(5)
            print("Waiting for a connection")
            connection, client_address = self.sock.accept()
            print(sys.stderr, "client connected: ", client_address)
            # 创建线程
            new_thread = ClientThread(client_address, connection)
            new_thread.start()
            self.threads.append(new_thread)


if __name__ == '__main__':
    server = Server('0.0.0.0', 8000)
    server.start()
