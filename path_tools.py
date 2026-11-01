import os, sys, platform, time
from os.path import expandvars
from pathlib import Path

'''FUNCTIONS WILL BE REPLACED WITH UPGRADED ONES'''

def convert_path(PATH):
    return str(Path(expandvars(PATH.strip())).resolve(strict=False))
    
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
