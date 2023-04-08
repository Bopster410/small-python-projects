from gui import FilesApp
import logging

def main():
    logging.basicConfig(filename='files.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    app = FilesApp()
    app.mainloop()

if __name__ == '__main__':
    main()