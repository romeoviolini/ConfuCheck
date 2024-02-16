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

# Print the list to verify
for word in ambiguous_words:
    print(word.Word)

# Sample text
text = "John had always been a gracious competitor, ready to accept any outcome of the match. He knew that winning and losing were both part of the game. 'I will accept whatever result comes my way,' he said confidently before the final round. However, there was one condition he could not accept: being unfairly judged. 'I welcome all challenges, except when fairness is compromised,' he stated. This exception was well-known among his peers, who respected him for his principles. In every competition, John followed this simple rule: to accept every challenge with open arms, except when the rules of the game were not respected. 'It's not just about winning; it's about playing the game right,' he would often say. While discussing strategies, his coach mentioned, 'You should focus on improving your strengths and acknowledge your weaknesses, except for letting them define you.' John nodded in agreement, understanding that his willingness to accept constructive criticism except when it was unfounded was key to his growth."

# Find all the ambiguous words in the text
results = find_ambiguous_words(text, ambiguous_words, nlp)

# Print the result
for result in results:
    print(
        f"Word found: {result[0]}\nPosition: {result[1]}\nAmbiguous word Id: {result[2]}")

# For each word found, replace it with the word TEST
offset_accumulator = 0
for result in results:
        word, position, word_id = result

        # Update the current word's position with the accumulated offset so far
        current_position = position + offset_accumulator

        # Replace the word and calculate the offset
        text, offset = replace_word_and_calculate_offset(text, current_position, word, "TEST")

        # Update the offset accumulator
        offset_accumulator += offset

print(text)

# test the ambiguities of the word Accept
ambiguities = ambiguous_words[0].find_related_ambiguities(ambiguous_words)

# should print Except
print(ambiguities[0].Word)

app = QApplication(sys.argv)
window = MainWindow(nlp, ambiguous_words)
window.show()
sys.exit(app.exec_())