import os, sys, time, shutil

#CONVERT BYTES, TO PROPER INCREMENTS, IN BINARY FORMAT
def convert_bytes(BYTES):
    if str(BYTES).strip() and isinstance(BYTES, int):
        BINARY_INCREMENT = int(1024)
        if BYTES < BINARY_INCREMENT:return f'{BYTES} b'
        KILOBYTES = f'{round(BYTES/BINARY_INCREMENT, 2)}'
        if BYTES >= BINARY_INCREMENT and BYTES < BINARY_INCREMENT ** 2:return f'{KILOBYTES} kb'
        MEGABYTES = round(BYTES/(BINARY_INCREMENT ** 2), 2)
        if BYTES >= (BINARY_INCREMENT ** 2) and BYTES < BINARY_INCREMENT ** 3:return f'{MEGABYTES} Mb'
        GIGABYTES = round(BYTES/(BINARY_INCREMENT ** 3), 2)
        if BYTES >= (BINARY_INCREMENT ** 3) and BYTES < BINARY_INCREMENT ** 4:return f'{GIGABYTES} Gb'
        TERABYTES = round(BYTES/(BINARY_INCREMENT ** 4), 2)
        return f'{TERABYTES} Tb'
    elif not str(BYTES).strip():
        raise EOFError('convert_bytes():\nAn empty variable, was supplied.')
    elif not isinstance(BYTES, int):
        raise TypeError('convert_bytes():\nA non-integer, was supplied.')
    
#LOOP THROUGH A SET OF KEYS AND REPLACE THEM,
#WITH THEIR VALUES IN A STRING
def replace_string_dictionary(STRING, DICTIONARY):
    LAST_REPLACED_STRING = STRING
    for OLD, NEW in DICTIONARY.items():
        REPLACED_STRING = LAST_REPLACED_STRING.replace(OLD, NEW)
        LAST_REPLACED_STRING = REPLACED_STRING
    return REPLACED_STRING

#FILTER QUOTES, FROM A PATH, STRIP ANY SPACES FROM IT, AND CHECK IF THE PATH EXISTS
def filter(PATH):
    FILTERED_PATH = os.path.normpath(replace_string_dictionary(PATH, {"'":'', '"':'', ' ':''}))                     
    if FILTERED_PATH.strip('.') and os.path.exists(FILTERED_PATH):
        return FILTERED_PATH
    elif not str(PATH).strip():
        raise EOFError('filter():\nAn empty variable, was supplied.')
    else:
        raise FileNotFoundError(f'filter():\nThe path: {FILTERED_PATH}, was not found.')
    
#RECURSIVELY SCAN A FOLDER, FOR THE TOTAL FILES AND BYTES
def recursive_files_and_bytes_total(PATH):
    if all([str(PATH).strip(), isinstance(PATH, str), os.path.isdir(PATH)]):
        FILES_TOTAL = int(0)
        BYTES_TOTAL = int(0)

        #LOOP THROUGH FOLDERS, IN THE PATH, RECURSIVELY
        for WALK_PATH, DIRECTORIES, FILES in os.walk(PATH):
            
            #REMOVE HIDDEN AND LINK FILES, FROM FILES ARRAY
            FILES = [FILE for FILE in FILES if not FILE.startswith('.') and not os.path.islink(os.path.join(WALK_PATH, FILE))]

            #LOOP THROUGH FILES, IN THE DIRECTORY LOOP
            for FILE in FILES:
                FILES_TOTAL += int(1)
                SCAN_PATH = str(os.path.join(WALK_PATH, FILE))
                FILE_SIZE = int(os.path.getsize(SCAN_PATH))
                BYTES_TOTAL += FILE_SIZE
        return FILES_TOTAL, BYTES_TOTAL
    elif not str(PATH).strip():
        raise EOFError('recursive_files_and_bytes_total():\nAn empty variable, was supplied.')
    elif os.path.isfile(PATH):
        raise NotADirectoryError('recursive_files_and_bytes_total():\nThe path, was not a folder.')
    
#CONVERT SECONDS TO Y/M/W/D/H/M/S FORMAT
def convert_seconds(SECONDS):
    if all([str(SECONDS).strip(), isinstance(SECONDS, int)]):
        YEARS = f'{SECONDS // int(31536000)}y:' if (SECONDS // int(31536000)) > int(0) else ''
        REMAINDER_SECONDS = SECONDS % int(31536000)
        MONTHS = f'{REMAINDER_SECONDS // int(2628000)}M:' if (REMAINDER_SECONDS // int(2628000)) > int(0) else ''
        REMAINDER_SECONDS %= int(2628000)
        WEEKS = f'{REMAINDER_SECONDS // int(604800)}w:' if (REMAINDER_SECONDS // int(604800)) > int(0) else ''
        REMAINDER_SECONDS %= int(604800)
        DAYS = f'{REMAINDER_SECONDS // int(86400)}d:' if (REMAINDER_SECONDS // int(86400)) > int(0) else ''
        REMAINDER_SECONDS %= int(86400)
        HOURS = f'{REMAINDER_SECONDS // int(3600)}h:' if (REMAINDER_SECONDS // int(3600)) > int(0) else ''
        REMAINDER_SECONDS %= int(3600)
        MINUTES = f'{REMAINDER_SECONDS // int(60)}m:' if (REMAINDER_SECONDS // int(60)) > int(0) else ''
        REMAINDER_SECONDS %= int(60)
        SECONDS = f'{REMAINDER_SECONDS % int(60)}s'
        CONVERTED_SECONDS = f'{YEARS}{MONTHS}{WEEKS}{DAYS}{HOURS}{MINUTES}{SECONDS}'
        return CONVERTED_SECONDS
    elif not str(SECONDS).strip():
        raise EOFError('convert_seconds():\nAn empty variable, was supplied.')
    elif not isinstance(SECONDS, int):
        raise TypeError('convert_seconds():\nA non-integer, was supplied.')

#DISPLAY PROGRESS BAR, FOR THE "recursiveCopyWithProgress()" FUNCTION   
def recursive_copy_progress_bar(COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS, LENGTH = int(30)):
    if all([str(COPIED_BYTES).strip(), str(TOTAL_BYTES).strip(), str(ETA_SECONDS).strip(), isinstance(COPIED_BYTES, int), isinstance(TOTAL_BYTES, int), isinstance(ETA_SECONDS, int)]):
        PERCENT = (COPIED_BYTES / TOTAL_BYTES) * int(100)
        BARS_FILLED = (LENGTH * COPIED_BYTES) // TOTAL_BYTES
        PROGRESS_BAR = '=' * BARS_FILLED + '-' * (LENGTH - BARS_FILLED)
        ETA = convert_seconds(ETA_SECONDS)
        sys.stdout.write(f'\rProgress: [{PROGRESS_BAR}]({round(PERCENT)}%) ETA: {ETA.ljust(50)}')
        sys.stdout.flush()
    elif not all([str(COPIED_BYTES).strip(), str(TOTAL_BYTES).strip(), str(ETA_SECONDS).strip()]):
        raise EOFError('recursive_copy_progress_bar():\nOne or more empty variables, were supplied.')
    elif not all([isinstance(COPIED_BYTES, int), isinstance(TOTAL_BYTES, int), isinstance(ETA_SECONDS, int)]):
        raise TypeError('recursive_copy_progress_bar():\nOne or more non-integer variables, were supplied.')   
    if PERCENT == int(100.0):
        print('\nFinished!')

#RECURSIVELY COPY, A FOLDER PATH
def recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH):
    FILTERED_SOURCE_PATH = filter(SOURCE_PATH)
    FILTERED_DESTINATION_PATH = os.path.join(filter(DESTINATION_PATH), os.path.basename(FILTERED_SOURCE_PATH))
    TOTAL_FILES, TOTAL_BYTES = recursive_files_and_bytes_total(FILTERED_SOURCE_PATH)
    COPIED_FILES = int(0)
    COPIED_BYTES = int(0)
    if os.path.isdir(FILTERED_SOURCE_PATH) and os.path.isdir(FILTERED_DESTINATION_PATH):
        if FILTERED_SOURCE_PATH == FILTERED_DESTINATION_PATH or os.path.exists(FILTERED_DESTINATION_PATH):
            i = int(0)
            MAKE_DESTINATION_DIRECTORY = FILTERED_DESTINATION_PATH
            while os.path.exists(MAKE_DESTINATION_DIRECTORY) == True:
                i += int(1)
                MAKE_DESTINATION_DIRECTORY = FILTERED_DESTINATION_PATH + ' ' + str(f'- Copy {i}').strip()
            FILTERED_DESTINATION_PATH = MAKE_DESTINATION_DIRECTORY
        os.makedirs(FILTERED_DESTINATION_PATH, exist_ok=True)
        START_COPY = time.time()
        for WALK_PATH, DIRECTORIES, FILES in os.walk(FILTERED_SOURCE_PATH):
            RELATIVE_DIRECTORY = os.path.relpath(WALK_PATH, FILTERED_SOURCE_PATH)
            SUB_DESTINATION_DIRECTORY = os.path.join(FILTERED_DESTINATION_PATH, RELATIVE_DIRECTORY)
            os.makedirs(SUB_DESTINATION_DIRECTORY, exist_ok=True)

            #REMOVE HIDDEN AND LINK FILES, FROM FILES ARRAY
            FILES = [FILE_NAME for FILE_NAME in FILES if not FILE_NAME.startswith('.') and not os.path.islink(os.path.join(WALK_PATH, FILE_NAME))]
            
            for FILE_NAME in FILES:
                SOURCE_FILE_PATH = os.path.join(WALK_PATH, FILE_NAME)
                BYTES = int(os.path.getsize(SOURCE_FILE_PATH))
                DESTINATION_FILE_PATH = os.path.join(SUB_DESTINATION_DIRECTORY, FILE_NAME)
                shutil.copy2(SOURCE_FILE_PATH, DESTINATION_FILE_PATH)
                
                COPY_COMPLETE = time.time()
                ELAPSED_SECONDS = float(COPY_COMPLETE - START_COPY)
                COPIED_FILES += int(1)
                COPIED_BYTES += BYTES
                BYTES_PER_SECOND = COPIED_BYTES / ELAPSED_SECONDS
                ETA_SECONDS =  int(f'{(TOTAL_BYTES - COPIED_BYTES) / BYTES_PER_SECOND:.0f}')
                
                recursive_copy_progress_bar(COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS)
        return
    else:
        raise NotADirectoryError('recursive_copy_with_progress():\nOne or more paths, were not a folder.')