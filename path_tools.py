import os, sys, platform, time
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

#THIS FUNCTION:
#1.) REQUIRES A PATH STRING
#2.) CHECKS IF THE PATH IS A NORMAL PATH
#3.) RETURNS "True" OR "False"
def is_normal(PATH):
    try:
        PATH = abspath(PATH)
        #CHECK IF THE PATH IS A FIFO, MOUNTPOINT, SOCKET, JUNCTION, SYMLINK, CLOUD-PLACEHOLDER, VIRTUALIZATION, DOOR, OR WHITEOUT
        PATH_STATUS = Path(PATH).lstat()
        PATH_MODE = PATH_STATUS.st_mode
        if not any([S_ISDIR(PATH_MODE), S_ISREG(PATH_MODE)]):
            return False
        elif system() == 'Windows':
            #CHECK IF THE PATH, IS A HIDDEN, SYSTEM, OR REPARSE-POINT PATH
            WINDOWS_FILE_ATTRIBUTE_HIDDEN = 0x2
            WINDOWS_FILE_ATTRIBUTE_SYSTEM = 0x4
            WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
            WINDOWS_FILE_ATTRIBUTES = PATH_STATUS.st_file_attributes
            if WINDOWS_FILE_ATTRIBUTES & WINDOWS_FILE_ATTRIBUTE_SYSTEM:
                return False
            elif WINDOWS_FILE_ATTRIBUTES & WINDOWS_FILE_ATTRIBUTE_HIDDEN:
                return False
            elif WINDOWS_FILE_ATTRIBUTES & WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT:
                return False
        return True
    except:
        return False

#THIS FUNCTION:
#1.) REQUIRES A PATH STRING AND A PERMISSION(S) STRING CONTAINING "R" (READ) "W" (WRITE) AND/OR "X" (EXECUTE)
#2.) CHECKS IF THE SUPPLIED PATH, HAS THE REQUESTED PERMISSION(S)
#3.) RETURNS "True" OR "False"
def has_permissions(PATH, PERMISSIONS):
    try:
        PATH = abspath(PATH)
        #ENSURE R, W, AND/OR X ARE INCLUDED, IN THE PERMISSIONS PARAMETER
        if not set(PERMISSIONS) <= {'R','W','X'}:
            return False
        #CHECK STATIC METADATA PERMISSIONS
        elif 'R' in PERMISSIONS and not access(PATH, R_OK):
            return False
        elif 'W' in PERMISSIONS and not access(PATH, W_OK):
            return False
        elif 'X' in PERMISSIONS and not access(PATH, X_OK):
            return False
        elif system() == 'Windows':
            #CHECK WINDOWS DYNAMIC METADATA PERMISSIONS
            from ctypes import wintypes, WinDLL
            GENERIC_READ  = 0x80000000
            FILE_SHARE_READ = 0x00000001
            FILE_SHARE_WRITE = 0x00000002
            FILE_SHARE_DELETE = 0x00000004
            OPEN_EXISTING = 3
            FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
            kernel32 = WinDLL('kernel32', use_last_error=True)
            CreateFileW = kernel32.CreateFileW
            CreateFileW.argtypes = [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.LPVOID,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.HANDLE
            ]
            CreateFileW.restype = wintypes.HANDLE
            def can_access(PATH):
                HANDLE = CreateFileW(
                    PATH,
                    GENERIC_READ,
                    FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
                    None,
                    OPEN_EXISTING,
                    FILE_FLAG_BACKUP_SEMANTICS,
                    None
                )
                if HANDLE == wintypes.HANDLE(-1).value:
                    return False
                kernel32.CloseHandle(HANDLE)
                return True
            if not can_access(PATH):
                return False
        return True
    except:
        return False
        
#THIS FUNCTION:
#1.) REQUIRES A FOLDER PATH STRING
#2.) RECURSIVELY SCANS THE PATH
#3.) RETURNS ABSOLUTE FOLDER PATH AND ABSOLUTE FILE PATH LISTS, TOTAL AMOUNT OF ACCESSABLE FILE(S) INTEGER, AND A BYTES TOTAL STRING FOR ALL FILE(S)
def recursive_files_and_bytes_total(FOLDER_PATH):
    if not isabs(FOLDER_PATH):
        raise ValueError('[ValueError]\nFunction: "recursive_files_and_bytes_total()"\nThe folder path parameter must be an absolute path.')
    elif not isdir(FOLDER_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "recursive_files_and_bytes_total()"\nThe folder path parameter must be a path to an existing folder.')
    try:
        FOLDER_PATH = abspath(FOLDER_PATH)
        ABSOLUTE_FOLDER_PATHS = []
        ABSOLUTE_FILE_PATHS = []
        FILES_TOTAL = 0
        BYTES_TOTAL = 0
        for ROOT, FOLDER_NAMES, FILE_NAMES in walk(FOLDER_PATH):
            FOLDER_NAMES = [FOLDER_NAME for FOLDER_NAME in FOLDER_NAMES]
            FILE_NAMES = [FILE_NAME for FILE_NAME in FILE_NAMES if all([is_normal(join(ROOT, FILE_NAME)), has_permissions(join(ROOT, FILE_NAME), 'RW')])]
            for FOLDER_NAME in FOLDER_NAMES:
                ABSOLUTE_FOLDER_PATH = abspath(join(ROOT, FOLDER_NAME))
                ABSOLUTE_FOLDER_PATHS.append(ABSOLUTE_FOLDER_PATH)
            for FILE_NAME in FILE_NAMES:
                FILES_TOTAL += 1
                ABSOLUTE_FILE_PATH = abspath(join(ROOT, FILE_NAME))
                ABSOLUTE_FILE_PATHS.append(ABSOLUTE_FILE_PATH)
                FILE_SIZE = getsize(ABSOLUTE_FILE_PATH)
                BYTES_TOTAL += FILE_SIZE
        return ABSOLUTE_FOLDER_PATHS, ABSOLUTE_FILE_PATHS, FILES_TOTAL, BYTES_TOTAL
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "recursive_files_and_bytes_total()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES A BYTES NUMBER STRING OR INTEGER
#2.) CONVERTS THE SUPPLIED BYTES NUMBER
#3.) RETURNS THE CONVERTED BYTES AS A STRING
def convert_bytes(BYTES_NUMBER):
    if not isinstance(BYTES_NUMBER, (str, int)):
        raise TypeError('[TypeError]\nFunction: "convert_bytes()"\nThe bytes number parameter must be a string or integer type.')
    try:
        BINARY_INCREMENT = 1024
        if BYTES_NUMBER < BINARY_INCREMENT:return f'{BYTES_NUMBER} Bytes'
        KILOBYTES = f'{round(BYTES_NUMBER/BINARY_INCREMENT, 2)}'
        if BYTES_NUMBER >= BINARY_INCREMENT and BYTES_NUMBER < BINARY_INCREMENT ** 2:return f'{KILOBYTES} KB'
        MEGABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 2), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 2) and BYTES_NUMBER < BINARY_INCREMENT ** 3:return f'{MEGABYTES} MB'
        GIGABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 3), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 3) and BYTES_NUMBER < BINARY_INCREMENT ** 4:return f'{GIGABYTES} GB'
        TERABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 4), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 4) and BYTES_NUMBER < BINARY_INCREMENT ** 5:return f'{TERABYTES} TB'
        PETABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 5), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 5) and BYTES_NUMBER < BINARY_INCREMENT ** 6:return f'{PETABYTES} PB'
        EXABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 6), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 6) and BYTES_NUMBER < BINARY_INCREMENT ** 7:return f'{EXABYTES} EB'
        ZETTABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 7), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 7) and BYTES_NUMBER < BINARY_INCREMENT ** 8:return f'{ZETTABYTES} ZB'
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "convert_bytes()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')
    
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
                    COPIED_BYTES = 0
                    for WALK_PATH, DIRECTORIES, FILES in os.walk(SOURCE_PATH):
                        RELATIVE_DIRECTORY = os.path.relpath(WALK_PATH, SOURCE_PATH)
                        SUB_DESTINATION_DIRECTORY = os.path.join(DESTINATION_PATH, RELATIVE_DIRECTORY)
                        os.makedirs(SUB_DESTINATION_DIRECTORY, exist_ok=True)

                        #REMOVE HIDDEN AND SYM-LINK FILES, FROM THE FILES LIST
                        FILES = [FILE_NAME for FILE_NAME in FILES if not FILE_NAME.startswith('.') and not os.path.islink(os.path.join(WALK_PATH, FILE_NAME))]
                        
                        for FILE_NAME in FILES:
                            SOURCE_FILE_PATH = os.path.join(WALK_PATH, FILE_NAME)
                            DESTINATION_FILE_PATH = os.path.join(SUB_DESTINATION_DIRECTORY, FILE_NAME)
                            with open(SOURCE_FILE_PATH, 'rb') as FILE_SOURCE, open(DESTINATION_FILE_PATH, 'wb') as FILE_DESTINATION:
                                BUFFER_SIZE = (1024 * 1024 * 2)
                                while True:
                                    DATA_CHUNK = FILE_SOURCE.read(BUFFER_SIZE)
                                    if not DATA_CHUNK:
                                        break
                                    else:
                                        FILE_DESTINATION.write(DATA_CHUNK)
                                        COPIED_BYTES += len(DATA_CHUNK)
                                    COPY_COMPLETE = time.time()
                                    ELAPSED_SECONDS = float(COPY_COMPLETE - START_COPY)
                                    BYTES_PER_SECOND = (COPIED_BYTES / ELAPSED_SECONDS)
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
