"""
This module is designed to handle file and directory operations for the World Athletics Records project.

Functions:
- sync_folders(): Synchronizes the contents of two folders ('data/data_before' and 'data/data_after'), moving all items
  from the 'after' folder to the 'before' folder, excluding 'README.md' files. It also cleans the 'before' folder
  before synchronization by removing all items that do not match 'README.md'.

Author: LE GOURRIEREC Titouan
"""

############################################################################################################

import logging
import os
import shutil

logging.basicConfig(filename='log/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

############################################################################################################

def sync_folders() -> None:
    """
    Synchronizes the contents of two folders, moving all items from the 'after' folder to the 'before' folder,
    while excluding 'README.md' files. Items in the 'before' folder that do not match 'README.md' are removed
    before the synchronization.
    """
    before_path = 'data/data_before'
    after_path = 'data/data_after'

    for filename in os.listdir(before_path):
        if filename.lower() != 'readme.md':
            file_path = os.path.join(before_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.info(f'Failed to delete {file_path}. Reason: {e}')

    for filename in os.listdir(after_path):
        if filename.lower() != 'readme.md':
            source = os.path.join(after_path, filename)
            destination = os.path.join(before_path, filename)
            try:
                shutil.move(source, destination)
            except Exception as e:
                logging.info(f'Failed to move {source} to {destination}. Reason: {e}')