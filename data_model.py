import json
from typing import List

# This class represents an ambiguous word, which could have multiple meanings depending on the context.
# It is designed to be a part of a larger system that helps in identifying and resolving ambiguities in technical writing.
class AmbiguousWord:
    def __init__(self, Id: int, Word: str, Meaning: str, Type: int, Ambiguities: List[int]):
        self.Id = Id  # Unique identifier for the word
        self.Word = Word  # The ambiguous word itself
        self.Meaning = Meaning  # A possible meaning of the word
        self.Type = Type  # Type of the word (0 = noun, 1 = verb, 2 = other)
        self.Ambiguities = Ambiguities  # List of IDs of ambiguous words related to this one

    def __repr__(self):
        return f"AmbiguousWord(Id={self.Id}, Word='{self.Word}', Meaning='{self.Meaning}', Type={self.Type}, Ambiguities={self.Ambiguities})"

def load_ambiguous_words_from_json(file_path: str) -> List[AmbiguousWord]:
    """Load ambiguous words from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [AmbiguousWord(**word_data) for word_data in data]

def save_ambiguous_words_to_json(file_path: str, ambiguous_words: List[AmbiguousWord]):
    """Save ambiguous words to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json_data = [word.__dict__ for word in ambiguous_words]
        json.dump(json_data, file, indent=4)
