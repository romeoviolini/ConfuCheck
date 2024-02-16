from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QApplication)
from PyQt5.QtCore import Qt
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, formatTextAsHTML


class DocumentWindow(QWidget):
    def __init__(self, text, ambiguous_words_results, parent=None, previousWindow=None):
        super().__init__(parent)
        self.sourceText = text
        self.ambiguousWordsResults = ambiguous_words_results
        self.previousWindow = previousWindow
        self.setWindowTitle("Document View")
        self.initUI()
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)  # Optionally resize the window
        self.showFullScreen()  # Display the window in fullscreen mode

    def initUI(self):
        text = self.highlight_words_in_html(self.sourceText, self.ambiguousWordsResults)
        text = formatTextAsHTML(text)

        mainLayout = QVBoxLayout()

        # Navigation Panel
        navigationPanel = QHBoxLayout()
        backButton = QPushButton("Back")
        navigationPanel.addWidget(backButton)
        navigationPanel.addStretch()
        backButton.clicked.connect(self.goBack)

        mainLayout.addLayout(navigationPanel)

        # Content Area
        contentArea = QHBoxLayout()

        # Document Visualization
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(text)

        # Side Panel
        sidePanel = QVBoxLayout()
        optionLabel = QLabel("Options will be here")
        sidePanel.addWidget(optionLabel)

        # Adding widgets to the content area with stretch factors
        contentArea.addWidget(self.textEdit, 2)  # Document takes 2/3 of the space
        contentArea.addLayout(sidePanel, 1)  # Side panel takes 1/3 of the space

        mainLayout.addLayout(contentArea)

        # Bottom navigation panel
        bottomNavPanel = QHBoxLayout()

        # Back arrow button
        backButton = QPushButton("Previous Word")
        backButton.clicked.connect(self.onBackClicked)  # Implement onBackClicked method

        # Progress label
        self.progressLabel = QLabel("0/0")  # Update this dynamically based on actual progress
        self.progressLabel.setAlignment(Qt.AlignCenter)

        # Next arrow button
        nextButton = QPushButton("Next Word")
        nextButton.clicked.connect(self.onNextClicked)  # Implement onNextClicked method

        # Add widgets to the bottom navigation panel
        bottomNavPanel.addWidget(backButton)
        bottomNavPanel.addStretch()  # This adds a stretchable space, centering the label
        bottomNavPanel.addWidget(self.progressLabel)
        bottomNavPanel.addStretch()  # This ensures the label stays centered
        bottomNavPanel.addWidget(nextButton)

        # Add the bottom navigation panel to the main layout
        mainLayout.addLayout(bottomNavPanel)

        self.setLayout(mainLayout)

    def goBack(self):
        # Close the current window and show the previous one if it exists
        if self.previousWindow:
            self.previousWindow.show()
        self.close()

    def onBackClicked(self):
        # Placeholder for back button functionality
        print("Back button clicked")

    def onNextClicked(self):
        # Placeholder for next button functionality
        print("Next button clicked")

    # Example function to highlight words in HTML
    def highlight_words_in_html(self, text, ambiguous_words_results):
        highlighted_text = text
        offset = 0
        for word, position, _ in ambiguous_words_results:
            start_tag = '<span style="background-color: yellow;">' if ambiguous_words_results.index(
                (word, position, _)) != 0 else '<span style="background-color: blue;">'
            end_tag = '</span>'
            highlighted_text = highlighted_text[:position + offset] + start_tag + word + end_tag + highlighted_text[
                                                                                                   position + offset + len(
                                                                                                       word):]
            offset += len(start_tag) + len(end_tag)
        return highlighted_text
