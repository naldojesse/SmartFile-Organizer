import os
import shutil
import joblib
from pathlib import Path
from watchdog.events import FileSystemEventHandler
import requests
from scripts.utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, extract_text_from_csv, extract_text_from_html, analyze_text, summarize_text, classify_text
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

file_organization_schema = {
    "documents": {
        "work": os.getenv("WORK_PATH"),
        "personal": os.getenv("PERSONAL_PATH"),
        "finance": os.getenv("FINANCE_PATH")
    },
    "images": {
        "photos": os.getenv("PHOTOS_PATH"),
        "screenshots": os.getenv("SCREENSHOTS_PATH")
    },
    "videos": {
        "movies": os.getenv("MOVIES_PATH"),
        "tutorials": os.getenv("TUTORIALS_PATH")
    }
}

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

def move_file_based_on_tags(file_path, tags, schema):
    destination = None
    text = " ".join(tags)
    category_label = classify_text(text)

    # Adjust this mapping based on your classification labels and schema
    category_mapping = {
        "work": "work",
        "personal": "personal",
        "finance": "finance",
        "photos": "photos",
        "screenshots": "screenshots",
        "misc": "misc"
    }
    category = "documents"
    subcategory = category_mapping.get(category_label.lower(), "misc")
    if category in schema and subcategory in schema[category]:
        destination = schema[category][subcategory]
    else:
        destination = os.getenv("MISC_PATH")

    create_directory_if_not_exists(destination)
    
    try:
        shutil.move(file_path, destination)
        print(f"Moved {file_path} to {destination}")
    except Exception as e:
        print(f"Error moving {file_path} to {destination}: {e}")

def analyze_existing_files(path, event_handler):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            event_handler.on_created(None, file_path)

class FileHandler(FileSystemEventHandler):
    def on_created(self, event, file_path=None):
        if event is None:
            # Handle the case when analyzing existing files
            logging.info(f"Analyzing existing file: {file_path}")
            self.process_file(file_path)
        else:
            if not event.is_directory:
                logging.info(f"New file detected: {event.src_path}")
                self.process_file(event.src_path)
            else:
                return

    def process_file(self, file_path):
        logging.info(f"Processing file: {file_path}")
        ext = Path(file_path).suffix.lower()
        text = ""
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif ext == ".docx":
            text = extract_text_from_docx(file_path)
        elif ext == ".txt":
            text = extract_text_from_txt(file_path)
        elif ext == ".csv":
            text = extract_text_from_csv(file_path)
        elif ext in [".html", ".htm"]:
            text = extract_text_from_html(file_path)

        if text:
            tags = analyze_text(text)
            summarized_text = summarize_text(" ".join(tags))
            logging.info(f"Summarized text: {summarized_text}")
            move_file_based_on_tags(file_path, [summarized_text], file_organization_schema)
        else:
            logging.warning(f"Could not extract text from file: {file_path}")
