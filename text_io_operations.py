"""
text_io_operations.py

This module manages text input and output operations, focusing on reading from and saving to text files.
It abstracts away the complexity of file I/O, enabling the application to handle text data seamlessly
without getting entangled in the specifics of the filesystem. Designed to support reusability and ease
of management, it plays a critical role in applications where efficient text data manipulation is crucial.
"""


def read_text_from_file(file_path: str) -> str:
    """
    Reads and returns the content of a text file.

    :param file_path: The path to the text file to be read.
    :return: The content of the file as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return ""
    except IOError:
        print(f"Error occurred while reading the file {file_path}.")
        return ""


def save_text_to_file(file_path: str, text: str) -> None:
    """
    Saves the given text into a text file specified by file_path.

    :param file_path: The path to the file where the text will be saved.
    :param text: The text to be saved.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except IOError:
        print(f"Error occurred while writing to the file {file_path}.")
