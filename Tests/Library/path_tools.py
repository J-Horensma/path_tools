import os, shutil, sys, platform, time
from pathlib import Path

#RETURNS "True", IF THE SUPPLIED PATH,
#IS OS-APPROPRIATELY AND CORRECTLY QUOTED, OTHERWISE, "False"
def is_safely_quoted(PATH):
    STRIPPED = str(PATH).strip()
    if STRIPPED and isinstance(STRIPPED, str):
        OS_QUOTE = '"' if platform.system() == 'Windows' else "'"
        PREPENDED_QUOTES = int(0)
        for CHARACTER in STRIPPED:
            if CHARACTER in ["'", '"']:
                PREPENDED_QUOTES += 1
            else:
                break
        if os.path.isabs(STRIPPED[1:-1]) and ' ' in STRIPPED and STRIPPED.startswith(OS_QUOTE) and STRIPPED.endswith(OS_QUOTE) and STRIPPED.count(OS_QUOTE) == int(2) and PREPENDED_QUOTES < int(2):
            return True
        elif ' ' not in STRIPPED and OS_QUOTE not in STRIPPED and PREPENDED_QUOTES == int(0):
            return True
        else:
            return False
    else:
        raise TypeError('is_safely_quoted():\nThe PATH variable, must be a string and cannot be empty')

#OS-APPROPRIATELY, QUOTES A SUPPLIED PATH
#AND FIXES INCORRECT QUOTING
def appropriate_quotes(PATH):
    STRIPPED = str(PATH).strip()
    if STRIPPED and isinstance(STRIPPED, str):
        if is_safely_quoted(STRIPPED):
            return STRIPPED
        else:
            NON_OS_QUOTE = "'" if platform.system() == 'Windows' else '"'
            OS_QUOTE = '"' if platform.system() == 'Windows' else "'"
            PREPENDED_QUOTES = int(0)
            MATCHED_QUOTES = int(0)
            for CHARACTER in STRIPPED:
                if CHARACTER in ["'", '"']:
                    PREPENDED_QUOTES += 1
                    if CHARACTER == STRIPPED[-PREPENDED_QUOTES]:
                        MATCHED_QUOTES += 1
                else:
                    break
            STRIPPED = STRIPPED[PREPENDED_QUOTES:-MATCHED_QUOTES].replace(OS_QUOTE, NON_OS_QUOTE) if MATCHED_QUOTES > int(0) else STRIPPED[PREPENDED_QUOTES:].replace(OS_QUOTE, NON_OS_QUOTE)
            APPROPRIATED = f'{OS_QUOTE}{STRIPPED}{OS_QUOTE}' if ' ' in STRIPPED else STRIPPED.replace(OS_QUOTE, NON_OS_QUOTE)
            return APPROPRIATED
    else:
        raise TypeError('appropriate_quotes():\nThe PATH variable, must be a string and cannot be empty')
    
#UNQUOTES, THE SUPPLIED PATH
def unquote_path(PATH):
    STRIPPED = str(PATH).strip()
    if STRIPPED and isinstance(STRIPPED, str):
        OS_QUOTE = '"' if platform.system() == 'Windows' else "'"
        if STRIPPED[0] == OS_QUOTE and STRIPPED[0] == STRIPPED[-1]:
            return STRIPPED[1:-1]
        else:
            return STRIPPED
    else:
        raise TypeError('unquote_path():\nThe PATH variable, must be a string and cannot be empty')

#UNQUOTES, STRIPS, EXPANDS VARIABLES, 
#RESOLVES, AND REMOVES THE PREPENDED PATHLIB PATH (IF ANY),
#FROM THE SUPPLIED PATH
def filter_path(PATH):
    APPROPRIATELY_QUOTED = appropriate_quotes(PATH)
    STRIPPED = unquote_path(APPROPRIATELY_QUOTED)
    if STRIPPED and isinstance(STRIPPED, str):
        PATHLIB_PATH = str(Path.cwd())
        EXPANDED_VARIABLES = str(os.path.expandvars(STRIPPED))
        RESOLVED = str(Path(EXPANDED_VARIABLES).resolve(strict=False))
        STRIP_LENGTH = int(0) if int(len(PATHLIB_PATH)) == int(0) else int(len(PATHLIB_PATH)) + int(1)
        if not os.path.isabs(EXPANDED_VARIABLES) and RESOLVED.lower().startswith(PATHLIB_PATH.lower()):
            FILTERED = RESOLVED[STRIP_LENGTH:]
        else:
            FILTERED = RESOLVED
        return FILTERED
    else:
        raise TypeError('filter_path():\nThe PATH variable, must be a string and cannot be empty')
    
#RECURSIVELY SCANS A FOLDER PATH, FOR THE TOTAL NUMBER, OF FILES AND BYTES
def recursive_files_and_bytes_total(PATH):
    STRIPPED = filter_path(PATH)
    if all([STRIPPED, isinstance(STRIPPED, str), os.path.exists(STRIPPED), os.path.isdir(STRIPPED)]):
        FILES_TOTAL = int(0)
        BYTES_TOTAL = int(0)

        #LOOP THROUGH FOLDERS, IN THE PATH, RECURSIVELY
        for WALK_PATH, DIRECTORIES, FILES in os.walk(STRIPPED):
            
            #REMOVE HIDDEN AND LINK FILES, FROM FILES ARRAY
            FILES = [FILE for FILE in FILES if not FILE.startswith('.') and not os.path.islink(os.path.join(WALK_PATH, FILE))]

            #LOOP THROUGH FILES, IN THE DIRECTORY LOOP
            for FILE in FILES:
                FILES_TOTAL += int(1)
                SCAN_PATH = str(os.path.join(WALK_PATH, FILE))
                FILE_SIZE = int(os.path.getsize(SCAN_PATH))
                BYTES_TOTAL += FILE_SIZE
        return FILES_TOTAL, BYTES_TOTAL
    elif not STRIPPED or not isinstance(STRIPPED, str):
        raise TypeError('recursive_files_and_bytes_total():\nThe PATH variable, must be a string and cannot be empty')
    elif not os.path.exists(STRIPPED):
        raise FileNotFoundError(f'recursive_files_and_bytes_total():\nThe path: {STRIPPED}\nwas not found')
    elif os.path.isfile(PATH):
        raise NotADirectoryError('recursive_files_and_bytes_total():\nThe PATH variable, must be a folder path')

#CONVERT BYTES, TO OTHER MEASUREMENTS, IN BINARY FORMAT
def convert_bytes(BYTES):
    STRIPPED = str(BYTES).strip()
    if STRIPPED and STRIPPED.isnumeric():
        BYTES = int(STRIPPED)
        BINARY_INCREMENT = int(1024)
        if BYTES < BINARY_INCREMENT:return f'{BYTES} b'
        KILOBYTES = f'{round(BYTES/BINARY_INCREMENT, 2)}'
        if BYTES >= BINARY_INCREMENT and BYTES < BINARY_INCREMENT ** 2:return f'{KILOBYTES} kb'
        MEGABYTES = round(BYTES/(BINARY_INCREMENT ** 2), 2)
        if BYTES >= (BINARY_INCREMENT ** 2) and BYTES < BINARY_INCREMENT ** 3:return f'{MEGABYTES} Mb'
        GIGABYTES = round(BYTES/(BINARY_INCREMENT ** 3), 2)
        if BYTES >= (BINARY_INCREMENT ** 3) and BYTES < BINARY_INCREMENT ** 4:return f'{GIGABYTES} Gb'
        TERABYTES = round(BYTES/(BINARY_INCREMENT ** 4), 2)
        return f'{round(TERABYTES, 2)} Tb'
    else:
        raise TypeError('convert_bytes():\nThe BYTES variable, must be an integer and cannot be empty')
    
#CONVERTS SECONDS TO FULL TIME FORMAT
def convert_seconds(SECONDS):
    STRIPPED = str(SECONDS).strip()
    if STRIPPED and STRIPPED.isnumeric():
        SECONDS = int(STRIPPED)
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
    else:
        raise TypeError('convert_seconds():\nThe SECONDS variable, must be an integer and cannot be empty')
    
#DISPLAY A PROGRESS BAR, FOR THE "recursive_copy_with_progress()" FUNCTION   
def recursive_copy_progress_bar(COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS, LENGTH = int(30)):
    COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS = str(COPIED_BYTES).strip(), str(TOTAL_BYTES).strip(), str(ETA_SECONDS).strip()
    if all([COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS, COPIED_BYTES.isnumeric(), TOTAL_BYTES.isnumeric(), ETA_SECONDS.isnumeric()]):
        COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS = int(COPIED_BYTES), int(TOTAL_BYTES), int(ETA_SECONDS)
        PERCENT = (COPIED_BYTES / TOTAL_BYTES) * int(100)
        BARS_FILLED = (LENGTH * COPIED_BYTES) // TOTAL_BYTES
        PROGRESS_BAR = '=' * BARS_FILLED + '-' * (LENGTH - BARS_FILLED)
        ETA = convert_seconds(ETA_SECONDS)
        sys.stdout.write(f'\rProgress: [{PROGRESS_BAR}]({round(PERCENT)}%) ETA: {ETA.ljust(50)}')
        sys.stdout.flush()
    elif not all([COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS]):
        raise EOFError('recursive_copy_progress_bar():\nOne or more empty variables, were supplied')
    elif not all([COPIED_BYTES.isnumeric(), TOTAL_BYTES.isnumeric(), ETA_SECONDS.isnumeric()]):
        raise TypeError('recursive_copy_progress_bar():\nOne or more non-integer variables, were supplied')   
    if PERCENT == int(100.0):
        print('\nFinished!')

#RECURSIVELY COPIES A SUPPLIED SOURCE PATH, TO A DESTINATION PATH,
#WHILE SKIPPING NON-FILES, THAT CANNOT BE COPIED, LIKE SYM-LINKS
def recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH):
    if str(SOURCE_PATH).strip() and str(DESTINATION_PATH).strip():
        FILTERED_SOURCE_PATH = filter_path(SOURCE_PATH)
        FILTERED_DESTINATION_PATH = filter_path(DESTINATION_PATH)
        if os.path.exists(FILTERED_SOURCE_PATH) and os.path.exists(FILTERED_DESTINATION_PATH):
            TOTAL_FILES, TOTAL_BYTES = recursive_files_and_bytes_total(FILTERED_SOURCE_PATH)
            print(f'Copying a total of: {TOTAL_FILES} files and {convert_bytes(TOTAL_BYTES)}, of data')
            COPIED_FILES = int(0)
            COPIED_BYTES = int(0)
            if os.path.isdir(FILTERED_SOURCE_PATH) and os.path.isdir(FILTERED_DESTINATION_PATH):
                FILTERED_DESTINATION_PATH = os.path.join(FILTERED_DESTINATION_PATH, os.path.basename(FILTERED_SOURCE_PATH))
                if FILTERED_SOURCE_PATH == FILTERED_DESTINATION_PATH or os.path.exists(FILTERED_DESTINATION_PATH):
                    i = int(0)
                    MAKE_DESTINATION_DIRECTORY = FILTERED_DESTINATION_PATH

                    #CHECK IF THE FOLDER ALREADY EXISTS, IN THE DESTINATION PATH,
                    #AND MAKE A NEW ONE, WITH A DIFFERENT NAME, IF SO
                    while os.path.exists(MAKE_DESTINATION_DIRECTORY) == True:
                        i += int(1)
                        MAKE_DESTINATION_DIRECTORY = FILTERED_DESTINATION_PATH + ' ' + str(f'- Copy {i}').strip()
                    FILTERED_DESTINATION_PATH = MAKE_DESTINATION_DIRECTORY
                
                #MAKE THE FOLDER, IN THE DESTINATION PATH
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
                raise NotADirectoryError('recursive_copy_with_progress():\nOne or more supplied paths, were not a folder')
        else:
            raise FileNotFoundError(f'recursive_copy_with_progress():\nOne or more supplied paths, were not found')
    else:
        raise EOFError('recursive_copy_with_progress():\nOne or more empty variables, were supplied')
