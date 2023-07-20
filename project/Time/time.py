import logging, time, customtkinter as ctk, threading

class TaskWidget(ctk.CTkFrame):
    def __init__(self, name, time, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.task_name = name
        self.time = time
        self.current_time = time
        self.text = ctk.StringVar(value=f'{self.task_name}: {self.current_time}')
        self.label = ctk.CTkLabel(self, textvariable=self.text, font=('Arial', 20))
        self.label.grid(row=0, column=0, sticky='e')
    
    def reset_time(self):
        self.current_time = self.time
        self.update_label()

    def decrease(self):
        if self.current_time != 0:
            self.current_time -= 1
            self.update_label()

    def update_label(self):
        self.text.set(f'{self.task_name}: {self.current_time}')


class TasksManager(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        logging.info('TasksManager object has been created')
        self.tasks_widgets = []
        self.start_btn = ctk.CTkButton(self, text='start', command=self.execute_tasks)
        self.start_btn.grid(row=0, column=0)
    
    def reload_tasks_time(self):
        for task in self.tasks_widgets:
            task.reset_time()
    
    def reload_tasks_grid(self):
        for task_widget in self.tasks_widgets:
            task_widget.grid_forget()

        for row_ind, task_widget in enumerate(self.tasks_widgets):
            task_widget.grid(row=row_ind+1, column=0, sticky='ew', pady=10, padx=20)

    def add_task(self, name, length):
        if len(name) > 0:
            self.tasks_widgets.append(TaskWidget(name, length, self))
    
    def execute_tasks(self):
        self.reload_tasks_time()
        thread = threading.Thread(target=self.__execute_tasks)
        thread.start()

    def __execute_tasks(self):
        self.start_btn.configure(state='disabled')
        logging.debug('Started executing tasks...')
        for task in self.tasks_widgets:
            logging.debug(f'executing next task {task.task_name}')
            while task.current_time != 0:
                time.sleep(1)
                task.decrease()
                logging.debug(f'{task.task_name}: {task.time}')
        logging.debug('end executing tasks')
        self.start_btn.configure(state='enabled')
            


if __name__ == '__main__':
    logging.basicConfig(filename='time.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')

    window = ctk.CTk()
    window.geometry('1024x800')
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    window.resizable(False, False)

    tm = TasksManager(window)
    tm.add_task('work', 5)
    tm.add_task('rest', 2)
    tm.reload_tasks_grid()
    tm.grid(row=0, column=0, sticky='nswe')
    
    window.mainloop()