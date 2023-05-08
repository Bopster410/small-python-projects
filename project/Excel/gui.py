import customtkinter as ctk, openpyxl as xl, logging, excel

class ExcelFileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        a = xl.load_workbook('aboba.xlsx')
        sheet = a['ИУ4-23Б']

        for row in sheet.iter_rows(min_row=0, max_row=sheet.max_row):
            for cell in row:
                if cell.value != None:
                    current_cell = ctk.CTkLabel(self, text=cell.value)
                # else:
                #     current_cell = ctk.Label(self, text='')
                current_cell.grid(row=cell.row-1, column=cell.column-1)

class ExcelApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.file_id_input = ctk.CTkEntry(self)
        self.file_id_input.grid(row=0, column=0, sticky='we')

        self.input_confirm_btn = ctk.CTkButton(self, command=self.input_confirm_command)
        self.input_confirm_btn.grid(row=0, column=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=1, column=0, columnspan=2)
        self.file_frame = ExcelFileFrame(self.frame)
        self.file_frame.grid(row=0, column=0)

    
    def input_confirm_command(self):
        file_id = self.file_id_input.get()
        logging.info(f'id that was entered: {file_id}')
        excel.load_from_drive(file_id)

if __name__ == '__main__':
    logging.basicConfig(filename='excel_gui.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    a = ctk.CTk()
    a.resizable(False, False)
    # a.geometry('600x300')

    a_fr = ctk.CTkFrame(a)
    a_fr.grid(row=1, column=0, columnspan=2)

    app = ExcelApp(a_fr)
    app.grid(row=0, column=0)

    a.mainloop()