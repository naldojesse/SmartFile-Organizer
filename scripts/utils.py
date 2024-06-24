import spacy
import PyPDF2
import docx
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import logging

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

OLLAMA_API_URL = "http://localhost:11434/api"

def extract_text_from_pdf(pdf_path, num_pages=1):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): The path of the PDF file.
        num_pages (int): The number of pages to extract text from.

    Returns:
        str: The extracted text.
    """
    logging.info(f"Extracting text from PDF: {pdf_path}")
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages[:num_pages]:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_path, num_paragraphs=5):
    """
    Extract text from a DOCX file.

    Args:
        docx_path (str): The path of the DOCX file.
        num_paragraphs (int): The number of paragraphs to extract text from.

    Returns:
        str: The extracted text.
    """
    logging.info(f"Extracting text from DOCX: {docx_path}")
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs[:num_paragraphs]])
        return text
    except docx.opc.exceptions.PackageNotFoundError:
        raise FileNotFoundError(f"File not found: {docx_path}")

def extract_text_from_txt(txt_path, num_lines=100):
    """
    Extract text from a TXT file.

    Args:
        txt_path (str): The path of the TXT file.
        num_lines (int): The number of lines to extract text from.

    Returns:
        str: The extracted text.
    """
    logging.info(f"Extracting text from TXT: {txt_path}")
    with open(txt_path, "r") as file:
        lines = file.readlines()
    return "".join(lines[:num_lines])

def extract_text_from_csv(csv_path, num_rows=10):
    """
    Extract text from a CSV file.

    Args:
        csv_path (str): The path of the CSV file.
        num_rows (int): The number of rows to extract text from.

    Returns:
        str: The extracted text.
    """
    logging.info(f"Extracting text from CSV: {csv_path}")
    df = pd.read_csv(csv_path, nrows=num_rows)
    text = df.to_string()
    return text

def extract_text_from_html(html_path, num_lines=100):
    """
    Extract text from an HTML file.

    Args:
        html_path (str): The path of the HTML file.
        num_lines (int): The number of lines to extract text from.

    Returns:
        str: The extracted text.
    """
    logging.info(f"Extracting text from HTML: {html_path}")
    with open(html_path, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        text = soup.get_text()
    return text

def analyze_text(text):
    """
    Analyze text using NLP to extract keywords.

    Args:
        text (str): The text to analyze.

    Returns:
        list: A list of unique keywords.
    """
    logging.info("Analyzing text")
    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    unique_keywords = list(set(keywords))[:10]
    return unique_keywords

def summarize_text(prompt):
    """
    Summarize text using an AI model.

    Args:
        prompt (str): The text to summarize.

    Returns:
        str: The summarized text.
    """
    logging.info("Summarizing text")
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": True
    }
    response = requests.post(f"{OLLAMA_API_URL}/generate", json=payload, stream=True)

    if response.status_code == 200:
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                data = chunk.decode('utf-8')
                json_data = json.loads(data)
                full_response += json_data.get("response", "")
        return full_response
    else:
        logging.error(f"Error summarizing text: {response.status_code}")
        return "Error: Unable to summarize text"

def classify_text(text):
    """
    Classify text using an AI model.

    Args:
        text (str): The text to classify.

    Returns:
        str: The classification label.
    """
    logging.info("Classifying text")
    payload = {
        "model": "llama3",
        "messages": [
            { "role": "user", "content": text }
        ]
    }
    response = requests.post(f"{OLLAMA_API_URL}/chat", json=payload, stream=True)

    if response.status_code == 200:
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                data = chunk.decode('utf-8')
                json_data = json.loads(data)
                full_response += json_data.get("content", "")
        return full_response
    else:
        logging.error(f"Error classifying text: {response.status_code}")
        return "Error: Unable to classify text"
