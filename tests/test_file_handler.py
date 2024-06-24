import pytest
import os
from scripts.file_handler import FileHandler, create_directory_if_not_exists, move_file_based_on_tags
from scripts.utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, extract_text_from_csv, extract_text_from_html

@pytest.fixture
def file_handler():
    return FileHandler()

def test_create_directory_if_not_exists(tmp_path):
    test_dir = tmp_path / "test_dir"
    create_directory_if_not_exists(str(test_dir))
    assert test_dir.exists()

def test_move_file_based_on_tags(tmp_path):
    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    
    test_file = source_dir / "test.txt"
    test_file.write_text("Test content")
    
    schema = {"documents": {"work": str(dest_dir)}}
    tags = ["work"]
    
    new_file_path = move_file_based_on_tags(str(test_file), tags, schema)
    
    assert not test_file.exists()
    assert new_file_path is not None
    assert os.path.exists(new_file_path)
    assert os.path.basename(new_file_path) == "test.txt"

def test_extract_text_from_txt(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, world!")
    
    extracted_text = extract_text_from_txt(str(test_file))
    assert extracted_text == "Hello, world!"

@pytest.mark.parametrize("file_type,extract_function", [
    ("pdf", extract_text_from_pdf),
    ("docx", extract_text_from_docx),
    ("csv", extract_text_from_csv),
    ("html", extract_text_from_html),
])
def test_extract_text_raises_error_for_missing_file(file_type, extract_function):
    with pytest.raises(FileNotFoundError):
        extract_function(f"non_existent_file.{file_type}")

def test_file_handler_process_file(file_handler, tmp_path, mocker):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Test content")
    
    mock_extract = mocker.patch('scripts.file_handler.extract_text_from_txt', return_value="Test content")
    mock_analyze = mocker.patch('scripts.file_handler.analyze_text', return_value=["work"])
    mock_summarize = mocker.patch('scripts.file_handler.summarize_text', return_value="Test summary")
    mock_move = mocker.patch('scripts.file_handler.move_file_based_on_tags')
    
    file_handler.process_file(str(test_file))
    
    mock_extract.assert_called_once_with(str(test_file))
    mock_analyze.assert_called_once_with("Test content")
    mock_summarize.assert_called_once_with(" ".join(["work"]))
    mock_move.assert_called_once()
