import logging, webbrowser, shelve, bs4, requests

class WebScaper():
    def __init__(self):
        logging.info("WebScraper object has been created")
    
    def get_html(self, name, local=False):
        if local:
            html = open(name)
            text = bs4.BeautifulSoup(html, 'html.parser')
        else:
            html = requests.get(name)
            text = bs4.BeautifulSoup(html.text, 'html.parser')
        return text
    
    def find(self, src, selector):
        html = self.get_html(src)
        result = html.select(selector)
        return result

class WebPages():
    def __init__(self):
        logging.info("WebPages object has been created")
        with shelve.open("user_data") as data:
            if not "fav_url" in data.keys():
                data["fav_url"] = []

    # Add url to favorites
    def to_favorites(self, url):
        logging.info(f"adding {url} to favorites")
        with shelve.open("user_data") as data:
            t = data["fav_url"]
            t.append(url)
            data["fav_url"] = t

    # Get all favorite urls    
    def get_favorites(self):
        logging.info("listing favorite urls")
        with shelve.open("user_data") as data:
            return data["fav_url"]

    # Open url in the browser
    def go_to_url(self, url):
        logging.info(f"opening {url} page")
        webbrowser.open(url)

if __name__ == '__main__':
    logging.basicConfig(filename='files.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    ws = WebScaper()
    print(ws.get_html('https://www.banki.ru/products/currency/rub/'))