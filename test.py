from data_model import AmbiguousWord, load_ambiguous_words_from_json
from text_analyzer import find_ambiguous_words
import spacy

nlp = spacy.load("en_core_web_sm")

# Path to the JSON file (adjust the path according to your directory structure)
json_file_path = 'ambiguous_words.json'

# Read the JSON file and convert it into a list of AmbiguousWord objects
ambiguous_words = load_ambiguous_words_from_json(json_file_path)

# Print the list to verify
for word in ambiguous_words:
    print(word.Word)


text = "John had always been a gracious competitor, ready to accept any outcome of the match. He knew that winning and losing were both part of the game. 'I will accept whatever result comes my way,' he said confidently before the final round. However, there was one condition he could not accept: being unfairly judged. 'I welcome all challenges, except when fairness is compromised,' he stated. This exception was well-known among his peers, who respected him for his principles. In every competition, John followed this simple rule: to accept every challenge with open arms, except when the rules of the game were not respected. 'It's not just about winning; it's about playing the game right,' he would often say. While discussing strategies, his coach mentioned, 'You should focus on improving your strengths and acknowledge your weaknesses, except for letting them define you.' John nodded in agreement, understanding that his willingness to accept constructive criticism except when it was unfounded was key to his growth."

results = find_ambiguous_words(text, ambiguous_words, nlp)

for result in results:
    print(
        f"Parola trovata: {result[0]}\n Posizione: {result[1]}\nId parola ambigua di riferimento: {result[2]}")



