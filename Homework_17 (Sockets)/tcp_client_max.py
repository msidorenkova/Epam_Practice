import socket
import sys
import threading
import time
from datetime import datetime

import pyWinhook
import pythoncom


class Collector:

    def __init__(self):
        self.start = int(time.time())
        self.counter = 0
        self.flag = False
        self.hm = pyWinhook.HookManager()

    def start_collect(self):
        self.flag = True
        self.hm.MouseAll = self._timer
        self.hm.HookMouse()
        self.hm.KeyDown = self._onKeyboardEvent
        self.hm.HookKeyboard()
        pythoncom.PumpMessages()

    def _timer(self, event):
        if self.flag:
            current_time = int(time.time())
            if self.start != current_time:
                self.counter += 1
                self.start = current_time
        return True

    def _onKeyboardEvent(self, event):
        if event.Key == 'S' and self.flag:
            self.stop_collect()
            self.cleanup()
            print('Stopping data collection')
        elif event.Key == 'R' and not self.flag:
            print('Resuming data collection')
            self.start_collect()
        elif event.Key == 'Q':
            print('Stopping execution')
            sys.exit()
        return True

    def get_current_state(self):
        return self.counter

    def cleanup(self):
        self.counter = 0
        self.start = int(time.time())

    def stop_collect(self):
        self.flag = False


collector = Collector()
thread = threading.Thread(target=collector.start_collect)
thread.daemon = True
thread.start()

print('Starting data collection')
print('Press "s" to stop collecting data, "r" to resume collecting data or "q" to close a client: \n')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9999))

while True:
    time.sleep(60)

    if collector.flag:
        data = f'Mouse events, seconds: {str(collector.get_current_state())}'
        collector.cleanup()
    else:
        data = 'Data collection disabled'

    sock.send(data.encode('utf-8'))
    print(f'{datetime.now()}: Data has been sent')

sock.close()
