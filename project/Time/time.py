import logging, time, customtkinter as ctk, threading

class TaskWidget(ctk.CTkFrame):
    def __init__(self, name, time, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.task_name = name
        self.time = time
        self.text = ctk.StringVar(value=f'{self.task_name}: {self.time}')
        self.label = ctk.CTkLabel(self, textvariable=self.text, font=('Arial', 20))
        self.label.grid(row=0, column=0, sticky='e')
    
    def decrease(self):
        if self.time != 0:
            self.time -= 1
            self.update_label()

    def update_label(self):
        self.text.set(f'{self.task_name}: {self.time}')


class TasksManager(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        logging.info('TasksManager object has been created')
        self.tasks = {}
        self.tasks_widgets = []
        self.start_btn = ctk.CTkButton(self, text='start', command=self.execute_tasks)
        self.start_btn.grid(row=0, column=0)
    
    def reload_tasks_time(self):
        for task in self.tasks_widgets:
            task.time = self.tasks[task.task_name]
    
    def reload_tasks_grid(self):
        for task_widget in self.tasks_widgets:
            task_widget.grid_forget()

        len = 0
        for task_name, time in self.tasks.items():
            task_widget = TaskWidget(task_name, time, self)
            task_widget.grid(row=len+1, column=0, sticky='ew', pady=10, padx=20)
            self.tasks_widgets.append(task_widget)
            len += 1

    def add_task(self, name, length):
        if len(name) > 0:
            self.tasks[name] = length
    
    def execute_tasks(self):
        self.reload_tasks_time()
        thread = threading.Thread(target=self.__execute_tasks)
        thread.start()

    def __execute_tasks(self):
        logging.debug('Started executing tasks...')
        for task in self.tasks_widgets:
            logging.debug(f'executing next task {task.task_name}')
            while task.time != 0:
                time.sleep(1)
                task.decrease()
                logging.debug(f'{task.task_name}: {task.time}')
        logging.debug('end executing tasks')
            


if __name__ == '__main__':
    logging.basicConfig(filename='time.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')

    window = ctk.CTk()
    window.geometry('1024x800')
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    tm = TasksManager(window)
    tm.add_task('work', 5)
    tm.add_task('rest', 2)
    tm.reload_tasks_grid()
    tm.grid(row=0, column=0, sticky='nswe')
    
    window.mainloop()