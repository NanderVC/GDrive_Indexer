from __future__ import print_function
import os
import io
import pickle
import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from app.Processing.convert_to_txt import convert_file_to_text
from app.Ingestion.ingestion import ingest_text_file, ingest_pdf_file

# Get the current working directory (current path)
current_path = os.getcwd()

# Move two folders up
BASE_FOLDER = os.path.abspath(current_path)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def download_and_ingest(index_name, file_metadata):
    """Download all files in the specified folder in Google Drive."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.


    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    page_token = None

    try:
        request = service.files().get_media(fileId=file_metadata[0])
        destination_path = os.path.join(BASE_FOLDER, file_metadata[1])
        fh = open(destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            fh.close()
            print(f'File downloaded to {destination_path}')

            _, file_extension = os.path.splitext(destination_path)

            if file_extension.lower() == ".pdf":
                ingest_pdf_file(index_name, destination_path)

            else:
                text_path = convert_file_to_text(destination_path)

                ingest_text_file(index_name, text_path)

                os.remove(text_path)

            

            os.remove(destination_path)



    except Exception as e:
        fh.close()
        os.remove(destination_path)
        print(f'An error occurred: {str(e)}')

if __name__ == "__main__":

    with open('file_metadata.pickle', 'rb') as f:
        data = pickle.load(f)
        print(data)

    test_metadata = data[-1]

    download_and_ingest("langchain-doc-index", test_metadata)



