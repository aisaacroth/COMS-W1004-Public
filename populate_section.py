#!/usr/bin/env python3

'''


Author: Alexander Roth
Date:   2016-01-30
'''

from os import listdir, makedirs, path, remove, rename
import sys
from zipfile import ZipFile


def main(args):
    section_bounds = (args[0], args[1])
    sub_dir = args[2]
    sub_dir_path = get_directory_path(sub_dir)

    section_items = populate_section_list(section_bounds, sub_dir_path)
    remove_other_students(section_items, sub_dir_path)
    create_student_directories(sub_dir_path)


def get_directory_path(sub_dir):
    return path.realpath(sub_dir)


def populate_section_list(section_bounds, sub_dir_path):
    start_uni = section_bounds[0]
    end_uni = section_bounds[1]

    section_items = []
    for item in listdir(sub_dir_path):
        uni = retrieve_uni(item)

        if start_uni <= uni and uni <= end_uni:
            section_items.append(item)

    return section_items


def retrieve_uni(filename):
    if filename.split('_')[1] == 'late':
        return filename.split('_')[4].lower()
    return filename.split('_')[3].lower()


def remove_other_students(section_items, sub_dir_path):
    for item in listdir(sub_dir_path):
        if item in section_items:
            continue
        remove(path.join(sub_dir_path, item))


def create_student_directories(sub_dir_path):
    for item in listdir(sub_dir_path):
        old_dir = path.join(sub_dir_path, item)
        uni = retrieve_uni(item)
        new_dir = path.join(sub_dir_path, uni)

        if item.endswith('.zip'):
            with ZipFile(path.join(sub_dir_path, item), 'r') as zipfile:
                zipfile.extractall(new_dir)
                remove(old_dir)
        else:
            makedirs(new_dir)
            rename(old_dir, path.join(new_dir, item))


def print_arguments(arg):
    print('python3 {0} <start_uni> <end_uni> <submission dir>'.format(arg))
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1:])
    else:
        print_arguments(sys.argv[0])
