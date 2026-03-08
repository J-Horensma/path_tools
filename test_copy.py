import path_tools

try:
    SOURCE_PATH = input('Enter a source path: ')
    DESTINATION_PATH = input('Enter a destination path: ')
    SOURCE_PATH_FILES_TOTAL, SOURCE_PATH_BYTES_TOTAL = path_tools.recursive_files_and_bytes_total(SOURCE_PATH)
    print(f'Copying a total of: {SOURCE_PATH_FILES_TOTAL} files and {path_tools.convert_bytes(SOURCE_PATH_BYTES_TOTAL)}')
    path_tools.recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH)
except Exception as ERROR:
    print(ERROR)
input('Press Enter: ')