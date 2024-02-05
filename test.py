from data_model import AmbiguousWord, load_ambiguous_words_from_json

# Path to the JSON file (adjust the path according to your directory structure)
json_file_path = 'ambiguous_words.json'

# Read the JSON file and convert it into a list of AmbiguousWord objects
ambiguous_words = load_ambiguous_words_from_json(json_file_path)

# Print the list to verify
for word in ambiguous_words:
    print(word)
