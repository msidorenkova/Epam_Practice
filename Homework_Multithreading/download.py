import argparse
import io
import os
import re
import time
import urllib.error
import urllib.request
from collections import namedtuple
from functools import partial
from multiprocessing.pool import ThreadPool
from threading import Lock

from PIL import Image, UnidentifiedImageError


def valid_size(size):
    try:
        return tuple(map(int, re.fullmatch(r'(\d*)x(\d*)', size).group(1, 2)))
    except AttributeError:
        raise argparse.ArgumentTypeError('Invalid size')


def valid_urllist(urllist):
    if os.path.isfile(urllist):
        return urllist
    raise argparse.ArgumentTypeError(f'File {urllist} does not exist')


def valid_dir(d):
    try:
        if not os.path.exists(d):
            os.makedirs(d)
        return d
    except NotADirectoryError:
        raise argparse.ArgumentTypeError(f"Invalid dir '{d}'")


def download_image(args, headers, lock, counters, line):
    try:
        request = urllib.request.Request(line.url, headers=headers)
        data = urllib.request.urlopen(request)
        meta = int(data.headers['Content-Length'])
        data = data.read()

    except (urllib.error.HTTPError, urllib.error.URLError, TypeError, ConnectionResetError):
        print(f'Error: Invalid url, line {line.num}',)
        with lock:
            counters.error_counter += 1
        return

    process_image(line, meta, data, lock, counters, args)


def process_image(line, meta, data, lock, counters, args):
    try:
        img = Image.open(io.BytesIO(data))
        img.thumbnail(args.size)
        img = img.convert("RGB")

    except UnidentifiedImageError:
        print(f'Error: Invalid image, line {line.num}')
        with lock:
            counters.error_counter += 1
        return

    filename = f'{line.num:05}.jpeg'
    img.save(os.path.join(args.dir, filename))
    print(f'Image saved: {filename}')
    with lock:
        counters.bytes_downloaded += meta
        counters.counter += 1


def setup_parser():
    parser = argparse.ArgumentParser(description='download and process images in multiple threads')

    parser.add_argument('urllist', nargs='?', default='.', type=valid_urllist, help='path to file with urls')
    parser.add_argument('--dir', default='.', nargs='?', type=valid_dir, help='specify destination directory')
    parser.add_argument('--threads', default='1', nargs='?', type=int, help='specify number of threads')
    parser.add_argument('--size', default='100x100', nargs='?', type=valid_size, help='define maximum image size')

    return parser.parse_args()


def main():
    args = setup_parser()
    counters = Counters()
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }
    Lines = namedtuple('Lines', ['num', 'url'])

    with open(args.urllist, 'r') as fnm:
        lines = (Lines(num, url) for num, url in enumerate(fnm.readlines(), 1))

    lock = Lock()
    func = partial(download_image, args, headers, lock, counters)
    start_time = time.time()
    pool = ThreadPool(args.threads)
    pool.map(func, lines)
    pool.close()
    pool.join()
    stop_time = time.time() - start_time

    print('----')
    print(f'Images Saved: {counters.counter}')
    print(f'Bytes Downloaded: {counters.bytes_downloaded}')
    print(f'Saving Images Failed: {counters.error_counter}')
    print(f'Time spent: {round(stop_time, 2)} sec')


class Counters:
    counter = 0
    error_counter = 0
    bytes_downloaded = 0

if __name__ == '__main__':
    main()
