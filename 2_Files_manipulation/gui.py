import customtkinter as ctk
from pathlib import Path

class FilesApp(ctk.CTk):
    def __init__(self):
        self.super()

        self.title('Files app')
        self.geometry('700x500')

        self.current_dir = ctk.label(self, text='[Current directory]', font=('Arial', 25))
        self.current_dir.grid(column=0, row=0, ancher=ctk.CENTER)