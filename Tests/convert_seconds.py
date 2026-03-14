from Library.path_tools import convert_seconds

try:
    SECONDS = input('Enter a number, of seconds: ')
    print(f'Converted: {convert_seconds(SECONDS)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
