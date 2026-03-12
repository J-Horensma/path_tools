from Library.path_tools import is_safely_quoted, appropriate_quotes

try: 
    print('The "appropriate_quotes()" function,')
    print('replaces and/or removes,incorrectly placed quotes, in the supplied path\n')
    PATH = input('Enter a path: ')
    if is_safely_quoted(PATH):
        print(f'Correct: {appropriate_quotes(PATH)}')
    else:
        print(f'Incorrect: {PATH}')
        print(f'Corrected: {appropriate_quotes(PATH)}')
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
    



        