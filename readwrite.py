#!/usr/bin/env python3

from typing import List

class Readwrite:
    def __init__(self):
        pass

    def read_file(self, file_path: str) -> List:
        try:
            with open(file_path, "r") as file:
                return file.readlines()
        except Exception as e:
            print("Error! in read_file: " + file_path + " - " + str(e))


    def read_file_as_bytes(self, file_path: str) -> bytes:
        try:
            with open(file_path, "rb") as file:
                return file.read(1024000)
        except Exception as e:
            print("Error! in read_file: " + file_path + " - " + str(e))


    def write_to_file(self, file_path: str, string_to_write: str):
        try:
            with open(file_path, "a") as file:
                file.write(string_to_write)
        except Exception as e:
            print("Error! in write_to_file: " + str(e))


    def write_list_to_file(self, file_path: str, list_to_write: List):
        try:
            with open(file_path, "a") as file:
                file.writelines(list_to_write)
        except Exception as e:
            print("Error! in write_to_file: " + str(e))






