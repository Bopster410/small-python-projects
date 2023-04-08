import customtkinter as ctk, logging
from pathlib import Path

class FilesApp(ctk.CTk):
    def __init__(self):
        logging.info('FilesApp object was created')
        super().__init__()

        self.title('Files app')
        self.geometry('700x500')

        self.cwd = Path.cwd()
        self.cwd_str = ctk.StringVar(value=str(self.cwd))
 
        self.current_dir = ctk.CTkLabel(self, textvariable=self.cwd_str, font=('Arial', 20))
        self.current_dir.grid(column=0, row=0, pady=10, sticky='ew')
        
        inner_dirs = [child.name for child in self.cwd.iterdir()]
        self.inner_dirs_btns = [ctk.CTkButton(self, text=str(child), font=('Arial', 17), command=self.change_dir_event(child)) for child in inner_dirs]

        for i in range(len(self.inner_dirs_btns)):
            self.inner_dirs_btns[i].grid(column=0, row=i+1, sticky='w', padx=10)

    def change_dir_event(self, new_dir):
        def change_dir():
            if (self.cwd / new_dir).is_dir():
                self.cwd = self.cwd / new_dir
                self.cwd_str.set(str(self.cwd))
                inner_dirs = [child.name for child in self.cwd.iterdir()]
                for i in range(len(self.inner_dirs_btns)):
                    self.inner_dirs_btns[i].grid_forget()
                self.inner_dirs_btns = [ctk.CTkButton(self, text=str(child), font=('Arial', 17), command=self.change_dir_event(child)) for child in inner_dirs]
                for i in range(len(self.inner_dirs_btns)):
                    self.inner_dirs_btns[i].grid(column=0, row=i+1, sticky='w', padx=10)
            
        return change_dir