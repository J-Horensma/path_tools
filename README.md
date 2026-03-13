# path_tools
**The "path_tools.py" library**, is a multi-OS Python library, that includes advanced path filtering functions and\
the "recursive_copy_with_progress()" function, that displays a progress bar and an ETA, while recursively copying files.

## **The "recursive_copy_with_progress()" Function:**
### **Syntax:** 
#### recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH)
### **Description:**
**1.)** Filters and/or replaces characters, OS variables, and dot-sequences, in the SOURCE_PATH or DESTINATION_PATH variables, passed to it, OS-appropriately, with path_tools' built-in "filter_path()", "appropriate_quotes()", and "unquote_path()" functions, as well as, the help of the "os", "platform", and "pathlib" modules\
**2.)** Calculates and displays the total number of files and bytes to be copied, from the SOURCE_PATH variable, using path_tools' built-in "recursive_files_and_bytes_total()", "convert_bytes()" functions, and the help of, the "os" module\
**3.)** Creates a new directory, in the destination path, matching the source path's folder name, using the "os" module, if the folder does not already exists in the destination path, if it does exist, in the destination path, a new directory, with a new name, is created, in the destination path\
**4.)** Recursively copies all files and folders within the chosen source path, to the destination path, with the source path folder's name appended,\
to the destination path, while displaying a live progress bar and an ETA, until finished, with path_tools' built-in "recursive_copy_progress_bar()", "convert_seconds()" functions, and the help of the, "sys", shutil, and "time" modules

### **Example:**
![Alt text](Images/recursive_copy_with_progress.png)
