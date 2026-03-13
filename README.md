# path_tools
**The "path_tools.py" library**, is a multi-OS Python library, that includes advanced path filtering functions and\
the "recursive_copy_with_progress()" function, that displays a progress bar and an ETA, while recursively copying files.

## **The "recursive_copy_with_progress()" Function:**
### **Syntax:** 
#### recursive_copy_with_progress(SOURCE_PATH, DESTINATION_PATH)
### **Description:**
This function, first calculates and displays the total number of files and bytes to be copied, from a folder path, then recursively copies all files and folders,
within the chosen folder path, while displaying a live progress bar and an ETA, until finished.

### **Example:**
![Alt text](Images/recursive_copy_with_progress.png)
