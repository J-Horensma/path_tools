from Library.path_tools import is_safely_quoted, appropriate_quotes

try:
    PATH = input('Enter a path: ')
    if is_safely_quoted(PATH):
        print(f'Correct: {appropriate_quotes(PATH)}')
    else:
        print(f'Incorrectly quoted path: {PATH}')
        print(f'Changed to: {appropriate_quotes(PATH)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
    




        
