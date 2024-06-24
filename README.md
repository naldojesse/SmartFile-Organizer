# SmartFile Organizer

SmartFile Organizer is a Python-based tool that uses AI and machine learning to automatically tag and organize files based on their content. It monitors specified directories, extracts and analyzes file content, generates tags, and moves files to appropriate directories.

## Features
- **Directory Monitoring**: Monitors specified directories for new files.
- **Text Extraction**: Extracts text from various file formats (PDF, DOCX, TXT, CSV, HTML).
- **NLP Analysis**: Uses Natural Language Processing (NLP) to analyze and summarize text.
- **File Classification**: Classifies files based on their content and tags.
- **Automated Organization**: Automatically moves files to appropriate directories based on their classification.

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/SmartFileOrganizer.git
   cd SmartFileOrganizer
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
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

5. **Train the classifier**:
   ```bash
   python classifier/train_classifier.py
   ```

6. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

- **Monitoring**: The application will monitor the specified directory for new files.
- **Processing**: When a new file is detected, it will extract the text, analyze it, and move the file to the appropriate directory based on its content.

### Example
1. Place a new file (e.g., `report.pdf`) in the monitored directory.
2. The application will detect the new file, extract its content, analyze it, and move it to the appropriate directory (e.g., `WORK_PATH`).

## Directory Structure

```
SmartFileOrganizer/
├── classifier/
│   └── train_classifier.py
├── scripts/
│   ├── file_handler.py
│   └── utils.py
├── test_files/
│   └── Documents/
│       └── Misc/
│           └── bookcollection.csv
├── .env
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the repository**: Click the "Fork" button at the top right of this repository.
2. **Clone your fork**: 
   ```bash
   git clone https://github.com/yourusername/SmartFileOrganizer.git
   cd SmartFileOrganizer
   ```
3. **Create a branch**: 
   ```bash
   git checkout -b feature-branch
   ```
4. **Make your changes**: Add your features or fix bugs.
5. **Commit your changes**: 
   ```bash
   git commit -m "Description of your changes"
   ```
6. **Push to your fork**: 
   ```bash
   git push origin feature-branch
   ```
7. **Create a Pull Request**: Go to the original repository and create a pull request from your fork.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to open an issue or contact the repository owner.

## Acknowledgements

- [spaCy](https://spacy.io/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [python-docx](https://python-docx.readthedocs.io/en/latest/)
- [pandas](https://pandas.pydata.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [scikit-learn](https://scikit-learn.org/stable/)
- [watchdog](https://pypi.org/project/watchdog/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Troubleshooting

If you encounter any issues, please check the following:

- Ensure all dependencies are installed correctly.
- Verify that the environment variables in the `.env` file are set correctly.
- Check the logs for any error messages.

## Future Enhancements

- Add support for more file formats.
- Improve the accuracy of the classifier.
- Add a web interface for easier management and monitoring.
