import logging, webbrowser

class WebScraper():
    def __init__(self):
        logging.info("WebScraper object has been created")

    def go_to_url(self, url):
        logging.info(f"opening {url} page")
        webbrowser.open(url)

if __name__ == '__main__':
    logging.basicConfig(filename='files.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    ws = WebScraper()
    ws.go_to_url("https://www.youtube.com/")