import logging

class fileManipulator():
    def __init__(self):
        logging.debug('fileManipulator object has been created')

if __name__ == '__main__':
    logging.basicConfig(filename='files.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    fm = fileManipulator()