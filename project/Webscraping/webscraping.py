import logging, webbrowser, shelve, bs4, requests


class WebScraper():
    def __init__(self, api_key):
        logging.info("WebScraper object has been created")
        self.api_key = api_key
    
    def get_html(self, name, local=False):
        if local:
            html = open(name)
            text = bs4.BeautifulSoup(html, 'html.parser')
        else:
            html = requests.get(name)
            text = bs4.BeautifulSoup(html.text, 'html.parser')
        return text
    
    def find(self, src, selector):
        result = None
        with shelve.open('cache/WebScraper_cache') as cache_db:
            db_tag = 'bob'
            try:
                html = self.get_html(src)
                result = html.select(selector)[0].get_text()
                cache_db[db_tag] = result
            except requests.exceptions.ConnectionError:
                if db_tag in cache_db.keys():
                    result = cache_db[db_tag]
                    
        return result

    def use_api(self, url, params, cache=True):
        with shelve.open('cache/WebScraper_cache') as cache_db:
            db_tag = ''.join((url, ''.join(params)))
            if db_tag in cache_db.keys() and cache:
                respons = cache_db[db_tag]
                logging.info('api respons from cache was taken')
            else:
                try:
                    respons = requests.request('GET', url, headers={'apikey': self.api_key}, params=params)
                    cache_db[db_tag] = respons
                    logging.info('api was used')
                except requests.exceptions.ConnectionError:
                    logging.critical('connection problems')
                    respons = None
        return respons

    def save_file(self, file, save_as_name):
        file_on_hard_drive = open(save_as_name, 'wb')
        for chunk in file.iter_content(100000):
            file_on_hard_drive.write(chunk)


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
    with open('api_key') as api_ley_file:
        ws = WebScraper(api_ley_file.readline)
    