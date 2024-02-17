from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QApplication)
from PyQt5.QtCore import Qt
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, formatTextAsHTML, SELECTED_COLOR, UNSELECTED_COLOR, BACKGROUND_COLOR
from PyQt5.QtWebEngineWidgets import QWebEngineView

class DocumentWindow(QWidget):
    def __init__(self, text, ambiguous_words_results, parent=None, previousWindow=None):
        super().__init__(parent)
        self.currentIndex = 0
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
        self.webView = QWebEngineView()  # Use QWebEngineView instead of QTextEdit
        self.webView.setHtml(text)  # Load the HTML content

        # Side Panel
        sidePanel = QVBoxLayout()
        optionLabel = QLabel("Options will be here")
        sidePanel.addWidget(optionLabel)

        # Adding widgets to the content area with stretch factors
        contentArea.addWidget(self.webView, 2)  # Document takes 2/3 of the space
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

        self.webView.loadFinished.connect(self.onLoadFinished)

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
        self.selectNextAmbigousWordByIndex(self.currentIndex+1)

    # Example function to highlight words in HTML
    def highlight_words_in_html(self, text, ambiguous_words_results):
        highlighted_text = text
        offset = 0
        for index, (word, position, _) in enumerate(ambiguous_words_results):
            # Use underline for styling, and differentiate the first selected word with a different color
            #color = "#008000" good for corrected words
            color = SELECTED_COLOR if index == 0 else UNSELECTED_COLOR  # Change 'blue' to any color for the first word, and 'black' for others
            start_tag = (f'<span id={position} style="text-decoration: underline; color: {color}; background-color: '
                         f'{BACKGROUND_COLOR};">')
            end_tag = '</span>'
            highlighted_text = (highlighted_text[:position + offset] + start_tag + word + end_tag +
                                highlighted_text[position + offset + len(word):])
            offset += len(start_tag) + len(end_tag)
        return highlighted_text

    def getWordPositionByIndex(self, index):
        return self.ambiguousWordsResults[index][1]

    def change_word_color(self, span_id, color, bold):
        fontWeight = "bold" if bold else "normal"
        script = f"""
        var element = document.getElementById('{span_id}');
        if (element) {{
            element.style.color = '{color}';
            element.style.fontWeight = '{fontWeight}';
        }}
        """
        self.webView.page().runJavaScript(script)

    def scroll_to_word_on_top(self, span_id):
        script = f"""
        var element = document.getElementById('{span_id}');
        if (element) {{
            element.scrollIntoView();
        }}
        """
        self.webView.page().runJavaScript(script)

    def scroll_to_word(self, span_id):
        script = f"""
        var element = document.getElementById('{span_id}');
        if (element) {{
            var bounding = element.getBoundingClientRect();
            if (
                bounding.top >= 0 && bounding.left >= 0 &&
                bounding.right <= (window.innerWidth || document.documentElement.clientWidth) &&
                bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight)
            ) {{
                // The element is in the view, don't scroll
            }} else {{
                // The element is not in the view, scroll to the element
                element.scrollIntoView({{behavior: "smooth", block: "nearest", inline: "start"}});
            }}
        }}
        """
        self.webView.page().runJavaScript(script)

    def onLoadFinished(self, success):
        if success:
            if len(self.ambiguousWordsResults) > 0:
                firstAmbiguousPosition = self.getWordPositionByIndex(self.currentIndex)
                print(f"scroll to {firstAmbiguousPosition}")
                self.scroll_to_word_on_top(firstAmbiguousPosition)
                self.change_word_color(firstAmbiguousPosition, SELECTED_COLOR, True)

    def selectNextAmbigousWordByIndex(self, nextIndex):
        position = self.ambiguousWordsResults[self.currentIndex][1]
        self.change_word_color(position, UNSELECTED_COLOR, False)
        self.currentIndex = nextIndex
        self.currentIndex = self.currentIndex % len(self.ambiguousWordsResults)
        position = self.ambiguousWordsResults[self.currentIndex][1]
        self.change_word_color(position, SELECTED_COLOR, True)
        self.scroll_to_word(position)

    def selectNextAmbiguousWordByPosition(self, position):
        for index, (_, start, _) in enumerate(self.ambiguousWordsResults):
            if start == position:
                return index
        return None
