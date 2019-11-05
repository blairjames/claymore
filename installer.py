#!/usr/bin/env python3

import sys
import os


def check_python_version():
    try:
        x, y, z, a, b = sys.version_info
        ver = str(x) + str(y)
        if int(ver) < 36:
            print("\nThis application requires Python 3.6 or greater.\nhttps://www.python.org/downloads/\n")
            exit(0)
    except PermissionError as p:
        print("woops!, you need to run this as root.\n" + str(p))
        exit(1)
    except Exception as e:
        print("Error! in check_python_version: " + str(e))

def write_unit_file(systemd_file):
    try:
        with open("/etc/systemd/system/claymore.service", "w") as file:
            file.writelines(systemd_file)
    except PermissionError as p:
        print("\nwoops!, you need to run the installer as root.\n")
        exit(1)
    except Exception as e:
        print("Error! in write_unit_file: " + str(e))

def systemd_unit_file():
    systemd_file = [
    "[Unit]",
    "\nDescription=Claymore",
    "\n[Service]",
    "\nType=simple",
    "\nExecStartPre=/bin/sleep 4",
    "\nExecStart=/usr/bin/env python3 " + os.getcwd() + "/claymore.py",
    "\nRestart=always",
    "\n[Install]",
    "\nWantedBy=multi-user.target\n"
    ]
    return systemd_file

def enable_service():
    try:
        os.system("systemctl enable claymore.service")
        os.system("systemctl restart claymore.service")
    except PermissionError as p:
        print("woops!, you need to run this as root.\n" + str(p))
        exit(1)
    except Exception as e:
        print("Error! in enable_service: " + str(e))


def main():
    check_python_version()
    write_unit_file(systemd_unit_file())
    enable_service()

if __name__ == '__main__':
    main()
