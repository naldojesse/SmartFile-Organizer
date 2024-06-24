import os
import time
import logging
from watchdog.observers import Observer
from scripts.file_handler import FileHandler, analyze_existing_files
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    path = os.getenv("DOWNLOADS_PATH")
    logging.info(f"Monitoring directory: {path}")
    
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    # Analyze existing files in the DOWNLOADS_PATH folder
    logging.info("Analyzing existing files in the directory...")
    analyze_existing_files(path, event_handler)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
