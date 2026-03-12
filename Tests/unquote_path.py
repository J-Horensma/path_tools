from Library.path_tools import unquote_path

try:
    print('The "unquote_path()" function,')
    print('removes only the quote, at the beginning and end,') 
    print('of the supplied path (If both quotes, are present)\n')
    PATH = input('Enter a path: ')
    print(f'Unquoted path: {unquote_path(PATH)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
