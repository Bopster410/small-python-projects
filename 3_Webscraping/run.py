from gui import MoneyApp
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='money_app.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    app = MoneyApp()
    app.mainloop()