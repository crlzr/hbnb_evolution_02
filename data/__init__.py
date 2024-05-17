#!/usr/bin/python3
""" initialize the storage used by models """

import os
from data.db_storage import DBStorage
from data.file_storage import FileStorage

# check for STORAGE=FILE from command line
# command to use: STORAGE=FILE python3 ./app.py
use_file_storage = "STORAGE" in os.environ and os.environ['STORAGE'] == "FILE"

# check for TESTING=1 from command line
# command to use: TESTING=1 python3 -m unittest discover
is_testing = "TESTING" in os.environ and os.environ['TESTING'] == "1"

if use_file_storage:
    storage = FileStorage()
else:
    storage = DBStorage()

# doesn't matter if we're using file or db storage. call the load_data method
storage.load_data(is_testing)
