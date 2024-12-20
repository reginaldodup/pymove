# !/usr/bin/python
# Author: Reginaldo MARINHO
# Date:   11-20-19
# email:  reginaldomsj@gmail.com

import re
import os
import argparse
import csv

"""
    This script renames files based on regex matching.
        usage: pmove.py [-h] [-fp [FOLDER_PATH]] [-csv [CSV_LIST_FILE]]
                        [-seq SEQUENCE [SEQUENCE ...]] [-v] [-c]

        Use pmove -h for more details

    For positional arguments substitution use: \number instead of $number
"""

parser = argparse.ArgumentParser(
    description="This script renames files based on regex matching. \
    Usage: regex_mv [--folder_path] <folder path> [--csv_list_file] <csv file list> [-h] [-v] [-c] search_patern replace_patern"
)

parser.add_argument("search_patern", metavar="", help="search_patern:....Search patern")
parser.add_argument(
    "replace_patern", metavar="", help="replace_patern:...Replace patern"
)

parser.add_argument(
    "-fp",
    "--folder_path",
    nargs="?",
    default=False,
    help="Folder containing files to be renamed",
)
parser.add_argument(
    "-csv",
    "--csv_list_file",
    nargs="?",
    default=False,
    help="File containing the old and new names",
)
parser.add_argument(
    "-seq",
    "--sequence",
    type=int,
    nargs="+",
    default=[0, 1],
    help="sequence start number, increment, leading zeroes",
)
parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose")
parser.add_argument(
    "-c",
    "--check_output",
    action="store_true",
    help="Check outputs: This option will only \
print the old and new names of the files and will not rename them. It is recommended to used this option to \
check if the result is as expected and only then use the rename functionality!",
)
parser.add_argument(
    "-r", "--recursive", action="store_true", help="Aply change to subfolders"
)

args = parser.parse_args()


if args.folder_path:
    cwd = args.folder_path
else:
    cwd = os.getcwd()

if args.verbose:
    print("---\nPMOVE 1.0")
    print("SEARCH PATERN:  ", args.search_patern)
    print("REPLACE PATERN: ", args.replace_patern)
    print("FOLDER PATH:    ", cwd)
    print("Sequence:       ", args.sequence)
    print("CSV list file:  ", args.csv_list_file)


def rename_files(root, file_list, max_str_lenght):

    if args.sequence or args.sequence is None:
        if args.sequence is None:
            counter = 0
            increment = 1
            leading_zero = 0
        else:
            if len(args.sequence) == 1:
                counter = args.sequence[0]
                increment = 1
                leading_zero = 0
            elif len(args.sequence) == 2:
                counter = args.sequence[0]
                increment = args.sequence[1]
                leading_zero = 0
            else:
                counter = args.sequence[0]
                increment = args.sequence[1]
                leading_zero = args.sequence[2]

        if args.verbose:
            print("counter", counter)
            print("increment", increment, "\n---")

    if args.csv_list_file:
        # print("Get values from list")
        with open(os.path.join(cwd, args.csv_list_file), newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            # print(reader)
            for row in reader:
                # print(row)
                # print(row[args.search_patern], row[args.replace_patern])
                if os.path.isfile(
                    os.path.join(cwd, row[args.search_patern])
                ) or os.path.isdir(os.path.join(cwd, row[args.search_patern])):
                    f = row[args.search_patern]
                    dst = row[args.replace_patern]
                    if args.check_output:
                        print(f, "->", dst)
                    else:
                        print(f, "->", dst)
                        os.rename(f, dst)

    else:
        for f in file_list:

            if "%#%" in args.replace_patern:
                if leading_zero == 0:
                    new_patern = args.replace_patern.replace("%#%", str(counter))
                else:
                    new_patern = args.replace_patern.replace(
                        "%#%", str(counter).zfill(leading_zero)
                    )
            else:
                new_patern = args.replace_patern

            re.compile(args.search_patern, re.IGNORECASE)
            dst = re.sub(args.search_patern, new_patern, f)

            if dst != f:
                if args.check_output:
                    print(f, " " * (max_str_lenght - len(f)), "->", dst)
                else:
                    print(f, " " * (max_str_lenght - len(f)), "->", dst)
                    os.rename(os.path.join(root, f), os.path.join(root, dst))

                counter = counter + increment


if args.recursive:
    # Walk the folders three  from inside ou 'topdown=False' to prevent
    # renamimg top folders before files
    for root, dirs, files in os.walk(cwd, topdown=False):
        # for name in files:
        # print(os.path.join(root, name))
        # for name in dirs:
        # print(os.path.join(root, name))
        print("\nCHECKING :", root)
        print("-------------------")
        # print(files)
        file_list = files + dirs

        # if len(file_list)==0:
        # print("No file in directory. To rename folders use non recursive replace!")
        # quit()

        file_list.sort()
        max_str_lenght = max([len(f) for f in file_list])
        # print(max_str_lenght)

        rename_files(root, file_list, max_str_lenght)
else:
    file_list = [f for f in os.listdir(cwd)]
    file_list.sort()
    max_str_lenght = max([len(f) for f in file_list])
    print(max_str_lenght)
    rename_files(cwd, file_list, max_str_lenght)
