from Library.path_tools import is_safely_quoted

try: 
    print('The "is_safely_quoted()" function,')
    print('returns True, if the supplied path,')
    print('is correctly quoted (Or correctly not), otherwise False\n')
    PATH = input('Enter a path: ')
    print(f'Is safely quoted?: {is_safely_quoted(PATH)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')