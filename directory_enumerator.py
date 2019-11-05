#!/usr/bin/env python3

from os import walk, listdir, path
from typing import List
from claymore_conf import whitelist


class DirectoryEnumerator:

    def __init__(self):
        self.all_files = []
        self.whitelist_directories = whitelist


    def get_all_sub_dirs(self, dir) -> List:
        try:
            if not dir:
                print("No input directory")
                raise Exception
            if dir is not "/":
                dir.rstrip("/")
            dirs = []
            addit = dirs.append
            [addit(dir + "/" +l) for l in listdir(dir) if not path.isfile(dir + "/" + l)
             and dir + "/" + l not in dirs]
            return dirs
        except FileNotFoundError:
            pass
        except Exception as e:
            print("Error! in get_all_dirs: " + str(e))


    def get_files(self, dir: str) -> List:
        try:
            if not dir:
                print("no dir passed into get_files")
                raise Exception
            #print("\nEnumerating " + dir + " directory")
            for base, subs, all_files in walk(dir.rstrip("/")):
                files = [(base + "/" + file) for file in all_files]
                return files
        except Exception as e:
            print("Error! in get files " + str(e))
            exit(1)
