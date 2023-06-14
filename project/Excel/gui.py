import customtkinter as ctk, openpyxl as xl, logging, excel

class ExcelFileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.table = {}

    def delete_workbook(self):
        for cell in self.table.values():
            cell.grid_forget()

    def reload_workbook_local(self, file_name):
        self.delete_workbook()

        workbook = xl.load_workbook(file_name)
        sheet = workbook['ИУ4-23Б']

        for row in sheet.iter_rows(min_row=0, max_row=sheet.max_row):
            for cell in row:
                if cell.value != None:
                    current_cell = ctk.CTkLabel(self, text=cell.value)
                    self.table[cell.coordinate] = current_cell
                # else:
                #     current_cell = ctk.Label(self, text='')
                    current_cell.grid(row=cell.row-1, column=cell.column-1)
    
    def reload_workbook_drive(self, file_id):
        self.delete_workbook()

        workbook = excel.read_from_sheet(file_id, 'ИУ4-23Б!A1:P30')

        for row_ind, row in enumerate(workbook):
            for column_ind, cell in enumerate(row):
                if (cell != None):

                    current_cell = ctk.CTkLabel(self, text=cell)
                    self.table[f'{row_ind}:{column_ind}'] = current_cell
                    # else:
                    #     current_cell = ctk.Label(self, text='')
                    current_cell.grid(row=row_ind, column=column_ind)


class ExcelApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.file_id_input = ctk.CTkEntry(self, placeholder_text='File name')
        self.file_id_input.grid(row=0, column=0, sticky='we')

        self.input_confirm_btn = ctk.CTkButton(self, text='Enter', command=self.input_confirm_command)
        self.input_confirm_btn.grid(row=0, column=1)

        self.clear_btn = ctk.CTkButton(self, text='clear', command=self.clear_command)
        self.clear_btn.grid(row=0, column=2)

        self.load_from_drive_btn = ctk.CTkButton(self, text='load from drive', command=self.load_from_drive_command)
        self.load_from_drive_btn.grid(row=0, column=3)

        self.drive_local_option = ctk.CTkOptionMenu(self, values=['drive', 'local'])
        self.drive_local_option.grid(row=0, column=4)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=1, column=0, columnspan=5)
        self.excel_file = ExcelFileFrame(self.frame)
        self.excel_file.grid(row=0, column=0)
    
    def input_confirm_command(self):
        choice = self.drive_local_option.get()
        if choice == 'local':
            file_name = self.file_id_input.get()
            logging.info(f'file name that was entered: {file_name}')
            self.excel_file.reload_workbook_local(file_name)
        elif choice == 'drive':
            file_id = self.file_id_input.get()
            logging.info(f'file id that was entered: {file_id}')
            self.excel_file.reload_workbook_drive(file_id)
        else:
            logging.error('wrong choice')

        
    def clear_command(self):
        self.excel_file.delete_workbook()

    def load_from_drive_command(self):
        dialog = ctk.CTkInputDialog(text='Input id:', title='file from drive')
        excel.load_from_drive(dialog.get_input())


if __name__ == '__main__':
    logging.basicConfig(filename='excel_gui.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    a = ctk.CTk()
    a.resizable(False, False)

    # a_fr = ctk.CTkFrame(a)
    # a_fr.grid(row=1, column=0, columnspan=2)

    app = ExcelApp(a)
    app.grid(row=0, column=0)

    a.mainloop()