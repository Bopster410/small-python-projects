import customtkinter as ctk, webscraping

class MoneyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.ws = webscraping.WebScaper()
        self.title = 'Simple test, no need to worry'
        self.geometry('500x500')

        self.label = ctk.CTkLabel(self, text=f'1 USD == {self.__get_new_currency()} RUB', font=('Arial', 25))
        self.label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    def __get_new_currency(self):
        selector = 'body > div.layout-wrapper.padding-top-default.bg-white.position-relative \
> div.layout-columns-wrapper > main > section:nth-child(5) > div.currency-board__container \
> div.currency-board > div.currency-board__table > div:nth-child(2) > div > div \
> div.currency-board__field > div.currency-board__slot__value > span.currency-board__value.display-inline-block'
        # rubles = float(self.ws.find('https://www.banki.ru/products/currency/rub/', selector)[0].get_text().replace(',', '.'))
        rubles = 75.5
        return rubles



if __name__ == '__main__':
    app = MoneyApp()
    app.mainloop()