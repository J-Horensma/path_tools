import os
from Library.path_tools import recursive_files_and_bytes_total, convert_bytes

try:
    print('The "recursive_files_and_bytes_total()" function,')
    print('recursively scans a folder and returns the total number,')
    print('of files and bytes, in the folder\n')
    PATH = input('Enter a path: ')
    FILES_TOTAL, BYTES_TOTAL = recursive_files_and_bytes_total(PATH)
    print(f'Folder: {os.path.basename(PATH)}')
    print(f'Total files: {FILES_TOTAL}')
    print(f'Total amount of data: {convert_bytes(BYTES_TOTAL)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')