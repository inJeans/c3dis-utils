import os

ROOT_DATA_DIR = os.path.expanduser("~/data")
try:
    os.makedirs(ROOT_DATA_DIR)
except: 
    pass

GDRIVE_DATA_ID = "1f3y7SusD2ECpVnY4Q48G26wVyMBzDb7X"