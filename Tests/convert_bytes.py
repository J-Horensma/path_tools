from Library.path_tools import convert_bytes

try:
    BYTES = input('Enter a number, of bytes: ')
    print(f'Converted: {convert_bytes(BYTES)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
