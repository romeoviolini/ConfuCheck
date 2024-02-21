from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QMessageBox, QScrollArea, QLabel, QProgressDialog, QApplication
from PyQt5.QtCore import Qt

from UI.window_text_interaction import DocumentWindow
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, MAX_CHARACTERS, ALLOWED_FORMATS
from UI.plain_text_edit import PlainTextOnlyEdit
from docx import Document

from text_analyzer import find_ambiguous_words


class MainWindow(QMainWindow):
    def __init__(self, nlp, ambiguousWords):
        super().__init__()
        self.nlp = nlp
        self.ambiguousWords = ambiguousWords
        self.textEdit = None
        self.uploadButton = None
        self.setWindowTitle("New Text")
        self.initUI()
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)  # Increase the window size
        self.centerWindow()
        #self.showFullScreen()

    def centerWindow(self):
        qr = self.frameGeometry()  # Get the QRect representing the geometry of the main window
        cp = QApplication.desktop().availableGeometry().center()  # Get the center point of the screen
        qr.moveCenter(cp)  # Set the center of the QRect to the center of the screen
        self.move(qr.topLeft())

    def initUI(self):
        # Create layout and widget as before
        layout = QVBoxLayout()
        contentWidget = QWidget()  # This widget contains everything you want to be scrollable
        contentWidget.setLayout(layout)

        # Scroll Area setup as before
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(contentWidget)
        self.setCentralWidget(scrollArea)

        # Text edit area setup as before
        self.textEdit = PlainTextOnlyEdit()
        self.textEdit.setPlaceholderText("Copy and paste your text here...")
        layout.addWidget(self.textEdit)

        # Button to confirm pasted text setup as before
        self.confirmButton = QPushButton("Confirm Text")
        self.confirmButton.setEnabled(False)
        layout.addWidget(self.confirmButton)

        # Label indicating an alternative action
        separatorLabel = QLabel("--- or ---", self)
        separatorLabel.setAlignment(Qt.AlignCenter)  # Center-align the text
        layout.addWidget(separatorLabel)

        # Button to upload a file setup as before
        self.uploadButton = QPushButton("Upload Text File")
        layout.addWidget(self.uploadButton)

        # Signals setup as before
        self.textEdit.textChanged.connect(self.onTextChanged)
        self.confirmButton.clicked.connect(self.onConfirmText)
        self.uploadButton.clicked.connect(self.onUploadFile)

    def onTextChanged(self):
        """Check if the pasted text exceeds the maximum number of characters allowed."""
        text = self.textEdit.toPlainText()
        if len(text) > MAX_CHARACTERS:
            QMessageBox.warning(self, "Error", f"The text exceeds the maximum limit of {MAX_CHARACTERS} characters.")
            self.textEdit.clear()  # Clear the text or set it to a previous valid state
        else:
            self.confirmButton.setEnabled(bool(text))

    def onConfirmText(self):
        """Handle text confirmation."""
        text = self.textEdit.toPlainText()
        print("Text confirmed:", text)

        # Setup the progress dialog
        progressDialog = QProgressDialog("Analyzing text, please wait...", None, 0, 0, self)
        progressDialog.setCancelButton(None)  # Disable the Cancel button
        progressDialog.setWindowModality(Qt.WindowModal)
        progressDialog.setWindowTitle("Processing")
        progressDialog.show()
        QApplication.processEvents()

        results = find_ambiguous_words(text, self.ambiguousWords, self.nlp)

        progressDialog.close()

        # Here, proceed with processing the confirmed text
        self.documentWindow = DocumentWindow(text, results, self.ambiguousWords)
        self.documentWindow.previousWindow = self
        self.documentWindow.show()
        self.textEdit.clear()
        self.close()

    def onUploadFile(self):
        """Open a file dialog to select a file, check if its format is allowed, and read text accordingly."""
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if filename:
            file_extension = filename.split('.')[-1].lower()
            if not file_extension or f".{file_extension}" not in ALLOWED_FORMATS:
                QMessageBox.warning(self, "Error",
                                    f"The file format is not valid. Allowed formats: {', '.join(ALLOWED_FORMATS)}")
            else:
                if file_extension == "docx":
                    # Use python-docx to extract text from .docx files
                    try:
                        doc = Document(filename)
                        self.currentText = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                    except Exception as e:
                        QMessageBox.warning(self, "Error", "Failed to read .docx file.")
                        print(e)
                        return
                else:
                    # Handle other file types as before
                    try:
                        with open(filename, 'r') as file:
                            self.currentText = file.read()
                    except UnicodeDecodeError as e:
                        QMessageBox.warning(self, "Error",
                                            "Failed to decode the file. It might not be a plain text file.")
                        print(e)
                        return

                if len(self.currentText) > MAX_CHARACTERS:
                    QMessageBox.warning(self, "Error",
                                        f"The file's text exceeds the maximum limit of {MAX_CHARACTERS} characters.")
                    self.currentText = ""  # Clear the text due to error
                else:
                    self.textEdit.setText(self.currentText)  # Display the text
                    print("File uploaded and text saved for analysis.")
                    self.onConfirmText()