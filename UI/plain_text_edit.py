import re
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QMimeData

class PlainTextOnlyEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def insertFromMimeData(self, source: QMimeData):
        """
        Inserts only plain text from the clipboard, ignoring any formatting,
        non-text content like images or links, and specifically filters out
        markdown image links.
        """
        if source.hasText():
            text = source.text()
            # Filter out markdown image links using a regular expression
            filtered_text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
            self.insertPlainText(filtered_text)
        else:
            # Call the base class implementation for mime types we don't handle
            super().insertFromMimeData(source)
