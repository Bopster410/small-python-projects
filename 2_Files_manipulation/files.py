import logging, shutil
from pathlib import Path

class fileManipulator():
    def __init__(self):
        logging.info('fileManipulator object has been created')
    
    # Copies scr to dest (relative)
    def copy(self, src, dest):
        logging.info(f'copying {src} to {dest}')
        p = Path.cwd()
        shutil.copy(p / src, p / dest)


if __name__ == '__main__':
    logging.basicConfig(filename='files.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    fm = fileManipulator()
    fm.copy('files.log', 'logs/files.log')