from project.Files.gui import FilesApp
from project.Webscraping.gui import MoneyApp
from project.Excel.gui import ExcelApp
from project.Time.time import TasksManager
import customtkinter as ctk

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1024x800')
        self.title('epic')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.open_left_panel_btn = ctk.CTkButton(self, text='=', width=40, height=40, command=self.__change_left_panel_state)
        self.open_left_panel_btn.grid(row=0, column=0, sticky='nw', padx=2, pady=2)

        self.left_panel_frame = ctk.CTkFrame(self, width=140)
        self.left_panel_frame.columnconfigure(0, weight=1)
        self.left_panel_frame.grid(row=0, column=1, sticky='nsew')
        self.left_panel_state = 'shown'
        
        self.money_app_btn = ctk.CTkButton(self.left_panel_frame, text='Converter', command=self.__to_money_app)
        self.money_app_btn.grid(row=0, column=0, sticky='we', padx=5, pady=2)

        self.files_app_btn = ctk.CTkButton(self.left_panel_frame, text='Files', command=self.__to_files_app)
        self.files_app_btn.grid(row=1, column=0, sticky='we', padx=5, pady=(0,2))

        self.excel_app_btn = ctk.CTkButton(self.left_panel_frame, text='Excel', command=self.__to_excel_app)
        self.excel_app_btn.grid(row=2, column=0, sticky='we', padx=5, pady=(0,2))

        self.task_manager_btn = ctk.CTkButton(self.left_panel_frame, text='Tasks', command=self.__to_time_app)
        self.task_manager_btn.grid(row=3, column=0, sticky='we', padx=5)


        self.app_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.app_frame.columnconfigure(0, weight=1)
        self.app_frame.rowconfigure(0, weight=1)
        self.app_frame.grid(row=0, column=2, sticky='nsew')

        self.left_panel_frame.grid_propagate(0)

        self.app = None
    
    def __change_left_panel_state(self):
        if self.left_panel_state == 'shown':
            self.left_panel_frame.grid_forget()
            self.left_panel_state = 'hidden'
        else:
            self.left_panel_frame.grid(row=0, column=1, sticky='nsew')
            self.left_panel_state = 'shown'
            self.left_panel_frame.grid_propagate(0)

    def __to_money_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.files_app_btn.configure(state='normal')
        self.money_app_btn.configure(state='disabled')
        self.excel_app_btn.configure(state='normal')
        self.task_manager_btn.configure(state='normal')
        self.app = MoneyApp(master=self.app_frame)
        self.app.grid(row=0, column=0, sticky='nswe')
        # self.left_panel_frame.grid_propagate(0)
    
    def __to_files_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.files_app_btn.configure(state='disabled')
        self.money_app_btn.configure(state='normal')
        self.excel_app_btn.configure(state='normal')
        self.app = FilesApp(master=self.app_frame)
        self.app.grid(row=0, column=0, sticky='nswe')
        # self.left_panel_frame.grid_propagate(0)

    def __to_excel_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.files_app_btn.configure(state='normal')
        self.money_app_btn.configure(state='normal')
        self.excel_app_btn.configure(state='disabled')
        self.task_manager_btn.configure(state='normal')
        self.app = ExcelApp(master=self.app_frame)
        self.app.grid(row=0, column=0, sticky='nswe')
        # self.left_panel_frame.grid_propagate(0)
    
    def __to_time_app(self):
        if self.app != None:
            self.app.grid_forget()
        
        self.files_app_btn.configure(state='normal')
        self.money_app_btn.configure(state='normal')
        self.excel_app_btn.configure(state='normal')
        self.task_manager_btn.configure(state='disabled')
        self.app = TasksManager(master=self.app_frame)
        self.app.grid(row=0, column=0, sticky='nswe')
        # self.left_panel_frame.grid_propagate(0)
