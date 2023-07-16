from project.main_app import MainApp
from project.Webscraping.gui import get_new_exchange_rate
from project.Regex.phnumbers import extract_phone_number
import argparse, sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument('-c', '--currency', help='USD -> RUB')
        args_parser.add_argument('-p', '--phone', help='extract phone number from the string')
        arguments = args_parser.parse_args()
        if arguments.currency:
            print(f'{int(arguments.currency) * get_new_exchange_rate(cache=False)} RUB')
        elif arguments.phone:
            print(extract_phone_number(arguments.phone))
        else:
            print('error')
    else:
        app = MainApp()
        app.mainloop() 