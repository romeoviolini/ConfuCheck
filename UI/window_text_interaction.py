from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QApplication,
                             QTreeWidget, QTreeWidgetItem, QScrollArea)
from PyQt5.QtCore import Qt
from data_model import AmbiguousWord
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, formatTextAsHTML, SELECTED_COLOR, UNSELECTED_COLOR, BACKGROUND_COLOR
from PyQt5.QtWebEngineWidgets import QWebEngineView
from typing import List

class DocumentWindow(QWidget):
    def __init__(self, text, ambiguous_words_results, ambiguousWords: List[AmbiguousWord] , parent=None, previousWindow=None):
        super().__init__(parent)
        self.currentIndex = 0
        self.sourceText = text
        self.ambiguousWordsResults = ambiguous_words_results
        self.ambiguousWords = ambiguousWords
        self.previousWindow = previousWindow
        # List to keep track of all tree items
        self.treeItems = []
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

        # Side Panel setup with scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.sidePanel = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Example usage of dynamic side panel content population
        self.populateSidePanel()

        # Adding widgets to the content area with stretch factors
        contentArea.addWidget(self.webView, 2)
        contentArea.addWidget(self.scrollArea, 1)

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
        for index, (word, position, _,_,_,_) in enumerate(ambiguous_words_results):
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

    def populateSidePanel(self):

        self.treeItems.clear()

        currentAmbiguousWordId = self.ambiguousWordsResults[self.currentIndex][2]
        currentAmbiguousWord = self.ambiguousWords[currentAmbiguousWordId]

        self.addOptionToSidePanel(currentAmbiguousWord)

        for ambiguity in currentAmbiguousWord.find_related_ambiguities(self.ambiguousWords):
            self.addOptionToSidePanel(ambiguity)





    def addOptionToSidePanel(self, ambiguousWord: AmbiguousWord):
        titleLabel = QLabel(ambiguousWord.Word)
        titleLabel.setStyleSheet("font-weight: bold;")
        self.sidePanel.addWidget(titleLabel)

        descriptionLabel = QLabel(ambiguousWord.Meaning)
        self.sidePanel.addWidget(descriptionLabel)

        optionsTree = QTreeWidget()
        optionsTree.setHeaderHidden(True)
        optionsTree.setStyleSheet("""
                                        QTreeWidget::item {
                                            border: 1px solid #d9d9d9;
                                            border-radius: 5px;
                                            padding: 5px;
                                            margin-top: 2px;
                                        }
                                        QTreeWidget::item:selected {
                                            background-color: #f96d00;
                                            border-color: #faebcd;
                                        }
                                    """)
        if len(ambiguousWord.Variants) > 0:
            for variant in ambiguousWord.Variants:
                option = QTreeWidgetItem([variant])
                optionsTree.addTopLevelItem(option)
                self.treeItems.append(option)
                optionsTree.setMinimumHeight(
                    optionsTree.sizeHintForRow(0) * len(ambiguousWord.Variants) + 10)
        else:
            option = QTreeWidgetItem([ambiguousWord.Word])
            optionsTree.addTopLevelItem(option)
            self.treeItems.append(option)
            optionsTree.setMinimumHeight(
                optionsTree.sizeHintForRow(0) + 10)

        optionsTree.itemClicked.connect(self.onItemClicked)
        optionsTree.expandAll()
        self.sidePanel.addWidget(optionsTree)

    def onItemClicked(self, item, column):
        # Deselect all items except the one clicked
        for treeItem in self.treeItems:
            if treeItem != item:
                # Deselect item. There's no direct deselect method, but you can simulate it by:
                treeItem.setSelected(False)
            else:
                # Ensure the clicked item is selected
                treeItem.setSelected(True)
