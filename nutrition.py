import os
import requests

# Get PDF document
pdf_path = "human-nutrition-text.pdf"

# Download PDF if it doesn't already exist
if not os.path.exists(pdf_path):
    print("File doesn't exist, downloading...")

    # The URL of the PDF you want to download
    url = "https://pressbooks.oer.hawaii.edu/humannutrition2/open/download?type=pdf"

    #The local filename to save the downloaded file 
    filename = pdf_path

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in binary write mode and save the content to it
        with open(pdf_path, "wb") as file:
            file.write(response.content)

        print(f"The file has been downloaded and saved as {pdf_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
else:
    print(f"File '{pdf_path}' already exists.")




#requires !pip install PyMuPDF, see: https://github.com/pymupdf/pymupdf
import fitz  # PyMuPDF, found this is better thay pypdf for our use case, note: lincence is AGPL-3.0,
from tqdm.auto import tqdm


def text_formatter(text: str) -> str:
    """
    Performs minor formatting on text.
    """
    cleaned_text = text.replace("\n", " ").strip()

    # Other potential text formatting functions can go here

    return cleaned_text


def open_and_read_pdf(pdf_path: str) -> list[dict]:
    """
    Opens a PDF file, reads its text content page by page,
    and collects statistics.

    Parameters:
        pdf_path (str): The file path to the PDF document.

    Returns:
        list[dict]: A list of dictionaries containing page statistics
        and extracted text.
    """

    doc = fitz.open(pdf_path)
    pages_and_texts = []

    for page_number, page in tqdm(enumerate(doc)):  #iterate the document pages
        text = page.get_text()    #get plain text encoded as UTF-8
        text = text_formatter(text)
        pages_and_texts.append({
            "page_number": page_number - 41,  #adjust page number
            "page_char_count": len(text),
            "page_word_count": len(text.split(" ")),
            "page_sentence_count": len(text.split(". ")),
            "page_token_count": len(text) / 4,  # rough estimate 1 token = ~4 chars
            "text": text
        })

    return pages_and_texts

pages_and_texts = open_and_read_pdf(pdf_path)
pages_and_texts[:2]




import random
print(random.sample(pages_and_texts, k=3))