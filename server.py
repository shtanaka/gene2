# coding: utf-8
import SocketServer
import threading

import time
import datetime
import sys


class Server(SocketServer.BaseRequestHandler):
    def append_message(self, message):
        file = open('server-list.txt', 'a')
        if message != "":
            file.write(message + "\n")
        file.close()

    def clear_file(self):
        file = open('server-list.txt', 'w')
        file.write("")
        file.close()

    def read_file(self):
        file = open('server-list.txt', 'r')
        out = file.read()
        file.close()
        return out

    def update_line(self, index, new_line):
        f = open('server-list.txt', 'r')
        lines = f.readlines()
        lines[index] = new_line + "\n"
        f.close()
        f = open('server-list.txt', 'w')
        f.writelines(lines)
        f.close()

    def get_file_len(self):
        return self.read_file().__len__()

    def get_current_time_in_seconds(self):
        h, min, sec = datetime.datetime.now().strftime('%H:%M:%S').split(":")
        return str(int(h) * 3600 + int(min) * 60 + int(sec))

    def write_if_new(self, message):
        data, origin = self.data.split("/")
        cpu, mem = data.split(" ")
        self.append_message(message)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.write_if_new(self.data)
        self.request.send("Thanks for sending the message %s" % self.data)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ResourcesDB(threading.Thread):
    def __init__(self, threadID=1, name="resourcesDB"):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cpu = 0
        self.mem = 0
        self.serverlist = dict({})

    def clear_file(self):
        file = open('server-list.txt', 'w')
        file.write("")
        file.close()

    def calculate_resources(self):
        while True:
            self.cpu = 0
            self.mem = 0
            self.serverlist = dict({})
            for line in self.read_file().split("\n"):
                try:
                    data, origin = line.split("/")
                    self.serverlist[origin] = data
                except:
                    pass
            for v in self.serverlist.values():
                cpu, mem = v.split(" ")
                cpu = int(cpu)
                mem = int(mem)
                self.cpu += cpu
                self.mem += mem

            print self.serverlist
            print self.cpu
            print self.mem
            self.clear_file()
            time.sleep(2)

    def run(self):
        self.calculate_resources()

    def append_message(self, message):
        file = open('server-list.txt', 'a')
        file.write(message + "\n")
        file.close()

    def clear_file(self):
        file = open('server-list.txt', 'w')
        file.write("")
        file.close()

    def read_file(self):
        file = open('server-list.txt', 'r')
        out = file.read()
        file.close()
        return out

    def get_file_len(self):
        return self.read_file().__len__()

    def remove_line(self, file_line):
        file_lines = self.read_file().split()
        self.clear_file()
        for line in file_lines:
            if not line == file_line:
                self.append_message(line)


if __name__ == "__main__":
    HOST, PORT = "ec2-52-35-106-21.us-west-2.compute.amazonaws.com", int(sys.argv[1])

    # server = ThreadedTCPServer((HOST, PORT), Server)
    # ip, port = server.server_address
    # print "IP " + str(ip) + ":" + str(port)
    # server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.start()

    resourcesDB = ResourcesDB()
    resourcesDB.start()
    server = SocketServer.TCPServer((HOST, PORT), Server)
    server.serve_forever()
