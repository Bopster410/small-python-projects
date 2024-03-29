import logging, time, customtkinter as ctk, threading, re
from tkinter import ttk
from collections import namedtuple
from datetime import time as time_dt
from plyer import notification


class TaskWidget(ctk.CTkFrame):
    def __init__(self, name, time, delete_command, master, **kwargs):
        super().__init__(master=master, **kwargs)
        # Configuring grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Initial values
        self.task_name = name
        self.time = time
        self.current_time = ctk.DoubleVar(value=time)

        # Time label
        self.text = ctk.StringVar()
        self.update_label()
        self.label = ctk.CTkLabel(self, textvariable=self.text, font=('Arial', 20))
        self.label.grid(row=0, column=0, sticky='w')

        # Delete button
        self.delete_btn = ctk.CTkButton(self, text='X', width=40, command=delete_command, fg_color='transparent', text_color='black', hover_color='#aaaaaa')
        self.delete_btn.grid(row=0, column=1, padx=(15, 0))

        # Timer progress bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate", variable=self.current_time, maximum=time)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky='snwe')

    # Resets time 
    def reset_time(self):
        self.current_time.set(self.time)
        self.update_label()

    # Decreases time by 0.1
    def decrease(self):
        if self.current_time.get() > 0:
            self.current_time.set(round(self.current_time.get() - 0.1, 1))
            self.update_label()
            logging.debug(f'time of {self.task_name} decreased ({self.current_time} now)')

    # Updates label with current time
    def update_label(self):
        current_time_double = self.current_time.get()
        current_time_int = int(current_time_double)
        # If max time is bigger than 1 minute, use special format
        if self.time >= 60:
            # Special case when minutes are decreasing
            if 59 <= current_time_int % 60 <= 60:
                t = time_dt(minute=int(current_time_int / 60 + 1)).strftime('%M:%S')
                self.text.set(f'{self.task_name} {t}')
            # Normal output
            else:
                t = time_dt(minute=int(current_time_int / 60), second=current_time_int % 60 + (current_time_int - current_time_double != 0)).strftime('%M:%S')
                self.text.set(f'{self.task_name} {t}')
        else:
            self.text.set(f'{self.task_name}: {current_time_int + (current_time_int - current_time_double != 0)}')

    # Disables delete button
    def disable_delete(self):
        self.delete_btn.configure(state='disabled')

    # Enables delete button
    def enable_delete(self):
        self.delete_btn.configure(state='normal')


class AddTaskDialog(ctk.CTkToplevel):
    def __init__(self, master):
        # Initial settings
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

        # Enter key returns input
        self.bind('<Return>', lambda e: self._enter_command())
        # Escape key closes dialog
        self.bind('<Escape>', lambda e: self.destroy())
    
    def _create_widgets(self):
        # Configuring grid system
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._label = ctk.CTkLabel(self, text='Enter new task name and its length in seconds:', font=('Arial', 20))
        self._label.grid(row=0, column=0, columnspan=2, pady=30, sticky='nsew')

        # Entry for tasks name
        self._name_entry = ctk.CTkEntry(self, placeholder_text='name')
        self._name_entry.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 20), sticky='we')

        # Entry for minutes
        self._minutes_entry = ctk.CTkEntry(self, placeholder_text='minutes')
        self._minutes_entry.grid(row=2, column=0, padx=(15, 5), pady=(0, 20), sticky='we')

        # Entry for seconds
        self._seconds_entry = ctk.CTkEntry(self, placeholder_text='seconds')
        self._seconds_entry.grid(row=2, column=1, padx=(5, 15), pady=(0, 20), sticky='we')
        
        # Enter button
        self._enter_btn = ctk.CTkButton(self, text='Enter', command=self._enter_command)
        self._enter_btn.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 60), sticky='we')
    
    # Return current input
    def _enter_command(self):
        logging.info('enter button was clicked')
        # Get all the fields
        name = self._name_entry.get()
        seconds = self._seconds_entry.get()
        minutes = self._minutes_entry.get()
        # If user is wrong, then return None
        self._user_input = None if name == '' or not re.fullmatch(r'\d+', seconds) or not re.fullmatch(r'\d*', minutes) else namedtuple('Input', ['name', 'time'])(name, int(seconds) + (int(minutes) * 60 if minutes != '' else 0))
        self.grab_release()
        self.destroy()

    # Get input
    def get_input(self):
        self.master.wait_window(self)
        return self._user_input


class TasksManager(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Configuring grid
        super().__init__(master, fg_color='transparent', **kwargs)
        logging.info('TasksManager object has been created')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Start tasks button
        self.start_btn = ctk.CTkButton(self, text='start', command=self.execute_tasks)
        self.start_btn.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        # Pause button
        self.pause_btn = ctk.CTkButton(self, text='pause', command=self.pause_tasks, state='disabled')
        self.pause_btn.grid(row=0, column=1, sticky='w', padx=(0, 5))

        # Stop tasks button
        self.stop_btn = ctk.CTkButton(self, text='stop', command=self.stop_tasks, state='disabled')
        self.stop_btn.grid(row=0, column=2, sticky='w', padx=(0, 5))
        
        # Repeat tasks switch
        self.repeat_switch = ctk.CTkSwitch(self, text='repeat', onvalue='on', offvalue='off')
        self.repeat_switch.grid(row=0, column=3, sticky='w')

        # Add task button
        self.add_task_btn = ctk.CTkButton(self, text='+', width=40, command=self._add_task_menu)
        self.add_task_btn.grid(row=0, column=4, sticky='e', padx=(0, 5))


        # Tasks frame
        self.tasks_widgets = {}
        self.tasks_frame = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.tasks_frame.rowconfigure(0, weight=1)
        self.tasks_frame.columnconfigure(0, weight=1)
        self.tasks_frame.grid(row=1, column=0, columnspan=5, sticky='nsew')
    
        # Style for progress bar
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Horizontal.TProgressbar', foreground='#007cca', background='#007cca')
        
        # self.current_task_ind = 0
        self.state = 'stop'
    
    # Reloads time for each task
    def reload_tasks_time(self):
        for task in self.tasks_widgets.values():
            task.reset_time()

    # Adds new task
    def add_task(self, name, length):
        if len(name) > 0:
            new_task = TaskWidget(name, length, self.create_delete_task(name), self.tasks_frame, width=400, height=200)
            self.tasks_widgets[name] = new_task

    # Delete task
    def delete_task(self, name):
        logging.info(f'Deleting {name} task')
        if name in self.tasks_widgets:
            self.tasks_widgets.pop(name).grid_forget()
            self._reload_tasks_grid()

    # Creates delete_task function for name with current name
    def create_delete_task(self, name):
        def delete_task():
            self.delete_task(name)

        return delete_task

    # Starts executing tasks in the separate threat
    def execute_tasks(self):
        thread = threading.Thread(target=self._execute_tasks)
        thread.start()

    # Pasuses tasks
    def pause_tasks(self):
        self.state = 'pause'
        self.start_btn.configure(state='normal')
        self.pause_btn.configure(state='disabled')

    # Stops all tasks and resets time
    def stop_tasks(self):
        self.state = 'stop'

    # Disables delete button for each tasks
    def _disable_delete_buttons(self):
        for task in self.tasks_widgets.values():
            task.disable_delete()
    
    # Enables delete button for each tasks
    def _enable_delete_buttons(self):
        for task in self.tasks_widgets.values():
            task.enable_delete()

    # Reloads tasks widgets in grid
    def _reload_tasks_grid(self):
        for task_widget in self.tasks_widgets.values():
            task_widget.grid_forget()

        for row_ind, task_widget in enumerate(self.tasks_widgets.values()):
            task_widget.grid(row=row_ind+1, column=0, sticky='w', pady=10, padx=20)
            task_widget.grid_propagate(0)

    # Opens dialog to add task
    def _add_task_menu(self):
        logging.info('Add task method')
        dialog = AddTaskDialog(self)
        input = dialog.get_input()
        if input != None:
            logging.info(f'input: name - {input.name}, time - {input.time}')
            self.add_task(*input)
            self._reload_tasks_grid()
        else:
            logging.warning(f'wrong input')

    # Execute all tasks
    def _execute_tasks(self):
        # start = 
        self.state = 'work'
        while self.state == 'work' and len(self.tasks_widgets) != 0:
            # Change buttons state
            self.start_btn.configure(state='disabled')
            self.add_task_btn.configure(state='disabled')
            self.pause_btn.configure(state='normal')
            self.stop_btn.configure(state='normal')
            self._disable_delete_buttons()
            logging.debug('Started executing tasks...')

            for i, task in enumerate(self.tasks_widgets.values()):
                notification.notify(title='Task manager', message=f'Next task is {task.task_name}')

                logging.debug(f'executing next task {task.task_name}')
                while task.current_time.get() != 0 and self.state == 'work':
                    time.sleep(0.1)
                    task.decrease()
                    logging.debug(f'{task.task_name}: {task.time}')
                
                if self.state in ('stop', 'pause'):
                    break
                
            if self.state == 'work':
                self.state = 'work' if self.repeat_switch.get() == 'on' else 'stop'
                
            if self.state in ('work', 'stop'):
                self.reload_tasks_time()

        notification.notify(title='Task manager', message='All tasks are completed!')

        # Return buttons to their previous
        logging.debug('end executing tasks')
        self.start_btn.configure(state='normal')
        self.add_task_btn.configure(state='normal')
        self.pause_btn.configure(state='disabled')
        self.stop_btn.configure(state='disabled')
        self._enable_delete_buttons()
            

if __name__ == '__main__':
    logging.basicConfig(filename='time.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')

    window = ctk.CTk()
    window.geometry('1024x800')
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    window.resizable(False, False)

    tm = TasksManager(window)
    tm.add_task('work', 4)
    tm._reload_tasks_grid()
    tm.grid(row=0, column=0, sticky='nswe')

    window.mainloop()