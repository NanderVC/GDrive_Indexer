from __future__ import print_function
import os.path
import os
import io
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload 
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Get the current working directory (current path)
current_path = os.getcwd()

# Move two folders up
base_folder = os.path.abspath(current_path)

FILE_METADATA_PATH = os.path.join(base_folder, 'file_metadata.pickle')


def get_all_file_names_folder(folder_id):
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
    while True:
        # Call the Drive v3 API
        results = service.files().list(
                q=f"'{folder_id}' in parents and (mimeType='application/pdf' or mimeType='application/vnd.google-apps.folder' or mimeType='text/plain' or mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document' or mimeType='application/vnd.google-apps.document')",
                # q = f"parents in '{FOLDER_ID}'",
                supportsAllDrives=True, 
                includeItemsFromAllDrives=True,
                #fields="nextPageToken, files(id, name)",
                pageSize=100, 
                pageToken=page_token).execute()
        items = results.get('files', [])

        if not items:
            pass
        else:
            for item in items:

                if item['mimeType'] == 'application/vnd.google-apps.folder':
                    # If the item is a folder, recursively call the function

                    get_all_file_names_folder(item['id'])

                else:
                    file_id = item['id']
                    request = service.files().get_media(fileId=file_id)

                    # Get the file resource
                    file = service.files().get(fileId=file_id, fields='webViewLink').execute()

                    # Get the web view link (shareable link)
                    web_view_link = file.get('webViewLink')

                    # Step 1: Open the pickle file in append mode
                    with open(FILE_METADATA_PATH, 'rb') as file:
                        try:
                            # Step 2: Read the existing data (if any)
                            existing_data = pickle.load(file)
                        except EOFError:
                            # If there's no existing data, start with an empty list
                            existing_data = []

                    with open(FILE_METADATA_PATH, 'wb') as f:

                        # Step 3: Append the new data to the existing data
                        existing_data.append((item['id'], item['name'], web_view_link))
                        
                        # Step 4: Write the combined data back to the pickle file
                        pickle.dump(existing_data, f)

        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break

    
