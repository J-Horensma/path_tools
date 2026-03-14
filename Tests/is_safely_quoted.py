from Library.path_tools import is_safely_quoted

try:
    PATH = input('Enter a path: ')
    print(f'Is safely quoted?: {is_safely_quoted(PATH)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
