from data_model import AmbiguousWord, load_ambiguous_words_from_json
from text_analyzer import find_ambiguous_words
from text_replacer import replace_word_and_calculate_offset
import spacy
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
from UI.window_text_input import MainWindow

nlp = spacy.load("en_core_web_sm")

# Path to the JSON file (adjust the path according to your directory structure)
json_file_path = 'ambiguous_words.json'

# Read the JSON file and convert it into a list of AmbiguousWord objects
ambiguous_words = load_ambiguous_words_from_json(json_file_path)

app = QApplication(sys.argv)
window = MainWindow(nlp, ambiguous_words)
window.show()
sys.exit(app.exec_())