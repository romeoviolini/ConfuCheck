import json
from typing import List
from enum import Enum

"""
data_model.py

This module defines the core data structures and operations for the ambiguous words identification system. This includes:
- An enumeration to categorize word types in a human-readable format.
- The AmbiguousWord class to represent words with multiple meanings, including their context, possible meanings, and relationships with other ambiguous words.
- Functions to load these ambiguous words from and save them to JSON files, facilitating persistence and data exchange.

These components are essential for identifying, categorizing, and resolving ambiguities in technical writing, making them foundational to the system's functionality.
"""


# Define an Enum to make the type more human-readable
class TypeReadable(Enum):
    Noun = 0
    Verb = 1
    Other = 2


class AmbiguousWord:
    """
    This class represents an ambiguous word, which could have multiple meanings depending on the context.
    It is designed to be a part of a larger system that helps in identifying and resolving ambiguities in technical writing.
    """

    def __init__(self, Id: int, Word: str, Meaning: str, Type: int, Ambiguities: List[int], Variants: List[str] = None):
        self.Id = Id  # Unique identifier for the word
        self.Word = Word  # The ambiguous word itself
        self.Meaning = Meaning  # A possible meaning of the word
        self.Type = Type  # Type of the word (0 = noun, 1 = verb, 2 = other)
        self.Ambiguities = Ambiguities  # List of IDs of ambiguous words related to this one
        self.Variants = Variants if Variants is not None else []  # List of possible variants of the ambiguous word
        self._related_words_cache = None  # Initialize the cache as None

    def __repr__(self):
        return (f"AmbiguousWord(Id={self.Id}, Word='{self.Word}', Meaning='{self.Meaning}', Type={self.Type}, "
                f"Ambiguities={self.Ambiguities})", f"Variants={self.Variants})")

    def find_related_ambiguities(self, words: List['AmbiguousWord']) -> List['AmbiguousWord']:
        """
        Finds and returns a list of AmbiguousWord instances that are related to this word,
        based on the IDs in this word's Ambiguities property. The result is cached to avoid
        recomputation on subsequent calls.

        :param words: A list of AmbiguousWord instances to search through for related words.
        :return: A list of AmbiguousWord instances that are related to this instance.
        """
        # Check if we've already computed this before
        if self._related_words_cache is not None:
            return self._related_words_cache

        # Compute the related words and cache the result
        self._related_words_cache = [word for word in words if word.Id in self.Ambiguities]

        return self._related_words_cache


def load_ambiguous_words_from_json(file_path: str) -> List[AmbiguousWord]:
    # Load ambiguous words from a JSON file.
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [AmbiguousWord(**word_data) for word_data in data]


def save_ambiguous_words_to_json(file_path: str, ambiguous_words: List[AmbiguousWord]):
    # Save ambiguous words to a JSON file.
    with open(file_path, 'w', encoding='utf-8') as file:
        json_data = [word.__dict__ for word in ambiguous_words]
        json.dump(json_data, file, indent=4)

def find_ambiguous_word_by_id(words, id):
    return next((word for word in words if word.Id == id), None)