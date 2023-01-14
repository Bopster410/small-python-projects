import logging, shutil, os, zipfile
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

    # Moves src to dest
    def move(self, src, dest):
        logging.info(f'moving {src} to {dest}')

        # Path to current workin directory in p variable
        p = Path.cwd()

        try:
            shutil.move(p / src, p / dest)
        # If dest contains folders that doesn't exist
        # then create them
        except FileNotFoundError:
            dir_to_create = dest[:dest.rfind('/')]
            os.makedirs(dir_to_create)
            shutil.move(p / src, p / dest)
            logging.info(f"created '{dir_to_create}' folders")

    # Creates zip-archive named [name] with [dir] in it
    # TODO add input errors handlers
    def zip(self, dir, name):
        with zipfile.ZipFile(name, 'w') as dir_zipped:
            p_dir = Path(dir)
            # If [dir] is directory
            if p_dir.is_dir():
                # Recursively add all files from the directory to the archive
                for file in p_dir.rglob('*'):
                    dir_zipped.write(file, compress_type=zipfile.ZIP_DEFLATED)
            # If [dir] is a single file actually
            else:
                dir_zipped.write(dir, compress_type=zipfile.ZIP_DEFLATED)
    
    # TODO add input errors handlers
    def unzip(self, dir, new_name=''):
        with zipfile.ZipFile(dir) as dir_zipped:
            dir_zipped.extractall(new_name) if len(new_name) else dir_zipped.extractall()
    

if __name__ == '__main__':
    logging.basicConfig(filename='files.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    fm = fileManipulator()
    # fm.copy('files.log', 'logss/files.log')
    # fm.move('logss/files.log', 'logs/files.log')
    # fm.zip('files.log', 'loggs.zip')
    # fm.zip('logs', 'logs.zip')
    # fm.unzip('logs.zip', 'l o g s')
    # fm.unzip('logs.zip')
    fm.zip('test', 'test.zip')
    fm.unzip('test.zip', 'test_unzipped')