#!/usr/bin/env python3

import hashlib
import asyncio
import os


class Claymore:

    def __init__(self):
        self.dirs = [
            "/bin",
            "/sbin",
            "/opt",
            "/home",
            "/etc",
            "/proc",
            "/run",
            "/root",
            "/usr",
            "/var",
            "/sys",
            "/dev",
            "/lib64",
            "/boot"
        ]


    async def walker(self, base_directory):
        try:
            file_list = []
            add_to_file_list = file_list.append
            for base, subs, all_files in os.walk(base_directory):
                files = [file for file in all_files]
                [add_to_file_list(base + "/" + f) for f in files]
            await self.hasher(file_list)
        except Exception as e:
            print("Error in walker: " + str(e))


    async def hasher(self, files):
        try:
            md5 = hashlib.md5
            hashes = tuple([(md5(f.encode()).hexdigest(), f) for f in files])
            [print(h) for h in hashes]
        except Exception as e:
            print("Error in hasher: " + str(e))


    async def controller(self):
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(self.walker(d)) for d in self.dirs]
        await asyncio.wait(tasks)


def new_claymore():
    c = Claymore()
    return c


if __name__ == '__main__':
    clay = new_claymore()
    loop = asyncio.get_event_loop()
    task = loop.create_task(clay.controller())
    loop.run_until_complete(task)
