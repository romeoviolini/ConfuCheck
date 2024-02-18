from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QApplication,
                             QTreeWidget, QTreeWidgetItem, QScrollArea, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from data_model import AmbiguousWord, find_ambiguous_word_by_id
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, formatTextAsHTML, SELECTED_COLOR, UNSELECTED_COLOR, BACKGROUND_COLOR
from PyQt5.QtWebEngineWidgets import QWebEngineView
from typing import List

from text_replacer import replace_word_and_calculate_offset


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
        # self.showFullScreen()  # Display the window in fullscreen mode

    def initUI(self):
        text = self.highlight_words_in_html(self.sourceText, self.ambiguousWordsResults)
        text = formatTextAsHTML(text)

        mainLayout = QVBoxLayout()

        # Navigation Panel
        navigationPanel = QHBoxLayout()
        newTextButton = QPushButton("New Text")
        copyTextButton = QPushButton("Copy Text")  # New button for copying text
        exportTextButton = QPushButton("Export Text")
        navigationPanel.addWidget(newTextButton)
        navigationPanel.addWidget(copyTextButton)  # Add the Copy Text button
        navigationPanel.addWidget(exportTextButton)

        navigationPanel.addStretch()
        newTextButton.clicked.connect(self.newText)
        copyTextButton.clicked.connect(self.copyText)  # Connect to copyText slot
        exportTextButton.clicked.connect(self.exportText)

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

        if self.ambiguousWordsResults and len(self.ambiguousWordsResults) > 0:
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
        self.progressLabel = QLabel(f"confused words checked: 0/{len(self.ambiguousWordsResults)}")  # Update this dynamically based on actual progress
        self.progressLabel.setAlignment(Qt.AlignCenter)

        # Next arrow button
        nextButton = QPushButton("Next Word")
        nextButton.clicked.connect(self.onNextClicked)  # Implement onNextClicked method

        if not self.ambiguousWordsResults or len(self.ambiguousWordsResults) == 0:
            backButton.setEnabled(False)
            nextButton.setEnabled(False)
            optionLabel = QLabel("The text looks clean.")
            self.sidePanel.addWidget(optionLabel)

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

    def newText(self):
        # Close the current window and show the previous one if it exists
        if self.previousWindow:
            self.previousWindow.show()
        self.close()

    def copyText(self):
        # Placeholder for the copy text functionality
        text = self.prepareSourceTextForExport()
        # You might want to use QApplication.clipboard().setText(self.sourceText)
        QApplication.clipboard().setText(text)
        print("Text copied to clipboard")
        QMessageBox.information(self, "Text Copied",
                                f"The text has been copied to the clipboard.")


    def exportText(self):
        # Placeholder for the export text functionality
        text = self.prepareSourceTextForExport()
        # This might involve saving self.sourceText to a file
        # Open a file dialog to let the user choose the file name and location to save
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Export Text", "textChecked.txt",
                                                  "Text Files (*.txt)", options=options)

        if fileName:
            # Ensure the fileName has a .txt extension if not provided
            if not fileName.endswith('.txt'):
                fileName += '.txt'

            # Write self.sourceText to the chosen file
            try:
                with open(fileName, "w", encoding="utf-8") as file:
                    file.write(text)
                QMessageBox.information(self, "Export Successful",
                                        f"File has been successfully exported to:\n{fileName}")
            except Exception as e:
                QMessageBox.warning(self, "Export Failed", f"Failed to export file:\n{e}")

    def onBackClicked(self):
        # Placeholder for back button functionality
        print("Back button clicked")
        self.selectNextAmbigousWordByIndex(self.currentIndex - 1)


    def onNextClicked(self):
        # Placeholder for next button functionality
        print("Next button clicked")
        self.selectNextAmbigousWordByIndex(self.currentIndex + 1)

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
        self.populateSidePanel()

    def populateSidePanel(self):

        self.treeItems.clear()
        self.clearLayout(self.sidePanel)

        currentAmbiguousWordId = self.ambiguousWordsResults[self.currentIndex][2]
        currentAmbiguousWord = find_ambiguous_word_by_id(self.ambiguousWords, currentAmbiguousWordId)

        self.addOptionToSidePanel(currentAmbiguousWord, 0)

        ambiguityCount = 1
        for ambiguity in currentAmbiguousWord.find_related_ambiguities(self.ambiguousWords):
            self.addOptionToSidePanel(ambiguity, ambiguityCount)
            ambiguityCount += 1





    def addOptionToSidePanel(self, ambiguousWord: AmbiguousWord, index):
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
            i = 0
            for variant in ambiguousWord.Variants:
                option = QTreeWidgetItem([variant])
                optionsTree.addTopLevelItem(option)
                self.treeItems.append((option,index,i))
                optionsTree.setMinimumHeight(
                    optionsTree.sizeHintForRow(0) * len(ambiguousWord.Variants) + 10)
                i += 1
        else:
            option = QTreeWidgetItem([ambiguousWord.Word])
            optionsTree.addTopLevelItem(option)
            self.treeItems.append((option,index,0))
            optionsTree.setMinimumHeight(
                optionsTree.sizeHintForRow(0) + 10)

        optionsTree.itemClicked.connect(self.onItemClicked)
        optionsTree.expandAll()
        self.sidePanel.addWidget(optionsTree)

    def onItemClicked(self, item, column):
        # Deselect all items except the one clicked
        for treeItem in self.treeItems:
            if treeItem[0] != item:
                # Deselect item. There's no direct deselect method, but you can simulate it by:
                treeItem[0].setSelected(False)
            else:
                # Ensure the clicked item is selected
                treeItem[0].setSelected(True)
                print(f"{treeItem[0].text(column)} option: {treeItem[1]} position: {treeItem[2]}")
                # results.append((match.group(), start, word.Id, False, -1, -1))
                resultWord = self.ambiguousWordsResults[self.currentIndex]
                if resultWord[3] == False:
                    count_true = len([item for item in self.ambiguousWordsResults if item[3] == True])
                    print("Time to count")
                    print(count_true)
                    self.progressLabel.setText(f"confused words checked: {count_true+1}/{len(self.ambiguousWordsResults)}")
                self.ambiguousWordsResults[self.currentIndex] = (resultWord[0], resultWord[1], resultWord[2], True, treeItem[1], treeItem[2])
                self.updateCurrentWordOnHTMLText(treeItem[0].text(column))

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def updateCurrentWordOnHTMLText(self, newText):

        position = self.ambiguousWordsResults[self.currentIndex][1]
        sourceText = self.ambiguousWordsResults[self.currentIndex][0]
        newText = self.adapt_case(sourceText, newText)

        script = f"""
                var element = document.getElementById('{position}');
                if (element) {{
                    element.innerText = '{newText}';
                    element.style.backgroundColor = '#e0ffcd';
                }}
                """
        self.webView.page().runJavaScript(script)

    def adapt_case(self, source, target):
        # Uppercase
        if source.isupper():
            return target.upper()
        # Lowercase
        elif source.islower():
            return target.lower()
        # Capitalized
        elif source.istitle():
            return target.capitalize()
        # Handle more specific mixed case scenarios here if needed
        else:
            return target

    def prepareSourceTextForExport(self):

        offset_accumulator = 0
        text = self.sourceText

        for result in self.ambiguousWordsResults:

            print(result)

            if result[3] != False:
                ambiguousWord = find_ambiguous_word_by_id(self.ambiguousWords, result[2])
                correctWord = ambiguousWord.Word
                if result[4] > 0:
                    ambiguities = ambiguousWord.find_related_ambiguities(self.ambiguousWords)
                    print(len(ambiguities))
                    currentAmbiguity = ambiguities[result[4]-1]

                    if not currentAmbiguity.Variants or len(currentAmbiguity.Variants) == 0:
                        correctWord = currentAmbiguity.Word
                    else:
                        correctWord = currentAmbiguity.Variants[result[5]]
                else:
                    if not ambiguousWord.Variants or len(ambiguousWord.Variants) == 0:
                        correctWord = ambiguousWord.Word
                    else:
                        correctWord = ambiguousWord.Variants[result[5]]

                correctWord = self.adapt_case(result[0], correctWord)

                # Update the current word's position with the accumulated offset so far
                current_position = result[1] + offset_accumulator

                # Replace the word and calculate the offset
                text, offset = replace_word_and_calculate_offset(text, current_position, result[0], correctWord)
                # Update the offset accumulator
                offset_accumulator += offset

        return text