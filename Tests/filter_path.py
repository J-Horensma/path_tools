from Library.path_tools import filter_path

try:
    PATH = input('Enter a path: ')
    FILTERED = filter_path(PATH)
    print(f'Filtered path: {FILTERED}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')

