import logging, time, customtkinter as ctk

class TaskWidget(ctk.CTkFrame):
    def __init__(self, name, time, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.task_name = name
        self.time = time
        self.text = ctk.StringVar(value=f'{self.task_name}: {self.time}')
        self.label = ctk.CTkLabel(self, textvariable=self.text, font=('Arial', 20))
        self.label.grid(row=0, column=0, sticky='e')

class TasksManager(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        logging.info('TasksManager object has been created')
        self.tasks = {}
        self.tasks_widgets = []
    
    def reload_tasks(self):
        for task_widget in self.tasks_widgets:
            task_widget.grid_forget()

        len = 0
        for task_name, time in self.tasks.items():
            task_widget = TaskWidget(task_name, time, self)
            task_widget.grid(row=len, column=0, sticky='ew', pady=10, padx=20)
            self.tasks_widgets.append(task_widget)
            len += 1

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

    window = ctk.CTk()
    window.geometry('1024x800')
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    tm = TasksManager(window)
    tm.add_task('work', 5)
    tm.add_task('rest', 2)
    tm.reload_tasks()
    tm.grid(row=0, column=0, sticky='nswe')
    
    window.mainloop()
