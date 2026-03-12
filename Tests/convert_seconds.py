from Library.path_tools import convert_seconds

try:
    print('The "convert_seconds()" function,')
    print('converts a number of seconds, to y:M:d:h:m:s format\n')
    SECONDS = input('Enter a number, of seconds: ')
    print(f'Converted: {convert_seconds(SECONDS)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')