# SmartFile Organizer

SmartFile Organizer is a Python-based tool that uses AI and machine learning to automatically tag and organize files based on their content. It monitors specified directories, extracts and analyzes file content, generates tags, and moves files to appropriate directories.

## Features
- Monitors specified directories for new files.
- Extracts text from various file formats (PDF, DOCX, TXT, CSV, HTML).
- Uses NLP to analyze and summarize text.
- Classifies files based on their content and tags.
- Automatically moves files to appropriate directories.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SmartFileOrganizer.git
   cd SmartFileOrganizer
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following variables:
   ```
   DOWNLOADS_PATH=/path/to/downloads
   WORK_PATH=/path/to/work
   PERSONAL_PATH=/path/to/personal
   FINANCE_PATH=/path/to/finance
   PHOTOS_PATH=/path/to/photos
   SCREENSHOTS_PATH=/path/to/screenshots
   MOVIES_PATH=/path/to/movies
   TUTORIALS_PATH=/path/to/tutorials
   MISC_PATH=/path/to/misc
   ```

5. Train the classifier:
   ```bash
   python classifier/train_classifier.py
   ```

6. Run the application:
   ```bash
   python main.py
   ```

## Usage

- The application will monitor the specified directory for new files.
- When a new file is detected, it will extract the text, analyze it, and move the file to the appropriate directory based on its content.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
