# path_tools
**The "path_tools" library**, is a multi-OS Python library, that includes advanced path-related functions.

## **The "recursive_copy_with_progress()" Function:**
### **Syntax:** 
#### recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH)
### **Description:**
**1.)** Removes or replaces OS-inappropriate or unneccessary quotes, OS-specific variables, and dot-sequences, in the SOURCE_PATH or DESTINATION_PATH variables, passed to it, OS-appropriately, with path_tools' built-in "filter_path()", "appropriate_quotes()", and "unquote_path()" functions, as well as, the help of the "os", "platform", and "pathlib" modules\
**2.)** Calculates and displays the total number of files and bytes to be copied, from the source path, using path_tools' built-in "recursive_files_and_bytes_total()", "convert_bytes()" functions, and the help of, the "os" module\
**3.)** Creates a new directory, in the destination path, matching the source path's folder name, using the "os" module, if the folder does not already exists in the destination path, if it does exist, in the destination path, a new directory, with a new name, is created, in the destination path\
**4.)** Recursively copies all files and folders within the chosen source path, to the destination path, with the source path folder's or new folder's name appended,\
to the destination path, while displaying a live progress bar and an ETA, until finished, with path_tools' built-in "recursive_copy_progress_bar()", "convert_seconds()" functions, and the help of the, "sys", "shutil", and "time" modules\
**5.)** All of the above, can be done with a single "recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH)" function call, after importing the "path_tools" library (See the test file: "recursive_copy_with_progress.py", in the Tests folder)

### **Example:**
![Alt text](Images/recursive_copy_with_progress.png)
