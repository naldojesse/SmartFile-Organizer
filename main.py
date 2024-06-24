import os
import time
import logging
from watchdog.observers import Observer
from scripts.file_handler import FileHandler, analyze_existing_files
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    # Get the path to monitor from environment variables
    path = os.getenv("DOWNLOADS_PATH")
    logging.info(f"Monitoring directory: {path}")
    
    # Initialize the file event handler and observer
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    # Analyze existing files in the DOWNLOADS_PATH folder
    logging.info("Analyzing existing files in the directory...")
    analyze_existing_files(path, event_handler)

    try:
        # Keep the script running to monitor the directory
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer if the script is interrupted
        observer.stop()
    observer.join()
