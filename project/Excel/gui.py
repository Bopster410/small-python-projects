import customtkinter as ctk, openpyxl as xl, logging, excel, tkinter as tk
from tkinter import filedialog

class ExcelFileFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Canvas inside of the frame
        self.canvas = tk.Canvas(self) 

        # Horizontal scrollbar
        self.scroll_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Vertical scrollbar
        self.scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Configuring canvas
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        # Frame inside of the canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor="nw", window=self.frame)
        
        self.frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.table = {}

        self.load_test_data()

    def delete_workbook(self):
        for cell in self.table.values():
            cell.grid_forget()

    def reload_workbook_local(self, file_name, sheet):
        self.delete_workbook()

        workbook = xl.load_workbook(file_name)

        if workbook == None:
            return

        sheet = workbook[sheet]

        for row in sheet.iter_rows(min_row=0, max_row=sheet.max_row):
            for cell in row:
                if cell.value != None:
                    current_cell = ctk.CTkLabel(self.frame, text=cell.value, width=80)
                    self.table[cell.coordinate] = current_cell

                    current_cell.grid(row=cell.column, column=cell.row)
    
    def reload_workbook_drive(self, file_id, sheet):
        self.delete_workbook()

        workbook = excel.read_from_sheet(file_id, f'{sheet}!A1:U30')

        if workbook == None:
            return
        
        for row_ind, row in enumerate(workbook):
            for column_ind, cell in enumerate(row):
                if (cell != None):

                    current_cell = ctk.CTkLabel(self.frame, text=cell, width=80)
                    self.table[f'{row_ind}:{column_ind}'] = current_cell
                    
                    current_cell.grid(row=row_ind, column=column_ind)
                  
    def load_test_data(self):
        self.reload_workbook_local('aboba.xlsx', 'Лист1')


class ExcelApp(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.columnconfigure((0, 1, 2), weight=1)
        self.columnconfigure(3, weight=12)

        self.rowconfigure(1, weight=1)

        self.local_btn = ctk.CTkButton(self, text='local file', command=self.load_local_command)
        self.local_btn.grid(row=0, column=0, padx=3, pady=5)

        self.drive_btn = ctk.CTkButton(self, text='drive file', command=self.load_drive_command)
        self.drive_btn.grid(row=0, column=1, padx=3, pady=5)

        self.load_from_drive_btn = ctk.CTkButton(self, text='load from drive', command=self.load_from_drive_command)
        self.load_from_drive_btn.grid(row=0, column=2, pady=5, sticky='e')

        self.clear_btn = ctk.CTkButton(self, text='clear', command=self.clear_command)
        self.clear_btn.grid(row=0, column=3, pady=5, sticky='e')

        self.excel_file = ExcelFileFrame(self)
        self.excel_file.grid(row=1, column=0, columnspan=4, sticky="nsew")
    
    # def input_confirm_command(self):
    #     choice = self.drive_local_option.get()
    #     if choice == 'local':
    #         file_name = self.file_id_input.get()
    #         logging.info(f'file name that was entered: {file_name}')
    #         self.excel_file.reload_workbook_local(file_name, 'ИУ4-23Б')
    #     elif choice == 'drive':
    #         file_id = self.file_id_input.get()
    #         logging.info(f'file id that was entered: {file_id}')
    #         self.excel_file.reload_workbook_drive(file_id, 'ИУ4-23Б')
    #     else:
    #         logging.error('wrong choice')
        
    def clear_command(self):
        self.excel_file.delete_workbook()

    def load_local_command(self):
        file_name = filedialog.askopenfilename()
        if file_name:
            self.excel_file.reload_workbook_local(file_name, 'ИУ4-23Б')

    def load_drive_command(self):
        dialog = ctk.CTkInputDialog(text='Input id:', title='file from drive')
        input = dialog.get_input()
        if input:
            self.excel_file.reload_workbook_drive(input, 'ИУ4-23Б')
                
    def load_from_drive_command(self):
        dialog = ctk.CTkInputDialog(text='Input id:', title='file from drive')
        input = dialog.get_input()
        if input:
            file_name = filedialog.asksaveasfilename()
            if file_name:
                excel.load_from_drive(input, file_name)


if __name__ == '__main__':
    logging.basicConfig(filename='excel_gui.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    a = ctk.CTk()
    a.geometry("1024x800")
    a.rowconfigure(0, weight=1)
    a.columnconfigure(0, weight=1)
    a.resizable(False, False)

    # a_fr = ctk.CTkFrame(a)
    # a_fr.grid(row=1, column=0, columnspan=2)

    app = ExcelApp(master=a, fg_color="transparent")
    app.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    a.mainloop()