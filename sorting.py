"""
    This script is used to sort files into folders in various different ways.
    Place this script in whatever directory you wish to sort.

    Sorting Styles:
    1) Year Created
    2) Substrings
    3) File Extension

    Renames duplicate files so they may be sorted out.

    By Aidan Clyens
"""
import os
from datetime import datetime

ACTIVE_DIRECTORY = os.getcwd()
MIN_YEAR = 2013
MAX_YEAR = int(datetime.today().year)

substrings_list = []
file_moved = {}
file_duplicate = {}

# Search through specified directory
def search(path, sort_years, substr_sort, del_directory, sub_string):
    # Search files
    for root, dirs, files in os.walk(path, topdown = True):
        for name in files:
            print('File: ' + os.path.join(root, name))

            file_moved[os.path.join(root, name)] = False

            if sort_years:
                year_sort(os.path.join(root, name))

            if substr_sort:
                substring_sort(os.path.join(root, name), sub_string)

    # Search folder
    for root, dirs, files in os.walk(path, topdown = True):
        for name in dirs:
            if del_directory:
                # Delete empty subdirectories first
                sub_dirs = os.listdir(os.path.join(root, name))
                for d in sub_dirs:
                    if os.path.isdir(os.path.join(root, name, d)): print('Dir: ' + os.path.join(root, name, d))
                    del_empty_dirs(os.path.join(root, name, d))

                del_empty_dirs(os.path.join(root, name))

            print('Dir: ' + os.path.join(root, name))

# Sort by year in file name
def year_sort(file_name):
    count = 0
    year = MIN_YEAR

    # Do not sort this script
    if not os.path.basename(file_name) == 'sorting.py':
        while not year > MAX_YEAR:
            year =  MIN_YEAR + count
            # Check if the first 4 characters contain a year
            file_name_start = os.path.basename(file_name)[:4]
            if str(year) in file_name_start and file_moved[file_name] == False:
                folder = os.path.join(ACTIVE_DIRECTORY, str(year))
                make_dirs(folder)
                move_files(file_name, folder)

            count += 1

        if file_moved[file_name] == False:
            year_sort_backup(file_name)

# Sort by year file was created
def year_sort_backup(file_name):
    ctime = os.path.getctime(file_name)
    year = datetime.fromtimestamp(ctime).strftime('%Y')

    # Do not sort this script
    if not os.path.basename(file_name) == 'sorting.py':
        folder = os.path.join(ACTIVE_DIRECTORY, str(year))
        make_dirs(folder)
        move_files(file_name, folder)

# Sort by substring
def substring_sort(file_name, substrings):
    length = len(substrings)

    string = ""
    count = 0
    while count < length:
        if not substrings[count].isspace():
            string += substrings[count]
        else:
            substrings_list.append(string)
            string = ""

        if count == length-1:
            substrings_list.append(string)
            string = ""

        count += 1

    # Do not sort this script
    for substr in substrings_list:
        if not os.path.basename(file_name) == 'sorting.py':
            if substr in os.path.basename(file_name):
                folder = os.path.join(ACTIVE_DIRECTORY, substr)
                make_dirs(folder)
                move_files(file_name, folder)

# Delete empty directories
def del_empty_dirs(path):
    # Test if path is a file or directory
    if not os.path.isdir(path):
        return

    # Remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            full_path = os.path.join(path, f)
            if os.path.isdir(full_path):
                del_empty_dirs(full_path)

    # If folder is empty, remove it
    if len(files) == 0:
        print('Removing empty folder: ' + path)
        try:
            os.rmdir(path)
        except PermissionError:
            print("Exception: could not delete folder: " + path)
            pass
        return

# Create folders if they do not exist already
def make_dirs(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Move files between directories
def move_files(file_name, folder):
    new_path = os.path.join(folder, os.path.basename(file_name))

    if new_path == file_name:
        return

    if not os.path.exists(new_path):
        os.rename(file_name, new_path)
        file_moved[file_name] = True
    else:
        file_moved[file_name] = False
        file_duplicate[file_name] = True
        print(new_path + " exists")

def rename_duplicates():
    if not len(file_duplicate) == 0:

        for name in file_duplicate:
            base = os.path.basename(name)
            new_name = "copy-" + base
            try:
                file_duplicate[name] == False
                if not os.path.exists(new_name):
                    os.rename(name, new_name)
            except FileNotFoundError:
                print("rename_duplicates: FileNotFound")


# Main function
def main():
    print("Sorting " + ACTIVE_DIRECTORY)

    # Ask if user wants to sort files by year
    print("How would you like to sort?\n 1) By year.\n 2) By substring.")
    c = input("Enter the number: ")

    if c == '1':
        sort = True
        substr = False
        substrings = ""

    elif c == '2':
        sort = False
        substrings = input("Enter substrings separated with a space: ")
        substr = True

    else:
        print("Invalid input!")
        exit()

    # Ask if user wants to delete empty directories
    c2 = input("Would you like to delete empty directories? (y or n) ")
    if c2 == 'y':
        delete = True
    elif c2 == 'n':
        delete = False
    else:
        print("Invalid input!")
        exit()

    c3 = input("Are you sure you want to sort " + ACTIVE_DIRECTORY + " ? (y or n) ")
    if c3 == 'y':
        # Search through files, sorting by year and deleting empty directories if specified by the user
        search(ACTIVE_DIRECTORY, sort, substr, delete, substrings)
        rename_duplicates()

    elif c3 == 'n':
        print("Exiting...")
        exit()
    else:
        print("Invalid input!")
        exit()

if __name__ == '__main__':
    main()
