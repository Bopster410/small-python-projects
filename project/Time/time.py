import logging, time, customtkinter as ctk, threading
from collections import namedtuple

class TaskWidget(ctk.CTkFrame):
    def __init__(self, name, time, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.task_name = name
        self.time = time
        self.current_time = time
        self.text = ctk.StringVar(value=f'{self.task_name}: {self.current_time}')
        self.label = ctk.CTkLabel(self, textvariable=self.text, font=('Arial', 20))
        self.label.grid(row=0, column=0, sticky='w')
    
    def reset_time(self):
        self.current_time = self.time
        self.update_label()

    def decrease(self):
        if self.current_time != 0:
            self.current_time -= 1
            self.update_label()

    def update_label(self):
        self.text.set(f'{self.task_name}: {self.current_time}')


class AddTaskDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('600x300')

        # Lift window on top
        self.lift()
        # Stay on top
        self.attributes('-topmost', True)
        # Create widgets with slight delay, to avoid white flickering of background
        self.after(10, self._create_widgets)  
        # Not resizable
        self.resizable(False, False)
        # Make other windows not clickable
        self.grab_set()

        self._user_input = None
    
    def _create_widgets(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._label = ctk.CTkLabel(self, text='Enter new task name and its length in seconds:', font=('Arial', 20))
        self._label.grid(row=0, column=0, columnspan=2, pady=30, sticky='nsew')

        self._name_entry = ctk.CTkEntry(self, placeholder_text='name')
        self._name_entry.grid(row=1, column=0, padx=(15, 5), pady=(0, 20), sticky='we')

        self._time_entry = ctk.CTkEntry(self, placeholder_text='time')
        self._time_entry.grid(row=1, column=1, padx=(5, 15), pady=(0, 20), sticky='we')
        
        self._enter_btn = ctk.CTkButton(self, text='Enter', command=self.enter_command)
        self._enter_btn.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 60), sticky='we')
    
    def enter_command(self):
        logging.info('enter button was clicked')
        name = self._name_entry.get()
        time = self._time_entry.get()
        self._user_input = None if name == '' or time == '' else namedtuple('Input', ['name', 'time'])(name, int(time))
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input


class TasksManager(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Configuring grid
        super().__init__(master, fg_color='transparent', **kwargs)
        logging.info('TasksManager object has been created')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # Start tasks button
        self.start_btn = ctk.CTkButton(self, text='start', command=self.execute_tasks)
        self.start_btn.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        # Add task button
        self.add_task_btn = ctk.CTkButton(self, text='+', width=40, command=self._add_task_menu)
        self.add_task_btn.grid(row=0, column=1, sticky='w')

        # Tasks frame
        self.tasks_widgets = []
        self.tasks_frame = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.tasks_frame.rowconfigure(0, weight=1)
        self.tasks_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')
    
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
            self.tasks_widgets.append(TaskWidget(name, length, self.tasks_frame))
    
    def execute_tasks(self):
        self.reload_tasks_time()
        thread = threading.Thread(target=self._execute_tasks)
        thread.start()

    def _add_task_menu(self):
        logging.info('Add task method')
        dialog = AddTaskDialog(self)
        input = dialog.get_input()
        if input != None:
            logging.info(f'input: name - {input.name}, time - {input.time}')
            self.add_task(*input)
            self.reload_tasks_grid()
        else:
            logging.warning(f'wrong input')

    def _execute_tasks(self):
        self.start_btn.configure(state='disabled')
        self.add_task_btn.configure(state='disabled')
        logging.debug('Started executing tasks...')
        for task in self.tasks_widgets:
            logging.debug(f'executing next task {task.task_name}')
            while task.current_time != 0:
                time.sleep(1)
                task.decrease()
                logging.debug(f'{task.task_name}: {task.time}')
        logging.debug('end executing tasks')
        self.start_btn.configure(state='enabled')
        self.add_task_btn.configure(state='enabled')
            

if __name__ == '__main__':
    logging.basicConfig(filename='time.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')

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