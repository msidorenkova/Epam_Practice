import argparse
import io
import os
import re
import time
import urllib.request
from multiprocessing.pool import ThreadPool
from threading import Lock

from PIL import Image


def valid_size(size):
    return tuple(map(int, re.fullmatch(r'(\d*)x(\d*)', size).group(1, 2)))


def valid_urllist(urllist):
    if os.path.isfile(urllist):
        return urllist
    raise argparse.ArgumentTypeError(f'File {urllist} does not exist')


parser = argparse.ArgumentParser(description='download and process images in multiple threads')

parser.add_argument('urllist', nargs='?', default='.', type=valid_urllist, help='path to file with urls')
parser.add_argument('--dir', default='.', nargs='?', help='specify destination directory')
parser.add_argument('--threads', default='1', nargs='?', type=int, help='specify number of threads')
parser.add_argument('--size', default='100x100', nargs='?', type=valid_size, help='define maximum image size')

args = parser.parse_args()

counter = 0
error_counter = 0
bytes_downloaded = 0
lock = Lock()

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent':user_agent,}


def download_image(num_url):
    num, url = num_url

    try:
        request = urllib.request.Request(url, None, headers)
        data = urllib.request.urlopen(request)
        meta = int(data.headers['Content-Length'])
        data = data.read()

    except:
        print(f'Error: Invalid url, line {num}',)
        with lock:
            global error_counter
            error_counter += 1
        return

    process_image(num, meta, data)


def process_image(num, meta, data):
    filename = f'{num:05}.jpeg'

    try:
        img = Image.open(io.BytesIO(data))
        img.thumbnail(args.size)
        img = img.convert("RGB")

        if not os.path.exists(args.dir):
            os.makedirs(args.dir)

        img.save(os.path.join(args.dir, filename))
        print(f'Image saved: {filename}')
        with lock:
            global bytes_downloaded
            global counter
            bytes_downloaded += meta
            counter += 1

    except:
        print(f'Error: Invalid image, line {num}')
        with lock:
            global error_counter
            error_counter += 1

with open(args.urllist, 'r') as fnm:
    lines = enumerate(fnm.readlines())

start_time = time.time()
pool = ThreadPool(args.threads)
results = pool.map(download_image, lines)
pool.close()
pool.join()
stop_time = time.time() - start_time

print('----')
print(f'Images Saved: {counter}')
print(f'Bytes Downloaded: {bytes_downloaded}')
print(f'Saving Images Failed: {error_counter}')
print(f'Time spent: {round(stop_time, 2)} sec')
