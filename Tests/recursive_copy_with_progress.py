from Library.path_tools import recursive_copy_with_progress
    
try:
    print('The "recursive_copy_with_progress()" function,')
    print('recursively copies all files and folders, in the supplied source path,')
    print('and displays a progress bar, with an ETA\n')
    SOURCE_PATH = input('Enter a source path: ')
    DESTINATION_PATH = input('Enter a destination path: ')
    recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH)
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')