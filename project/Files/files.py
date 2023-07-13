import logging, shutil, os, zipfile
from pathlib import Path

class FileManipulator():
    def __init__(self):
        logging.info('FileManipulator object has been created')
    
    # Copies scr to dest (relative)
    def copy(self, src: str, dest: str):
        logging.info(f'copying {src} to {dest}')

        # Path to current workin directory in p variable
        p = Path.cwd()
        dest_path = Path(p / dest)

        # Checks if [src] exists
        if Path(p / src).exists():
            try:
                count = 1
                dest_path_temp = dest_path
                while dest_path_temp.exists():
                    dest_path_temp = dest_path.with_stem(f'{dest_path.stem}({count})')
                    count += 1

                if Path(p / src).is_dir():
                    shutil.copytree(p / src, dest_path_temp)
                else:
                    shutil.copy(p / src, dest_path_temp)
            # If dest contains folders that doesn't exist
            # then create them
            except FileNotFoundError:
                dir_to_create = dest[:dest.rfind('/')]
                os.makedirs(dir_to_create)
                if Path(p / src).is_dir():
                    shutil.copytree(p / src, dest_path)
                else:
                    shutil.copy(p / src, dest_path)
                logging.info(f"created '{dir_to_create}' folders")
        else:
            logging.error(f"{src} doesn't exist")

    # Moves src to dest
    def move(self, src, dest):
        
        logging.info(f'moving {src} to {dest}')

        # Path to current workin directory in p variable
        p = Path.cwd()
        dest_path = Path(p / dest)
        
        # Checks if [src] exists
        if Path(p / src).exists():
            try:
                count = 1
                dest_path_temp = dest_path
                while dest_path_temp.exists():
                    dest_path_temp = dest_path.with_stem(f'{dest_path.stem}({count})')
                    count += 1

                shutil.move(p / src, dest_path_temp)
            # If dest contains folders that doesn't exist
            # then create them
            except FileNotFoundError:
                dir_to_create = dest[:dest.rfind('/')]
                os.makedirs(dir_to_create)
                shutil.move(p / src, dest_path)
                logging.info(f"created '{dir_to_create}' folders")
        else:
            logging.error(f"{src} doesn't exits")

    # Creates zip-archive named [name] with [dir] in it
    def zip(self, dir, name):
        logging.info(f'zipping {dir}')
        try:
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
                logging.info(f"successfully zipped {dir} into {name}")
        except:
            logging.error(f"couldn't zip {dir}: no such file or directory")
    
    # Extracts files from [dir] archive into [new_name] folder
    def unzip(self, dir, new_name=''):
        logging.info(f'unzipping {dir}')
        try:
            with zipfile.ZipFile(dir) as dir_zipped:
                dir_zipped.extractall(new_name) if len(new_name) else dir_zipped.extractall()
            logging.info(f"successfully extracted {dir} into {new_name if len(new_name) else 'current directory'}")
        except FileNotFoundError:
            logging.error(f"couldn't unzip {dir} file: no directory with this name")
    

if __name__ == '__main__':
    logging.basicConfig(filename='files.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    fm = FileManipulator()
    fm.copy('files.log', 'logss/files.log')
    fm.copy('logss', 'logsss/logss')
    fm.move('test', 'logss')
    fm.zip('test', 'test.zip')
    fm.unzip('test.zip')