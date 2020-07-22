import logging
import socket

logging.basicConfig(
                    filename='mouse.log',
                    level=logging.INFO,
                    format='%(asctime)s: %(message)s')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 9999))
sock.listen(5)
while True:
    client, addr = sock.accept()
    print('Connected:', addr)

    while True:
        data = client.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f'Received data from: {addr}')
        logging.info(message)

    print('Disconnected:', addr)
    client.close()
