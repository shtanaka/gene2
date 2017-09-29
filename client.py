# !/usr/bin/env python
# coding: utf-8

import sys
import socket
import time
import uuid


def help():
    print "uso: python client.py 2 1024 127.0.0.1:7000"


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    def __str__(self):
        return self.body


class HTTPClient(object):
    def __init__(self, host="127.0.0.1", port=7000):
        self.host = host
        self.port = port
        self.uuid = uuid.uuid4()

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
            return sock
        except:
            return None

    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def send_message(self, message):

        sock = self.connect()
        if sock != None:
            sock.sendall(message + "/" + self.uuid.__str__())
            response = self.recvall(sock)
            return response
        else:
            return "servidor offline"

    def notify_server(self):
        while True:
            print self.send_message("2 1024")
            time.sleep(1.5)


if __name__ == "__main__":
    client = HTTPClient(sys.argv[1], int(sys.argv[2]))
    client.notify_server()
