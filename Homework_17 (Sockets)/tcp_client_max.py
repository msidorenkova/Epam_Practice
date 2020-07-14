import socket
import threading
import pythoncom
import pyWinhook
import time
from datetime import datetime

class Collector:

    def __init__(self):
        self.start = int(time.time())
        self.counter = 0
        self.flag = False

    def start_collect(self):
        self.flag = True

    def timer(self):
        if self.flag:
            current_time = int(time.time())
            if self.start != current_time:
                self.counter += 1
                self.start = current_time

    def get_current_state(self):
        return self.counter

    def cleanup(self):
        self.counter = 0
        self.start = int(time.time())

    def stop_collect(self):
        self.flag = False


def create_thread(func):
    thread = threading.Thread(target=func)
    thread.daemon = True
    thread.start()


def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9999))

    while True:
        time.sleep(60)
        if collector.flag:
            data = f'Mouse events, seconds: {str(collector.get_current_state())}'
            collector.cleanup()
            sock.send(data.encode('utf-8'))
            print(f'{datetime.now()}: Data has been sent')
    sock.close()


def detect_mouse_event():
    hm = pyWinhook.HookManager()
    hm.MouseAll = onMouseEvent
    hm.HookMouse()
    pythoncom.PumpMessages()


def onMouseEvent(event):
    collector.timer()
    return True


collector = Collector()

create_thread(detect_mouse_event)
create_thread(start_client)

while True:
    cmd = input('Input a command (start, stop, get, clean or exit): ')
    if cmd == 'start':
        collector.start_collect()
    elif cmd == 'stop':
        collector.stop_collect()
    elif cmd == 'get':
        collector.get_current_state()
    elif cmd == 'clean':
        collector.cleanup()
    elif cmd == 'exit':
        break
    else:
        print('Invalid command')
