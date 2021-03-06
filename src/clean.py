import json
import shutil
import sys
from collections import Counter
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class OrganizeFiles:
    """this class is used to clean a directories based on extensions"""
    def __init__(self):
        ext_dirs = read_json(DATA_DIR / 'extensions.json')
        self.extensions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list :
                self.extensions_dest[ext] = dir_name

    def __call__(self, directory):
        """Organize files in a directory by moving them to their respective directories"""

        direcory = Path(directory)
        if not direcory.exists():
            raise FileNotFoundError("The directory does not exist")
        logger.info("Organizing the files in the {directory}...")
        for file_path in direcory.iterdir():
            #ignore directiries
            if file_path.is_dir():
                continue
            #ignore hidden files
            if file_path.name.startswith('.'):
                continue

            if file_path.suffix not in self.extensions_dest :
                DEST_DIR = direcory / 'others'
            else :
                #makes destionation directories
                DEST_DIR = direcory / self.extensions_dest[file_path.suffix]
                DEST_DIR.mkdir(exist_ok=True)
                logger.info(f"Moving {file_path} to {DEST_DIR}")
                shutil.move(str(file_path), str(DEST_DIR))
                #moves files to the directories
                pass

if __name__ == "__main__":
    org_files = OrganizeFiles()
    org_files(sys.argv[1])
    logger.info("Done!")
