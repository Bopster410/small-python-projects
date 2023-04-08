import customtkinter as ctk
from pathlib import Path

class FilesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Files app')
        self.geometry('700x500')

        cwd = ctk.StringVar(value=str(Path.cwd()))
        

        self.current_dir = ctk.CTkLabel(self, textvariable=cwd, font=('Arial', 25))
        self.current_dir.grid(column=0, row=0, sticky='ew')