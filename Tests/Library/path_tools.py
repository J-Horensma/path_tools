import os, shutil, sys, platform, time
from pathlib import Path

#RETURNS "True", IF THE SUPPLIED PATH IS OS-APPROPRIATELY AND CORRECTLY QUOTED, OTHERWISE "False"
def is_safely_quoted(PATH):
    PATH = PATH.strip()
    if PATH:
        if isinstance(PATH, str):
            OS_QUOTE = '"' if platform.system() == 'Windows' else "'"
            PREPENDED_QUOTES = 0
            for CHARACTER in PATH:
                if CHARACTER in ["'", '"']:
                    PREPENDED_QUOTES += 1
                else:
                    break
            if os.path.isabs(PATH[1:-1]) and ' ' in PATH and PATH.startswith(OS_QUOTE) and PATH.endswith(OS_QUOTE) and PATH.count(OS_QUOTE) == 2 and PREPENDED_QUOTES < 2:
                return True
            elif ' ' not in PATH and OS_QUOTE not in PATH and PREPENDED_QUOTES == 0:
                return True
            else:
                return False
        else:
            raise TypeError('"is_safely_quoted()":\nThe "PATH" variable, must be a string')
    else:
        raise EOFError('"is_safely_quoted()":\nThe "PATH" variable, cannot be empty')

#OS-APPROPRIATELY QUOTES, A SUPPLIED PATH (IF A SPACE, IS PRESENT) AND FIXES INCORRECT QUOTING
def appropriate_quotes(PATH):
    PATH = PATH.strip()
    if PATH:
        if isinstance(PATH, str):
            if is_safely_quoted(PATH):
                return PATH
            else:
                NON_OS_QUOTE = "'" if platform.system() == 'Windows' else '"'
                OS_QUOTE = '"' if platform.system() == 'Windows' else "'"
                PREPENDED_QUOTES = 0
                MATCHED_QUOTES = 0
                for CHARACTER in PATH:
                    if CHARACTER in ["'", '"']:
                        PREPENDED_QUOTES += 1
                        if CHARACTER == PATH[-PREPENDED_QUOTES]:
                            MATCHED_QUOTES += 1
                    else:
                        break
                PATH = PATH[PREPENDED_QUOTES:-MATCHED_QUOTES].replace(OS_QUOTE, NON_OS_QUOTE) if MATCHED_QUOTES > 0 else PATH[PREPENDED_QUOTES:].replace(OS_QUOTE, NON_OS_QUOTE)
                PATH = f'{OS_QUOTE}{PATH}{OS_QUOTE}' if ' ' in PATH else PATH.replace(OS_QUOTE, NON_OS_QUOTE)
                return PATH
        else:
            raise TypeError('"appropriate_quotes()":\nThe "PATH" variable, must be a string')
    else:
        raise EOFError('"appropriate_quotes()":\nThe "PATH" variable, cannot be empty')
    
#UNQUOTES, THE FIRST INSTANCES, OF BEGINNING AND END QUOTES, OF THE SUPPLIED PATH
def unquote_path(PATH):
    PATH = PATH.strip()
    if PATH:
        if isinstance(PATH, str):
            QUOTES = ["'", '"']
            if PATH[0] in QUOTES and PATH[0] == PATH[-1]:
                return PATH[1:-1]
            else:
                return PATH
        else:
            raise TypeError('"unquote_path()":\nThe "PATH" variable, must be a string')
    else:
        raise EOFError('"unquote_path()":\nThe "PATH" variable, cannot be empty')

#STRIPS, EXPANDS VARIABLES, OS-NORMALIZES SLASHES, AND CONVERTS DOT-SEQUENCES, FROM THE SUPPLIED PATH
def filter_path(PATH):
    PATH = PATH.strip()
    if PATH:
        if isinstance(PATH, str):
            PATH = appropriate_quotes(PATH)
            PATH = unquote_path(PATH)
            PATHLIB_PATH = str(Path.cwd())
            PATH = os.path.expandvars(PATH)
            RESOLVED = str(Path(PATH).resolve(strict=False))
            STRIP_LENGTH = 0 if len(PATHLIB_PATH) == 0 else len(PATHLIB_PATH) + 1
            if not os.path.isabs(PATH) and RESOLVED.lower().startswith(PATHLIB_PATH.lower()):
                PATH = RESOLVED[STRIP_LENGTH:]
            else:
                PATH = RESOLVED
            return PATH
        else:
            raise TypeError('"filter_path()":\nThe "PATH" variable, must be a string')
    else:
        raise EOFError('"filter_path()":\nThe "PATH" variable, cannot be empty')
    
#RECURSIVELY SCANS A FOLDER PATH, FOR THE TOTAL NUMBER, OF FILES AND BYTES
def recursive_files_and_bytes_total(PATH):
    PATH = PATH.strip()
    if PATH:
        if isinstance(PATH, str):
            PATH = filter_path(PATH)
            if os.path.exists(PATH):
                if os.path.isdir(PATH):
                    FILES_TOTAL = 0
                    BYTES_TOTAL = 0

                    #LOOP THROUGH FOLDERS, IN THE PATH, RECURSIVELY
                    for WALK_PATH, DIRECTORIES, FILES in os.walk(PATH):
                        
                        #REMOVE HIDDEN AND LINK FILES, FROM THE FILES LIST
                        FILES = [FILE for FILE in FILES if not FILE.startswith('.') and not os.path.islink(os.path.join(WALK_PATH, FILE))]

                        #LOOP THROUGH FILES, IN THE FOLDER
                        for FILE in FILES:
                            FILES_TOTAL += 1
                            SCAN_PATH = os.path.join(WALK_PATH, FILE)
                            FILE_SIZE = os.path.getsize(SCAN_PATH)
                            BYTES_TOTAL += FILE_SIZE
                    return FILES_TOTAL, BYTES_TOTAL
                else:
                    raise NotADirectoryError('"recursive_files_and_bytes_total()":\nThe "PATH" variable, must be a path, to a folder')
            else:
                raise FileNotFoundError(f'"recursive_files_and_bytes_total()":\nThe path: {PATH}, was not found')
        else:
            raise TypeError('"recursive_files_and_bytes_total()":\nThe "PATH" variable, must be a string')
    else:
        raise EOFError('"recursive_files_and_bytes_total()":\nThe "PATH" variable, cannot be empty')

#CONVERTS BYTES, TO OTHER MEASUREMENTS, IN BINARY FORMAT
def convert_bytes(BYTES):
    BYTES = str(BYTES).strip()
    if BYTES:
        if BYTES.isnumeric():
            BYTES = int(BYTES)
            BINARY_INCREMENT = 1024
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
            raise TypeError('"convert_bytes()":\nThe "BYTES" variable, must be an integer')
    else:
        raise EOFError('"convert_bytes()":\nThe "BYTES" variable, cannot be empty')
    
#CONVERTS SECONDS TO FULL TIME FORMAT
def convert_seconds(SECONDS):
    SECONDS = str(SECONDS).strip()
    if SECONDS:
        if SECONDS.isnumeric():
            SECONDS = int(SECONDS)
            YEARS = f'{SECONDS // 31536000}y:' if (SECONDS // 31536000) > 0 else ''
            REMAINDER_SECONDS = SECONDS % 31536000
            MONTHS = f'{REMAINDER_SECONDS // 2628000}M:' if (REMAINDER_SECONDS // 2628000) > 0 else ''
            REMAINDER_SECONDS %= 2628000
            WEEKS = f'{REMAINDER_SECONDS // 604800}w:' if (REMAINDER_SECONDS // 604800) > 0 else ''
            REMAINDER_SECONDS %= 604800
            DAYS = f'{REMAINDER_SECONDS // 86400}d:' if (REMAINDER_SECONDS // 86400) > 0 else ''
            REMAINDER_SECONDS %= 86400
            HOURS = f'{REMAINDER_SECONDS // 3600}h:' if (REMAINDER_SECONDS // 3600) > 0 else ''
            REMAINDER_SECONDS %= 3600
            MINUTES = f'{REMAINDER_SECONDS // 60}m:' if (REMAINDER_SECONDS // 60) > 0 else ''
            REMAINDER_SECONDS %= 60
            SECONDS = f'{REMAINDER_SECONDS % 60}s'
            CONVERTED_SECONDS = f'{YEARS}{MONTHS}{WEEKS}{DAYS}{HOURS}{MINUTES}{SECONDS}'
            return CONVERTED_SECONDS
        else:
            raise TypeError('"convert_seconds()":\nThe "SECONDS" variable, must be an integer')
    else:
        raise EOFError('"convert_seconds()":\nThe "SECONDS" variable, cannot be empty')
    
#DISPLAY A PROGRESS BAR, FOR THE "recursive_copy_with_progress()" FUNCTION   
def recursive_copy_progress_bar(COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS, LENGTH = 30):
    COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS = str(COPIED_BYTES).strip(), str(TOTAL_BYTES).strip(), str(ETA_SECONDS).strip()
    if all([COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS]):      
        if all([COPIED_BYTES.isnumeric(), TOTAL_BYTES.isnumeric(), ETA_SECONDS.isnumeric()]):
            COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS = int(COPIED_BYTES), int(TOTAL_BYTES), int(ETA_SECONDS)
            PERCENT = (COPIED_BYTES / TOTAL_BYTES) * 100
            BARS_FILLED = (LENGTH * COPIED_BYTES) // TOTAL_BYTES
            PROGRESS_BAR = '=' * BARS_FILLED + '-' * (LENGTH - BARS_FILLED)
            ETA = convert_seconds(ETA_SECONDS)
            sys.stdout.write(f'\rProgress: [{PROGRESS_BAR}]({round(PERCENT)}%) ETA: {ETA.ljust(30)}')
            sys.stdout.flush()
        else:
            raise TypeError('"recursive_copy_progress_bar()":\nOne or more non-integer variables, were supplied')   
    else:
        raise EOFError('"recursive_copy_progress_bar()":\nOne or more empty variables, were supplied')
    if PERCENT == 100.0:
        print('\nFinished!')

#RECURSIVELY COPIES A SUPPLIED SOURCE PATH, TO A SUPPLIED DESTINATION PATH,
#WHILE SKIPPING FILES THAT CANNOT BE COPIED, LIKE HIDDEN AND SYM-LINK FILES
def recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH):
    SOURCE_PATH, DESTINATION_PATH = SOURCE_PATH.strip(), DESTINATION_PATH.strip()
    if SOURCE_PATH and DESTINATION_PATH:
        if isinstance(SOURCE_PATH, str) and isinstance(DESTINATION_PATH, str):
            SOURCE_PATH = filter_path(SOURCE_PATH)
            DESTINATION_PATH = filter_path(DESTINATION_PATH)
            if os.path.exists(SOURCE_PATH) and os.path.exists(DESTINATION_PATH):
                if os.path.isdir(SOURCE_PATH) and os.path.isdir(DESTINATION_PATH):
                    COPIED_FILES = 0
                    COPIED_BYTES = 0
                    TOTAL_FILES, TOTAL_BYTES = recursive_files_and_bytes_total(SOURCE_PATH)
                    print(f'Copying a total of: {TOTAL_FILES} files ({convert_bytes(TOTAL_BYTES)})')
                    DESTINATION_PATH = os.path.join(DESTINATION_PATH, os.path.basename(SOURCE_PATH))
                    if SOURCE_PATH == DESTINATION_PATH or os.path.exists(DESTINATION_PATH):
                        i = 0
                        MAKE_DESTINATION_DIRECTORY = DESTINATION_PATH

                        #CHECK IF THE FOLDER ALREADY EXISTS, IN THE DESTINATION PATH
                        #AND MAKE A NEW FOLDER, WITH A DIFFERENT NAME, IF SO
                        while os.path.exists(MAKE_DESTINATION_DIRECTORY) == True:
                            i += 1
                            MAKE_DESTINATION_DIRECTORY = DESTINATION_PATH + ' ' + str(f'- Copy {i}').strip()
                        DESTINATION_PATH = MAKE_DESTINATION_DIRECTORY
                    
                    #MAKE THE FOLDER, IN THE DESTINATION PATH
                    os.makedirs(DESTINATION_PATH, exist_ok=True)
                    START_COPY = time.time()
                    for WALK_PATH, DIRECTORIES, FILES in os.walk(SOURCE_PATH):
                        RELATIVE_DIRECTORY = os.path.relpath(WALK_PATH, SOURCE_PATH)
                        SUB_DESTINATION_DIRECTORY = os.path.join(DESTINATION_PATH, RELATIVE_DIRECTORY)
                        os.makedirs(SUB_DESTINATION_DIRECTORY, exist_ok=True)

                        #REMOVE HIDDEN AND SYM-LINK FILES, FROM THE FILES LIST
                        FILES = [FILE_NAME for FILE_NAME in FILES if not FILE_NAME.startswith('.') and not os.path.islink(os.path.join(WALK_PATH, FILE_NAME))]
                        
                        for FILE_NAME in FILES:
                            SOURCE_FILE_PATH = os.path.join(WALK_PATH, FILE_NAME)
                            BYTES = os.path.getsize(SOURCE_FILE_PATH)
                            DESTINATION_FILE_PATH = os.path.join(SUB_DESTINATION_DIRECTORY, FILE_NAME)
                            shutil.copy2(SOURCE_FILE_PATH, DESTINATION_FILE_PATH)
                            COPY_COMPLETE = time.time()
                            ELAPSED_SECONDS = float(COPY_COMPLETE - START_COPY)
                            COPIED_FILES += 1
                            COPIED_BYTES += BYTES
                            BYTES_PER_SECOND = COPIED_BYTES / ELAPSED_SECONDS
                            ETA_SECONDS =  int(f'{(TOTAL_BYTES - COPIED_BYTES) / BYTES_PER_SECOND:.0f}')
                            recursive_copy_progress_bar(COPIED_BYTES, TOTAL_BYTES, ETA_SECONDS)
                    return
                else:
                    raise NotADirectoryError('"recursive_copy_with_progress()":\nOne or more supplied paths, do not exist')
            else:
                raise FileNotFoundError(f'"recursive_copy_with_progress()":\nOne or more supplied paths, were not found')
        else:
            raise TypeError('"recursive_copy_with_progress()":\nOne or more non-string variables, were supplied')
    else:
        raise EOFError('"recursive_copy_with_progress()":\nOne or more empty variables, were supplied')
