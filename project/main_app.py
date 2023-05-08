from project.Files.gui import FilesApp
from project.Webscraping.gui import MoneyApp
import customtkinter as tk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('epic')
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        
        self.money_app_btn = tk.Button(self, text='Converter', command=self.__to_money_app)
        self.money_app_btn.grid(row=0, column=1)

        self.files_app_btn = tk.Button(self, text='Files', command=self.__to_files_app)
        self.files_app_btn.grid(row=1, column=1)

        self.app_frame = tk.Frame(self)
        self.app_frame.grid_columnconfigure((0, 1), weight=1)
        self.app_frame.grid(row=0, column=0, rowspan=3, sticky='we')

        self.app = None

    def __to_money_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.money_app_btn.configure(state='disabled')
        self.files_app_btn.configure(state='normal')
        self.app = MoneyApp(self.app_frame)
        self.app.grid(row=0, column=0, sticky='we')
    
    def __to_files_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.files_app_btn.configure(state='disabled')
        self.money_app_btn.configure(state='normal')
        self.app = FilesApp(self.app_frame)
        self.app.grid(row=0, column=0, sticky='we')