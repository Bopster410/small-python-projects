import customtkinter as ctk, re, logging

if __name__ == '__main__':
    import webscraping, currency
else:
    import project.Webscraping.webscraping as webscraping, project.Webscraping.currency as currency 


# Currency converter frame
class ConverterFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configure grid
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure(2, weight=2)

        # Label showing current exchange rate
        exchange_rate = get_new_exchange_rate()
        self.exchange_rate_value = ctk.StringVar(value=f'1 USD == {exchange_rate} RUB')
        self.exchange_rate_lbl = ctk.CTkLabel(self, font=('Arial', 25), textvariable=self.exchange_rate_value)
        self.exchange_rate_lbl.grid(column=0, row=0, columnspan=2, pady=10, sticky='ew')

        # Button to update current exchange rate
        self.update_rate_btn = ctk.CTkButton(self, height=30, text='Update', command=self.update_rate_event)
        self.update_rate_btn.grid(column=2, row=0, padx=20, sticky='e')

        # Input currency
        self.currency_menu_input = ctk.CTkOptionMenu(self, values=['USD', 'RUB'], command=self.currency_menu_event)
        self.currency_menu_input.grid(row=1, column=0, padx=20, pady=10, sticky='we')

        # Output currency
        self.currency_menu_output = ctk.CTkOptionMenu(self, values=['RUB', 'USD' ], command=self.currency_menu_event)
        self.currency_menu_output.grid(row=1, column=1, pady=20,  sticky='we')

        # Button to show the result
        self.enter_btn = ctk.CTkButton(self, height=50, text='Enter', command=self.enter_event, font=('Arial', 20))
        self.enter_btn.grid(row=1, column=2, padx=20, pady=10, rowspan=2, sticky='esn')
        
        # Input value
        self.input_entry = ctk.CTkEntry(self, height=50, corner_radius=8, font=('Arial', 20))
        self.input_entry.grid(row=2, column=0, padx=20, pady=10 , sticky='ewsn')        

        # Result label
        self.result_value = ctk.StringVar(value='result')
        self.result_lbl = ctk.CTkLabel(self,  font=('Arial', 20), fg_color=('white', 'black'), height=50, corner_radius=8, textvariable=self.result_value)
        self.result_lbl.grid(row=2, column=1, sticky='ew')

        # Error label
        self.error_value = ctk.StringVar()
        self.error_lbl = ctk.CTkLabel(self, font=('Arial', 20), textvariable=self.error_value)
        self.error_lbl.grid(row=3, column=0, columnspan=3)
        
        # Bank for currency conversion
        self.bank = currency.Bank()
        self.bank.add_rate('USD', 'RUB', 1 / exchange_rate)
        self.bank.add_rate('RUB', 'USD', exchange_rate)


    # Callback for the enter button (enter_btn)
    def enter_event(self):
        input_val_str = self.input_entry.get()

        if self.validate_input(input_val_str):
            self.error_value.set('')
            input = currency.Money(self.currency_menu_input.get(), float(input_val_str))
            logging.debug(f'entered value: {input.amount()}')
            output = input.reduce(self.currency_menu_output.get(), bank=self.bank)
            self.result_value.set(output)

        else:
            self.on_invalid_input()

    # Updates current rate when button update_rate_btn is clicked
    def update_rate_event(self):
        logging.debug('Update button was clicked')
        self.exchange_rate_value.set(f'1 USD == {get_new_exchange_rate(cache=False)} RUB')

    
    def validate_input(self, input):
        result = re.fullmatch(r'\d+(\.{1}\d+)?', input)
        return result != None

    def on_invalid_input(self):
        logging.debug('Wrong value!')
        self.error_value.set('Wrong input value!')

    def currency_menu_event(self, currency):
        logging.debug('Option menu clicked: ' + currency)


class MoneyApp(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Label showing current exchange rate
        self.exchange_rate_lbl = ctk.CTkLabel(self, text='Money app!', font=('Arial', 25))
        self.exchange_rate_lbl.grid(column=0, row=0, sticky="ew")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)


        # Frame with converter
        self.converter_frame = ConverterFrame(self)
        self.converter_frame.grid(column=0, row=1, padx=20, pady=10, sticky="nsew")


# Returns current usd to rub exchange rate
# TODO use cache to store exchange rate
def get_new_exchange_rate(cache=True):
#     selector = 'body > div.layout-wrapper.padding-top-default.bg-white.position-relative \
# > div.layout-columns-wrapper > main > section:nth-child(5) > div.currency-board__container \
# > div.currency-board > div.currency-board__table > div:nth-child(2) > div > div \
# > div.currency-board__field > div.currency-board__slot__value > span.currency-board__value.display-inline-block'
#     web_scraping_result = ws.find('https://www.banki.ru/products/currency/rub/', selector)
#     if web_scraping_result != None:
#         rubles = float(web_scraping_result.replace(',', '.'))
#     else:
#         rubles = 0
    with open('api_key') as api_key_file:
        api_key = api_key_file.readline()
    ws = webscraping.WebScraper(api_key)
    url = 'https://api.apilayer.com/fixer/latest'
    params = {'base': 'USD', 'symbols': 'RUB'}
    result = ws.use_api(url, params, cache)
    if result == None:
        logging.critical('error with exchange rate update')
        rubles = 1
    else:
        rubles = round(result.json()['rates']['RUB'], 2)
    # rubles = 75.5
    return rubles


if __name__ == '__main__':
    logging.basicConfig(filename='gui.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    a = ctk.CTk()
    a.geometry("1024x800")
    a.rowconfigure(0, weight=1)
    a.columnconfigure(0, weight=1)
    a.resizable(False, False)

    app = MoneyApp(master=a)
    app.grid(row=0, column=0, sticky='nswe')
    a.mainloop()