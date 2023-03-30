# This component contains all the utility tools needed to operate

import os
from datetime import datetime
import sys


def get_version():
    ver = "1.0.0"  # Date 30.3.2023
    return ver


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]

# Returns time
def get_time():
    now = datetime.now()  # current date and time
    time = now.strftime("%H:%M:%S")
    return time

def get_date():
    now = datetime.now()  # current date and time
    date = now.date()
    return date

# returns path into local folder
def get_local_path():
    local_directory = os.getcwd()

    return local_directory

