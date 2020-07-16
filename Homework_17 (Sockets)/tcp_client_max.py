import socket
import threading
import time
from datetime import datetime

import keyboard
import pyWinhook
import pythoncom


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
        else:
            data = f'Data collection disabled'
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
collector.start_collect()
print('Starting data collection')
print('Press "s" to stop collecting data, "r" to resume collecting data or "q" to close a client: \n')

while True:
    if keyboard.is_pressed('s') and collector.flag:
        collector.stop_collect()
        print('Stopping data collection')
    elif keyboard.is_pressed('r') and not collector.flag:
        collector.start_collect()
        print('Resuming data collection')
    elif keyboard.is_pressed('q'):
        print('Stopping execution')
        break
