import customtkinter as ctk, webscraping, logging  

class MoneyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # WebScraper object to get exchange rate
        self.ws = webscraping.WebScaper()

        # Window settings
        self.title('Simple test, no need to worry')
        self.geometry('500x500')

        # Label showing current exchange rate
        self.exchange_rate_lbl = ctk.CTkLabel(self, text=f'1 USD == {self.__get_new_exchange_rate()} RUB', font=('Arial', 25))
        self.exchange_rate_lbl.pack(pady=30)

        # Frame with converter
        self.converter_frame = ctk.CTkFrame(self, width=450, height=350)
        self.converter_frame.pack()

        # Input value
        self.input_lbl = ctk.CTkEntry(self.converter_frame, width=140, height=50, corner_radius=8, font=('Arial', 20))
        self.input_lbl.place(relx=0.2, rely=0.5)

        # Button to show the result
        self.enter_btn = ctk.CTkButton(self.converter_frame, height=50, text='Enter', command=self.enter_event, font=('Arial', 20))
        self.enter_btn.place(relx=0.6, rely=0.5)

        # Result label
        self.result_lbl = ctk.CTkLabel(self.converter_frame, width=200, height=50, corner_radius=8, font=('Arial', 20), text='')
        self.result_lbl.place(relx=0.4, rely=0.7)
    
    # Callback for the enter button (enter_btn)
    # TODO use cache to get exchange rate
    # TODO regex to validate input
    def enter_event(self):
        input = float(self.input_lbl.get())
        logging.debug(f'entered value: {input}')
        self.result_lbl.configure(text=f'{round(input * self.__get_new_exchange_rate(), 2)} RUB')
    
    # Returns current usd to rub exchange rate
    # TODO use cache to store exchange rate
    def __get_new_exchange_rate(self):
        selector = 'body > div.layout-wrapper.padding-top-default.bg-white.position-relative \
> div.layout-columns-wrapper > main > section:nth-child(5) > div.currency-board__container \
> div.currency-board > div.currency-board__table > div:nth-child(2) > div > div \
> div.currency-board__field > div.currency-board__slot__value > span.currency-board__value.display-inline-block'
        # rubles = float(self.ws.find('https://www.banki.ru/products/currency/rub/', selector)[0].get_text().replace(',', '.'))
        rubles = 75.5
        return rubles


if __name__ == '__main__':
    logging.basicConfig(filename='gui.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    app = MoneyApp()
    app.mainloop()