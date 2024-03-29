import sys, os.path, io, logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

def google_auth(token_path, creds_path):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(
            token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds


def load_from_drive(file_id, saveas_name, token_path, creds_path):
    creds = google_auth(token_path, creds_path)
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    try:
        service = build('drive', 'v3', credentials=creds)
        request = service.files().export_media(fileId=file_id,
                                               mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logging.info(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        logging.error(f'An error occurred: {error}')

    with open(saveas_name, 'wb') as input:
        input.write(file.getvalue())


def read_from_sheet(file_id, token_path, creds_path):
    creds = google_auth(token_path, creds_path)
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.get(spreadsheetId=file_id).execute()
        # values = result.get('values', [])
        tabs = {}
        if 'sheets' in result:
            for tab in result['sheets']:
                title = tab['properties']['title']
                tabs[title] = sheet.values().get(spreadsheetId=file_id, range=title).execute().get('values', [])

        if not tabs:
            logging.info('No data found.')
            return

        return tabs
    
    except HttpError as err:
        logging.error(err)


if __name__ == '__main__':
    logging.basicConfig(filename='excel.log', filemode='w', level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s, %(lineno)d: %(message)s')
    if (len(sys.argv) == 2):
        print(read_from_sheet(sys.argv[1]))
    # load_from_drive(sys.argv[1])

    # a = xl.load_workbook('aboba.xlsx')
    # sheet = a['ИУ4-23Б']

    # for row in sheet.iter_rows(min_row=3, max_row=sheet.max_row - 2):
    #     print(f'{row[0].value}: ', end='')
    #     for cell in row[1:]:
    #         if cell.value == None:
    #             print('')
    #             break
    #         print(cell.value, end=' ')
