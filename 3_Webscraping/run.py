import webscraping as ws

if __name__ == '__main__':
    ws = ws.WebScaper()
    selector = 'body > div.layout-wrapper.padding-top-default.bg-white.position-relative \
> div.layout-columns-wrapper > main > section:nth-child(5) > div.currency-board__container \
> div.currency-board > div.currency-board__table > div:nth-child(2) > div > div \
> div.currency-board__field > div.currency-board__slot__value > span.currency-board__value.display-inline-block'
    rubles = float(ws.find('https://www.banki.ru/products/currency/rub/', selector)[0].get_text().replace(',', '.'))
    print(f'1 USD == {rubles} RUB')