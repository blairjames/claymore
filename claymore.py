#!/usr/bin/env python3

from directory_enumerator import DirectoryEnumerator
from claymore_conf import dirs, whitelist, frequency
from typing import List
from os import listdir, path, system
from hashlib import sha512
from readwrite import Readwrite
from time import sleep, perf_counter
from inotify import adapters


class Claymore:

    def __init__(self):
        self.dir_enum = DirectoryEnumerator()
        self.all_dirs = []
        self.all_files = []
        self.hash_dict = {}
        self.cached_hash_dict = {}
        self.reader = Readwrite().read_file_as_bytes
        self.writer = Readwrite().write_to_file
        self.frequency = frequency
        self.cache_is_warm = False
        self.logfile = "/var/log/claymore.log"


    def lint(self, message: str):
        try:
            message = str(message)
            print(message + "\n")
            self.writer(self.logfile, message + "\n")
        except Exception as e:
            print("Error! in Lint!! " + str(e))


    def notify(self):
        pass


    def get_subs(self, dir_list: List):
        try:
            addit = self.all_dirs.append
            all_dirs = self.all_dirs
            is_file = path.isfile
            [[addit(d + "/" +l) for l in listdir(d) if not is_file(d + "/" + l)
              and d + "/" + l not in all_dirs] for d in dir_list if d not in whitelist]
        except FileNotFoundError:
            pass
        except Exception as e:
            message = "Error! in get_subs: " + str(e)
            self.lint(message)


    def get_files(self, dir):
        try:
            addit = self.all_files.append
            files = DirectoryEnumerator().get_files(dir)
            all_files = self.all_files
            is_a_file = path.isfile
            if files:
                [addit(f) for f in files if f not in all_files and is_a_file(f)]
        except Exception as e:
            self.lint("Error! in get_files: " + str(e))


    def get_file_data(self, file_name) -> str:
        if file_name:
            data = system("stat " + file_name)
            self.lint(str(data))
            return str(data)


    def hashpipe(self, files: List):
        t1 = perf_counter()
        hashy = self.hash_dict.__setitem__
        read = self.reader
        my_sha512 = sha512
        [hashy(file, my_sha512(read(file))) for file in files]
        t2 = perf_counter()
        self.lint("Time to Hash all files: " + str(round(t2 - t1, 5)))


    def compare_dicts(self):
        # Compare Dicts
        try:
            self.lint("Checking Hashes..")
            if self.cache_is_warm:
                [self.lint(self.get_file_data(k) + "\n") for k in self.all_files
                 if self.cached_hash_dict[k].hexdigest() != self.hash_dict[k].hexdigest()]
        except Exception as e:
            self.lint("Error! - dict comparison: " + str(e))


    def controller(self):
        try:
            while True:
                self.lint("Getting files from root directories..")
                [self.get_files(d) for d in dirs if d not in whitelist]

                self.lint("Getting subdirectories from root directories..")
                self.get_subs(dirs)

                self.lint("Getting subdirectories recursively..")
                #Recursively get dirs
                i: int = 0
                while i < 21:
                    self.get_subs(self.all_dirs)
                    i += 1

                #Using complete unique dir list get files from dirs
                self.lint("Getting files from all directories..")
                [self.get_files(d) for d in self.all_dirs]

                self.lint("Moving hash dictionary to cache")
                #move last dict to cache
                self.cached_hash_dict = self.hash_dict.copy()
                self.hash_dict.clear()

                # make new dict
                self.lint("Hashing files..")
                self.hashpipe(self.all_files)

                self.lint("hash_dic_len: " + str(self.hash_dict.__len__()))
                self.lint("cache_len: " + str(self.cached_hash_dict.__len__()))

                #Is this the first run, cold cache
                self.cache_is_warm: bool = self.cached_hash_dict.__len__() > 0

                self.compare_dicts()

                self.lint("Total Directories: " + str(self.all_dirs.__len__()))
                self.lint("Total Files: " + str(self.all_files.__len__()))

                if self.cache_is_warm:
                    self.lint("\nSleeping " + str(self.frequency) + " sec\n")
                    sleep(self.frequency)

        except Exception as e:
            self.lint("Error! in controller: " + str(e))


def main():
    Claymore().controller()


if __name__ == '__main__':
    main()


