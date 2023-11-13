import os
from dotenv import load_dotenv
load_dotenv()

from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import NotionDirectoryLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone

pinecone.init(api_key="<YOUR PINECONE API KEY>", environment="<YOUR PINECONE ENVIRONMENT>")

def ingest_docx_folder(index_name, folder_path):

    loader = DirectoryLoader(folder_path, loader_cls=Docx2txtLoader)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ",""])
    documents = text_splitter.split_documents(documents=data)
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)

    return documents

def ingest_pdf_folder(index_name, folder_path):

    loader = DirectoryLoader(folder_path, loader_cls=PyPDFLoader)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ",""])
    documents = text_splitter.split_documents(documents=data)
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)

    return documents

def ingest_text_folder(index_name, folder_path):

    text_loader_kwargs={'autodetect_encoding': True}
    loader = DirectoryLoader(folder_path,glob="./*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ",""])
    documents = text_splitter.split_documents(documents=data)
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)

    return documents

def ingest_notion(index_name, folder_path):

    loader = DirectoryLoader(folder_path,glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ",""])
    documents = text_splitter.split_documents(documents=data)
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)

    return documents

def ingest_pdf_file(index_name, file_path):

    loader = PyPDFLoader(file_path)
    data = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ",""])
    documents = text_splitter.split_documents(documents=data)
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)

    return documents

def ingest_text_file(index_name, file_path):

    loader = TextLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ",""])
    documents = text_splitter.split_documents(documents=data)
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)

    return documents