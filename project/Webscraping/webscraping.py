import logging, webbrowser, shelve, bs4, requests, os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class WebScraper():
    def __init__(self):
        logging.info("WebScraper object has been created")
        self.api_key = 'kyQLr1wkOlVUFlyR0wApjQFUCGarFNVh'
    
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

    def load_from_drive(self):
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('test_data/token.json'):
            creds = Credentials.from_authorized_user_file('test_data/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'test_data/epic_client.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('test_data/token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)

            # Call the Drive v3 API
            results = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')


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
    ws = WebScraper()
    ws.load_from_drive()