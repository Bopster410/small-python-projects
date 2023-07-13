import customtkinter as ctk, logging, tkinter as tk 
from pathlib import Path

if __name__ == '__main__':
    import files
else:
    import project.Files.files as files

class FilesApp(ctk.CTkFrame):
    def __init__(self, master):
        logging.info('FilesApp object was created')
        super().__init__(master)

        # Init window settings
        # self.title('Files app')
        # self.geometry('700x500')
        self.columnconfigure((0, 1), weight=1)

        # Current working directory
        self.cwd = Path.cwd()
        self.cwd_str = ctk.StringVar(value=str(self.cwd))
 
        # Label for cwd
        self.current_dir = ctk.CTkLabel(self, textvariable=self.cwd_str, font=('Arial', 20))
        self.current_dir.grid(column=0, row=0, pady=10, padx=10, sticky="w")
        
        # Popup menu
        self.popup_command = None
        self.popup_file = tk.Menu(self, tearoff=False)
        self.popup_file.add_command(label='copy', command=self.__popup_copycut_command('copy'))
        self.popup_file.add_command(label='cut', command=self.__popup_copycut_command('cut'))
        self.popup_file.add_command(label='paste', command=self.__popup_paste_command())
        
        self.popup_general = tk.Menu(self, tearoff=False)
        self.popup_general.add_command(label='paste', command=self.__popup_paste_command())

        self.selected_dir = None
        self.src_path = None

        # Child directories inside cwd
        self.dirs_frame = ctk.CTkScrollableFrame(self, width=400, height=300, border_width=1, border_color="black")
        self.dirs_frame.grid(column=0, row=1, columnspan=2, sticky="we")
        self.dirs_frame.bind('<Button-3>', self.__popup_general_command())
        self.inner_dirs_btns = self.__form_inner_dirs()
        self.__grid_all(self.inner_dirs_btns, first_row=1)

    # Updates directories and files listed in cwd
    def reload_dirs(self):
        self.__grid_forget_all(self.inner_dirs_btns)
        self.inner_dirs_btns = self.__form_inner_dirs()
        self.__grid_all(self.inner_dirs_btns, first_row=1)
    
    # Callback for item copying
    def __popup_copycut_command(self, command: str):
        def popup_copycut_command():
            logging.debug('Label "copy" in the popup was clicked')
            if self.selected_dir != None:
                self.src_path = self.cwd / self.selected_dir.cget('text')
                self.popup_command = command
                logging.debug(f'New src_path: {self.src_path}')
        return popup_copycut_command
    

    # Callback for item pasting
    def __popup_paste_command(self):
        def popup_paste_command():
            logging.debug('Label "paste" in the popup was clicked')
            if self.src_path != None:
                fm = files.FileManipulator()
                if self.popup_command == 'copy':
                    logging.debug(f'Copying from {self.src_path} to {self.cwd / self.src_path.name}')
                    fm.copy(self.src_path, self.cwd / self.src_path.name)
                elif self.popup_command == 'cut':
                    fm.move(self.src_path, self.cwd / self.src_path.name)
                self.reload_dirs()
        return popup_paste_command
    
    # Callback for files popup appearance
    def __popup_file_command(self, dir: ctk.CTkButton):
        def popup_file_command(event):
            self.popup_file.tk_popup(event.x_root, event.y_root)
            self.selected_dir = dir
            logging.debug(f'Current selected dir is {dir.cget("text")}')
        return popup_file_command
    
    # Callbak for general popup appearance
    def __popup_general_command(self):
        def popup_general_command(event):
            self.popup_general.tk_popup(event.x_root, event.y_root)
            logging.debug('General popup was activated')
        return popup_general_command

    # Callback for changing cwd
    def __change_dir_event(self, new_dir):
        # If new_dir is buttons folder, open it,
        # else just leave everything as it is
        def change_dir_event(event):
            if (self.cwd / new_dir).is_dir():
                if new_dir == '..':
                    self.cwd = self.cwd.parent
                else:
                    self.cwd = self.cwd / new_dir
                self.cwd_str.set(str(self.cwd))
                self.reload_dirs()
        return change_dir_event
    
    # Callback for item hovering
    def __dir_hover_event(self, dir: ctk.CTkButton):
        def dir_hover_event(event):
            dir.configure(border_color="#257cee")
        return dir_hover_event
    
    # Callback for leaving item after hovering it
    def __dir_leave_event(self, dir: ctk.CTkButton):
        def dir_leave_event(event):
            dir.configure(border_color="#0F0F0F")
        return dir_leave_event
    
    # Updates list with all the items inside the cwd
    def __form_inner_dirs(self):
        # Child directories inside cwd
        inner_dirs = (['..'] if self.cwd.parent != self.cwd else []) + [child.name for child in self.cwd.iterdir()]
        # ..and buttons for all of them
        buttons = list()
        for child in inner_dirs:
            btn = ctk.CTkButton(self.dirs_frame, text=child, fg_color="white", border_color="#0F0F0F", border_width=2, text_color="black",
                              font=('Arial', 17), anchor="w", width=400, hover=False)
            btn.bind('<Double-Button-1>', self.__change_dir_event(child))
            btn.bind('<Motion>', self.__dir_hover_event(btn))
            btn.bind('<Leave>', self.__dir_leave_event(btn))
            if child != '..':
                btn.bind('<Button-3>', self.__popup_file_command(btn))
            buttons.append(btn)
        return buttons
    
    # Forgets all grid elements in [object]
    def __grid_forget_all(self, objects):
        for i in range(len(objects)):
            objects[i].grid_forget()

    # Adds all elements from [objects] to grid
    def __grid_all(self, objects, first_row=0):
        for i in range(len(objects)):
            objects[i].grid(column=0, row=i+first_row, columnspan=2, sticky='we', padx=10)
 
if __name__ == '__main__':
    logging.basicConfig(filename='files_gui.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    a = ctk.CTk()
    a.geometry("1024x800")
    a.rowconfigure(0, weight=1)
    a.columnconfigure(0, weight=1)
    a.resizable(False, False)

    app = FilesApp(master=a)
    app.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    a.mainloop()