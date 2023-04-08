import customtkinter as ctk, logging
from pathlib import Path

class FilesApp(ctk.CTk):
    def __init__(self):
        logging.info('FilesApp object was created')
        super().__init__()

        # Init window settings
        self.title('Files app')
        self.geometry('700x500')

        # Current working directory
        self.cwd = Path.cwd()
        self.cwd_str = ctk.StringVar(value=str(self.cwd))
 
        # Label for cwd
        self.current_dir = ctk.CTkLabel(self, textvariable=self.cwd_str, font=('Arial', 20))
        self.current_dir.grid(column=0, row=0, pady=10, sticky='ew')
        
        # Child directories inside cwd
        self.inner_dirs_btns = self.__form_inner_dirs()
        self.__grid_all(self.inner_dirs_btns, first_row=1)

    def change_dir_event(self, new_dir):
        # If new_dir is a folder, open it,
        # else just leave everything as it is
        def change_dir():
            if (self.cwd / new_dir).is_dir():
                if new_dir == '..':
                    self.cwd = self.cwd.parent
                else:
                    self.cwd = self.cwd / new_dir
                self.cwd_str.set(str(self.cwd))
                self.__grid_forget_all(self.inner_dirs_btns)
                self.inner_dirs_btns = self.__form_inner_dirs()
                self.__grid_all(self.inner_dirs_btns, first_row=1)
        return change_dir
    
    def __form_inner_dirs(self):
        # Child directories inside cwd
        inner_dirs = ['..'] + [child.name for child in self.cwd.iterdir()]
        # ..and buttons for all of them
        return [ctk.CTkButton(self, text=child, font=('Arial', 17), command=self.change_dir_event(child)) for child in inner_dirs]
    
    def __grid_forget_all(self, objects):
        for i in range(len(objects)):
            objects[i].grid_forget()

    def __grid_all(self, objects, first_row=0):
        for i in range(len(objects)):
            objects[i].grid(column=0, row=i+first_row, sticky='w', padx=10)
 