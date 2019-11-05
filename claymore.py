#!/usr/bin/env python3

from directory_enumerator import DirectoryEnumerator
from claymore_conf import dirs, whitelist
from typing import List
from os import listdir, path
from hashlib import sha512
from utilities import readwrite


class Claymore:

    def __init__(self):
        self.dir_enum = DirectoryEnumerator()
        self.all_dirs = []
        self.all_files = []
        self.hash_dict = {}
        self.old_hash_dict = {}
        self.log_file = "/var/log/claymore.log"
        self.writer = readwrite.Readwrite().write_to_file


    def lint(self, message: str):
        try:
            print(message)
            self.writer(self.log_file, message)
        except Exception as e:
            print("Error! in Lint!! " + str(e))


    def get_subs(self, dir_list: List):
        try:
            addit = self.all_dirs.append
            [[addit(d + "/" +l) for l in listdir(d) if not path.isfile(d + "/" + l)
              and d + "/" + l not in self.all_dirs] for d in dir_list if d not in whitelist]
        except FileNotFoundError:
            pass
        except Exception as e:
            message = "Error! in get_subs: " + str(e)
            self.lint(message)


    def get_files(self, dir):
        try:
            addit = self.all_files.append
            files = DirectoryEnumerator().get_files(dir)
            if files:
                [addit(f) for f in files if f not in self.all_files and path.isfile(f)]
        except Exception as e:
            self.lint("Error! in get_files: " + str(e))


    def hashpipe(self, file):
        self.hash_dict.__setitem__(file, sha512(file.encode()))


    def controller(self):
        try:
            [self.get_files(d) for d in dirs if d not in whitelist]
            self.get_subs(dirs)

            #Recursively get dirs
            i: int = 0
            while i < 21:
                self.get_subs(self.all_dirs)
                i += 1

            #Using complete unique dir list get files from dirs
            [self.get_files(d) for d in self.all_dirs]

            #move last dict to old dict
            self.old_hash_dict = self.hash_dict.copy()
            self.hash_dict.clear()

            #make new dict
            [self.hashpipe(f) for f in self.all_files]

            #compare dicts
            if not self.hash_dict == self.old_hash_dict:
                #work out what's different
                pass

        except Exception as e:
            self.lint("Error! in controller: " + str(e))


def main():
    Claymore().controller()


if __name__ == '__main__':
    main()


