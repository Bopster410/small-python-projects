import logging

def TasksManager():
    def __init__(self):
        logging.info('TasksManager object has been created')


if __name__ == '__main__':
    logging.basicConfig(filename='time.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    tm = TasksManager()