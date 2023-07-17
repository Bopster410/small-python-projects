import logging, time

class TasksManager():
    def __init__(self):
        logging.info('TasksManager object has been created')
        self.tasks = {}
    
    def add_task(self, name, length):
        if len(name) > 0:
            self.tasks[name] = length
    
    def execute_tasks(self):
        for task, length in self.tasks.items():
            print(f'{task} ({length}):')
            for seconds_left in range(length, 0, -1):
                print(f'{seconds_left} seconds left')
                time.sleep(1)
            print('task is over')
        print('all tasks are over')



if __name__ == '__main__':
    logging.basicConfig(filename='time.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    tm = TasksManager()
    tm.add_task('work', 5)
    tm.add_task('rest', 2)
    tm.execute_tasks()