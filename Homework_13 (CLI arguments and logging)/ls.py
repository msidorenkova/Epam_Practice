import argparse
import os
import logging
from typing import List


logging.basicConfig(
                    filename='ls.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(message)s'
                    )

parser = argparse.ArgumentParser(
                                 prog='Python ls',
                                 description='This script lists directory contents of files and directories.')

parser.add_argument('path', metavar='path', nargs='*', default='.')
parser.add_argument('--almost-all', '-A', action='store_true', help='do not ignore entries starting with . ')
parser.add_argument('--inode', '-i', action='store_true', help='print the index number of each file')
parser.add_argument('-S', action='store_true', help='sort by file size, largest first')
parser.add_argument('--reverse', '-r', action='store_true', help='reverse order while sorting')

args = parser.parse_args()

def check_path() -> List:
    '''Check if paths from user's input exist'''
    working_paths = []
    for pathname in args.path:
        if not os.path.isdir(pathname):
            print(f'Python ls: Cannot access {pathname}: No such file or directory')
            logging.info(f'Python ls: Cannot access {pathname}: No such file or directory')
        else:
            working_paths.append(pathname)
    working_paths.sort()
    return working_paths


def create_content_list(pathname) -> List:
    '''Create content list and sort it alphabetically'''
    contents = []
    if args.almost_all:
        for i in os.listdir(pathname):
            contents.append(i)
    elif not args.almost_all:
        for i in os.listdir(pathname):
            if not i.startswith('.'):
                contents.append(i)
    contents.sort(key=str.lower)
    return contents


def pretty_print(contents: List[str], path):
    '''Print directory contents in one or more columns depending on terminal size
    :param contents: List of directory contents (files and directories)
    '''
    logging.info(f"Python ls: {len(contents)} objects in {path}")

    rows, columns = os.get_terminal_size()
    max_width = len(max(contents, key=len))+2

    x = max(1, int(len(contents)/int(rows/max_width))+1)

    matrix = [[] for _ in range(x)]
    for ind in range(x):
        for num, element in enumerate(contents):
            if num % x == ind:
                matrix[ind].append(element)

    for row in matrix:
        row = ''.join(element.ljust(max_width) for element in row)
        print(row)

if __name__ == '__main__':
    logging.info(f"User's input: {args}")

    working_paths = check_path()
    if args.reverse:
        working_paths.reverse()

    for pathname in working_paths:
        contents = create_content_list(pathname)

        if len(args.path) > 1:
            print(pathname+':')

        if contents:
            if args.S:
                contents.sort(key=lambda x: os.stat(os.path.join(pathname, x)).st_size, reverse=True)

            if args.inode:
                for i, filename in enumerate(contents):
                    contents[i] = '{} {}'.format(os.stat(os.path.join(pathname, filename)).st_ino, filename)

            if args.reverse:
                contents.reverse()

            pretty_print(contents, pathname)
        else:
            logging.info(f"Python ls: empty directory")
