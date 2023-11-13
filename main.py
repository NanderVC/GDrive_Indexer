from app.Google_Drive.retrieve_file_metadata import get_all_file_names_folder
from app.Google_Drive.download_ingest import download_and_ingest

import pickle

from dotenv import load_dotenv
load_dotenv()

import pinecone

if __name__ == "__main__":
    
    #Step 0: clear metadata
    # Clear the data in the pickle file
    with open('file_metadata.pickle', 'wb') as file:
        empty_data = []  # An empty data structure
        pickle.dump(empty_data, file)

    #Clear Pinecone index
    #Clear pinecone index
    pinecone.init(api_key="<YOUR PINECONE API KEY>", environment="<YOUR PINECONE ENVIRONMENT>")

    index_name = "<YOUR PINECONE INDEX NAME>"

    pinecone.delete_index(index_name)

    #OpenAI Embeddings use 1536 dimensions
    pinecone.create_index(index_name, dimension=1536)

    # #Step 1: Get all file addreses in required folder including metadata
    get_all_file_names_folder("<ID of your google drive folder>")

    with open('file_metadata.pickle', 'rb') as f:
        all_data = pickle.load(f)
        
    #Step 2: Loop over file addresses, download, clean if neccessary, convert to text, ingest, then delete
    for data in all_data:
        download_and_ingest(index_name, data)


