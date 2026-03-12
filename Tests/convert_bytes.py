from Library.path_tools import convert_bytes

try:
    print('The "convert_bytes()" function,')
    print('converts a number of bytes, to the correct format\n')
    BYTES = input('Enter a number, of bytes: ')
    print(f'Converted: {convert_bytes(BYTES)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')