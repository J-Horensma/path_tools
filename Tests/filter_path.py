from Library.path_tools import filter_path

try:
    print('The "filter_path()" function,')
    print('filters and converts, the supplied path\n') 
    PATH = input('Enter a path: ')
    FILTERED = filter_path(PATH)
    print(FILTERED)
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
