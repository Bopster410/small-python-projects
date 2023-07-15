from project.main_app import MainApp
from project.Webscraping.gui import get_new_exchange_rate
import argparse, sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument('-c', '--currency', help='USD -> RUB')
        arguments = args_parser.parse_args()
        for current_argument, current_value in vars(arguments).items():
            if current_argument == 'currency':
                print(f'{int(current_value) * get_new_exchange_rate(cache=False)} RUB')
            elif current_argument in ('-p', 'phone'):
                print('phone')
            else:
                print('error')
    else:
        app = MainApp()
        app.mainloop() 