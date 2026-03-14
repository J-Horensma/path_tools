from Library.path_tools import unquote_path

try:
    PATH = input('Enter a path: ')
    print(f'Unquoted path: {unquote_path(PATH)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
