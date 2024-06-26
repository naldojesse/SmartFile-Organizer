import os
import shutil
import joblib
from pathlib import Path
from watchdog.events import FileSystemEventHandler
import requests
from scripts.utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, extract_text_from_csv, extract_text_from_html, analyze_text, summarize_text, classify_text
from dotenv import load_dotenv
import logging
import subprocess

# Load environment variables
load_dotenv()

# Define the file organization schema based on environment variables
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
    """
    Create a directory if it does not already exist.

    Args:
        directory_path (str): The path of the directory to create.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

def apply_macos_tags(file_path, tags):
    """
    Apply macOS tags to a file.

    Args:
        file_path (str): The path of the file to tag.
        tags (list): A list of tags to apply to the file.
    """
    tag_string = ','.join(tags)
    try:
        subprocess.run(['xattr', '-w', 'com.apple.metadata:_kMDItemUserTags', tag_string, file_path], check=True)
        logging.info(f"Applied tags {tag_string} to {file_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to apply tags to {file_path}: {e}")

def get_existing_tags(file_path):
    """
    Get existing macOS tags for a file.

    Args:
        file_path (str): The path of the file to check.

    Returns:
        list: A list of existing tags.
    """
    try:
        result = subprocess.run(['xattr', '-p', 'com.apple.metadata:_kMDItemUserTags', file_path], 
                                capture_output=True, text=True, check=True)
        tags = result.stdout.strip().split(',')
        return [tag.strip() for tag in tags if tag.strip()]
    except subprocess.CalledProcessError:
        return []

def move_file_based_on_tags(file_path, tags, schema):
    """
    Move a file to a destination directory based on its tags.

    Args:
        file_path (str): The path of the file to move.
        tags (list): A list of tags associated with the file.
        schema (dict): The file organization schema.
    """
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
        apply_macos_tags(file_path, tags)
        new_file_path = os.path.join(destination, os.path.basename(file_path))
        shutil.move(file_path, new_file_path)
        print(f"Moved {file_path} to {new_file_path}")
        return new_file_path
    except Exception as e:
        logging.error(f"Error moving {file_path} to {destination}: {e}")
        return None

def analyze_existing_files(path, event_handler):
    """
    Analyze existing files in a directory.

    Args:
        path (str): The path of the directory to analyze.
        event_handler (FileSystemEventHandler): The event handler to process files.
    """
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            event_handler.on_created(None, file_path)

class FileHandler(FileSystemEventHandler):
    """
    Custom file event handler to process files when they are created.
    """
    def on_created(self, event, file_path=None):
        """
        Handle the event when a file is created.

        Args:
            event (FileSystemEvent): The file system event.
            file_path (str, optional): The path of the file to process.
        """
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
        """
        Process a file by extracting text, analyzing it, and moving it based on tags.

        Args:
            file_path (str): The path of the file to process.
        """
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
            existing_tags = get_existing_tags(file_path)
            new_tags = analyze_text(text)
            summarized_text = summarize_text(" ".join(new_tags))
            logging.info(f"Summarized text: {summarized_text}")
            
            if set(new_tags) != set(existing_tags):
                logging.info(f"Tags changed for file: {file_path}")
                logging.info(f"Old tags: {existing_tags}")
                logging.info(f"New tags: {new_tags}")
                move_file_based_on_tags(file_path, [summarized_text], file_organization_schema)
            else:
                logging.info(f"Tags unchanged for file: {file_path}")
        else:
            logging.warning(f"Could not extract text from file: {file_path}")
