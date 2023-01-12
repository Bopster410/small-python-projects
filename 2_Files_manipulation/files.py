import logging, shutil, os
from pathlib import Path

class fileManipulator():
    def __init__(self):
        logging.info('fileManipulator object has been created')
    
    # Copies scr to dest (relative)
    def copy(self, src, dest):
        logging.info(f'copying {src} to {dest}')

        # Path to current workin directory in p variable
        p = Path.cwd()

        try:
            shutil.copy(p / src, p / dest)
        # If dest contains folders that doesn't exist
        # then create them
        except FileNotFoundError:
            dir_to_create = dest[:dest.rfind('/')]
            os.makedirs(dir_to_create)
            shutil.copy(p / src, p / dest)
            logging.info(f"created '{dir_to_create}' folders")



if __name__ == '__main__':
    logging.basicConfig(filename='files.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    fm = fileManipulator()
    fm.copy('files.log', 'logs/files.log')