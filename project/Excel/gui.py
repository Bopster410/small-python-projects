import customtkinter as ctk, openpyxl as xl, logging,tkinter as tk
from tkinter import filedialog

if __name__ == '__main__':
   import excel 
else:
    import  project.Excel.excel as excel 

# Frame with excel table
class ExcelFileFrame(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        logging.info('Creating ExcelFileFrame instance')

        super().__init__(master, **kwargs)

        self.tabs = []
        self.canvases = {}

        
    def __scroll_y(self, e):
        tab_name = self.get()
        canvas = self.canvases[tab_name] if tab_name else None
        if canvas:
            canvas.yview_scroll(int(-1*(e.delta/120)), 'units')

    def __scroll_x(self, e):
        tab_name = self.get()
        canvas = self.canvases[tab_name] if tab_name else None
        if canvas:
            canvas.xview_scroll(int(-1*(e.delta/120)), 'units')

    def __next_tab(self, e):
        current_tab_ind = self.tabs.index(self.get())
        if current_tab_ind >= len(self.tabs) - 1:
            self.set(self.tabs[0])
        else:
            self.set(self.tabs[current_tab_ind + 1])
    
    def __prev_tab(self, e):
        current_tab_ind = self.tabs.index(self.get())
        if current_tab_ind <= 0:
            self.set(self.tabs[len(self.tabs) - 1])
        else:
            self.set(self.tabs[current_tab_ind - 1])

    def __add_new_tab(self, tab_name):
        self.add(tab_name)
        # Canvas inside of the frame
        canvas = ctk.CTkCanvas(self.tab(tab_name)) 

        # Horizontal scrollbar
        scroll_x = ctk.CTkScrollbar(self.tab(tab_name), orientation='horizontal', command=canvas.xview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Vertical scrollbar
        scroll_y = ctk.CTkScrollbar(self.tab(tab_name), orientation='vertical', command=canvas.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Configuring canvas
        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Frame inside of the canvas
        frame = ctk.CTkFrame(canvas)
        canvas.create_window(0, 0, anchor="nw", window=frame)
        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame.bind('<Control-KeyPress-Tab>', self.__next_tab)
        frame.bind('<Shift-Control-KeyPress-Tab>', self.__prev_tab)

        # Binding scrollig to mousewheel
        canvas.bind_all('<MouseWheel>', self.__scroll_y)
        canvas.bind_all('<Shift-MouseWheel>', self.__scroll_x)

        self.canvases[tab_name] = canvas
        self.tabs.append(tab_name)

        return frame

    # Deletes current workbook
    def delete_workbook(self):
        for tab in self.tabs:
            self.delete(tab)
        self.tabs.clear()
        self.canvases.clear()
        # TODO remove a single sheet

    # Loads table from the local file
    def reload_workbook_local(self, file_name, sheet):
        self.delete_workbook()

        workbook = xl.load_workbook(file_name)

        if workbook == None:
            logging.warning('Something went wrong while loading the workbook')
            return
        
        logging.info(f"Loading workbook {file_name}")
        for sheet in workbook.sheetnames:
            current_sheet = workbook[sheet]

            frame = self.__add_new_tab(sheet)

            for row in current_sheet.iter_rows(min_row=0, max_row=current_sheet.max_row):
                for cell in row:
                    if cell.value != None:
                        current_cell = ctk.CTkLabel(frame, text=cell.value, width=80)
                        # TODO contain cells like this
                        # self.tabs[sheet][cell.coordinate] = current_cell

                        current_cell.grid(row=cell.column, column=cell.row)

    # Extracts table from the drive file
    def reload_workbook_drive(self, file_id, sheet):
        self.delete_workbook()

        workbook = excel.read_from_sheet(file_id)

        if not workbook:
            logging.warning('Something went wrong while loading the workbook')
            return
        
        logging.info(f"Loading workbook {file_id}")
        for sheet_name, sheet in workbook.items():
            current_sheet = self.__add_new_tab(sheet_name)
            for row_ind, row in enumerate(sheet):
                for column_ind, cell in enumerate(row):
                    if (cell != None):
                        current_cell = ctk.CTkLabel(current_sheet, text=cell, width=80)
                        # self.table[f'{row_ind}:{column_ind}'] = current_cell
                        
                        current_cell.grid(row=row_ind, column=column_ind)


# Main excel gui
class ExcelApp(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        logging.info('Creating ExcellApp instance')

        super().__init__(master, **kwargs)

       # Configuring grid 
        self.columnconfigure((0, 1, 2), weight=1)
        self.columnconfigure(3, weight=12)

        self.rowconfigure(1, weight=1)

        # Button to load local file
        self.local_btn = ctk.CTkButton(self, text='local file', command=self.load_local_command)
        self.local_btn.grid(row=0, column=0, padx=3, pady=5)

        # Button to load drive file
        self.drive_btn = ctk.CTkButton(self, text='drive file', command=self.load_drive_command)
        self.drive_btn.grid(row=0, column=1, padx=3, pady=5)

        # Button to download drive file on user's pc
        self.load_from_drive_btn = ctk.CTkButton(self, text='load from drive', command=self.load_from_drive_command)
        self.load_from_drive_btn.grid(row=0, column=2, pady=5, sticky='e')

        # Button to clear the table
        self.clear_btn = ctk.CTkButton(self, text='clear', command=self.clear_command)
        self.clear_btn.grid(row=0, column=3, pady=5, sticky='e')

        # Excel table
        self.excel_file = ExcelFileFrame(self)
        self.excel_file.grid(row=1, column=0, columnspan=4, sticky="nsew")
    
    # Clearing table
    def clear_command(self):
        logging.info('Clearing the table')
        self.excel_file.delete_workbook()

    # Extracting table from the local file
    def load_local_command(self):
        file_name = filedialog.askopenfilename()
        if file_name:
            logging.info(f'Extracting local file with name {file_name}')
            self.excel_file.reload_workbook_local(file_name, 'ИУ4-23Б')
        else:
            logging.warning('Extracting process was interrupted')

    # Extracting file from user's drive
    def load_drive_command(self):
        dialog = ctk.CTkInputDialog(text='Input id:', title='file from drive')
        input = dialog.get_input()
        if input:
            logging.info(f'Extracting drive file with id {input}')
            self.excel_file.reload_workbook_drive(input, 'ИУ4-23Б')
        else:
            logging.warning('Extracting process was interrupted')
                
    # Downloading file from user's drive
    def load_from_drive_command(self):
        dialog = ctk.CTkInputDialog(text='Input id:', title='file from drive')
        input = dialog.get_input()
        if input:
            logging.info(f'Downloading file with id {input}')
            file_name = filedialog.asksaveasfilename()
            if file_name:
                logging.info(f'Saving file as {file_name}')
                excel.load_from_drive(input, file_name)
            else:
                logging.warning('Saving process was interrupted')
        else:
            logging.warning('Downloading was interrupted')



if __name__ == '__main__':
    logging.basicConfig(filename='excel_gui.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    a = ctk.CTk()
    a.geometry("1024x800")
    a.rowconfigure(0, weight=1)
    a.columnconfigure(0, weight=1)
    a.resizable(False, False)

    app = ExcelApp(master=a, fg_color="transparent")
    app.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    a.mainloop()