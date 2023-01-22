import logging, webbrowser, shelve

class WebScraper():
    def __init__(self):
        logging.info("WebScraper object has been created")
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
    ws = WebScraper()
    ws.to_favorites("https://www.youtube.com/")
    print(ws.get_favorites())