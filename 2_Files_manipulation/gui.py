import customtkinter as ctk
from pathlib import Path

class FilesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Files app')
        self.geometry('700x500')

        cwd = Path.cwd()
        cwd_str = ctk.StringVar(value=str(cwd))
        inner_dirs = [child.name for child in cwd.iterdir()]
        inner_dirs_lbls = [ctk.CTkLabel(self, text=str(child), font=('Arial', 17)) for child in inner_dirs]

        for i in range(len(inner_dirs_lbls)):
            inner_dirs_lbls[i].grid(column=0, row=i+1, sticky='w', padx=10)

        self.current_dir = ctk.CTkLabel(self, textvariable=cwd_str, font=('Arial', 20))
        self.current_dir.grid(column=0, row=0, sticky='ew')