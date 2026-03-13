from Library.path_tools import recursive_copy_with_progress
    
try:
    SOURCE_PATH = input('Enter a source path: ')
    DESTINATION_PATH = input('Enter a destination path: ')
    recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH)
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')
