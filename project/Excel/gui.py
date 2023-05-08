import customtkinter as ctk, excel, logging

class ExcelApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.file_id_input = ctk.CTkEntry(self, placeholder_text='aboba')
        self.file_id_input.grid(row=0, column=0, sticky='we')

        self.input_confirm_btn = ctk.CTkButton(self, command=self.input_confirm_command)
        self.input_confirm_btn.grid(row=0, column=1)
    
    def input_confirm_command(self):
        file_id = self.file_id_input.get()
        logging.info(f'id that was entered: {file_id}')
        excel.load_from_drive(file_id)

if __name__ == '__main__':
    logging.basicConfig(filename='excel_gui.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    a = ctk.CTk()
    a.geometry('600x300')

    a_fr = ctk.CTkFrame(a)
    a_fr.grid(row=1, column=0, columnspan=2)

    app = ExcelApp(a_fr)
    app.grid(row=0, column=0)

    a.mainloop()