import os
from Library.path_tools import recursive_files_and_bytes_total, convert_bytes

try:
    PATH = input('Enter a path: ')
    FILES_TOTAL, BYTES_TOTAL = recursive_files_and_bytes_total(PATH)
    print(f'Total files: {FILES_TOTAL}')
    print(f'Total amount of data: {convert_bytes(BYTES_TOTAL)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
