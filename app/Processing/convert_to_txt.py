import os
import docx2txt

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def convert_file_to_text(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.docx':
        # Convert DOCX to text
        try:
            text = docx2txt.process(file_path)
            text_path = file_path.split(".")[-2] + ".txt"
            #Note Im ignoring characxters with unknown encoding
            with open(text_path, 'w', errors='ignore') as file:
                file.writelines(text)
        except Exception as e:
            print(f"Error converting DOCX to text: {str(e)}")

    elif file_extension.lower() == '.pdf':
        # Convert PDF to text
        try:
            output_string = StringIO()
            with open(file_path, 'rb') as in_file:
                parser = PDFParser(in_file)
                doc = PDFDocument(parser)
                rsrcmgr = PDFResourceManager()
                device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.create_pages(doc):
                    interpreter.process_page(page)

               
            text_path = file_path.split(".")[-2] + ".txt"

            with open(text_path, 'w') as file:
                print(output_string.getvalue(), file=file)

        except Exception as e:
            print(f"Error converting PDF to text: {str(e)}")

    elif file_extension.lower() == '.txt':
        # The file is already in text format, just read and return its content
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except Exception as e:
            print(f"Error reading text file: {str(e)}")

    else:
        # Unsupported file format
        print(f"Unsupported file format: {file_extension}")
        return None
    
    return text_path


