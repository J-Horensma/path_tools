# path_tools
**The "path_tools.py" library**, is a multi-OS Python library, that includes advanced path filtering functions and\
the "recursive_copy_with_progress()" function, that displays a progress bar and an ETA, while recursively copying files.

## **The "recursive_copy_with_progress()" Function:**
### **Syntax:** 
#### recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH)
### **Description:**
**1.)** Filters and/or replaces characters, OS variables, and dot-sequences, in the SOURCE_PATH or DESTINATION_PATH variables, passed to it, OS-appropriately, with it's built-in filter_path() function and the help of the "os", "platform", and "pathlib" modules\
**2.)** Calculates and displays the total number of files and bytes to be copied, from the source path\
**3.)** Creates a new directory, in the destination path, matching the source path's folder name, if it already exists in the destination path,\
a new directory, with a new name, is created, to copy the files to\
**4.)** Recursively copies all files and folders within the chosen source path, while displaying a live progress bar and an ETA, until finished

### **Example:**
![Alt text](Images/recursive_copy_with_progress.png)
