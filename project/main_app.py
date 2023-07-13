from project.Files.gui import FilesApp
from project.Webscraping.gui import MoneyApp
from project.Excel.gui import ExcelApp
import customtkinter as ctk

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('epic')
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1, 2), weight=1)
        
        self.money_app_btn = ctk.CTkButton(self, text='Converter', command=self.__to_money_app)
        self.money_app_btn.grid(row=0, column=0, sticky='w')

        self.files_app_btn = ctk.CTkButton(self, text='Files', command=self.__to_files_app)
        self.files_app_btn.grid(row=0, column=1, sticky='we')

        self.excel_app_btn = ctk.CTkButton(self, text='Excel', command=self.__to_excel_app)
        self.excel_app_btn.grid(row=0, column=2, sticky='e')

        self.app_frame = ctk.CTkFrame(self)
        self.app_frame.columnconfigure(0, weight=1)
        self.app_frame.rowconfigure(0, weight=1)
        self.app_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')

        self.app = None

    def __to_money_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.files_app_btn.configure(state='normal')
        self.money_app_btn.configure(state='disabled')
        self.excel_app_btn.configure(state='normal')
        self.app = MoneyApp(master=self.app_frame)
        self.app.grid(row=0, column=0, sticky='nswe')
    
    def __to_files_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.files_app_btn.configure(state='disabled')
        self.money_app_btn.configure(state='normal')
        self.excel_app_btn.configure(state='normal')
        self.app = FilesApp(master=self.app_frame)
        self.app.grid(row=0, column=0, sticky='nswe')

    def __to_excel_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.files_app_btn.configure(state='normal')
        self.money_app_btn.configure(state='normal')
        self.excel_app_btn.configure(state='disabled')
        self.app = ExcelApp(master=self.app_frame)
        self.app.grid(row=0, column=0, sticky='nswe')
