from data_model import AmbiguousWord, TypeReadable
from typing import List
import re

"""
text_analyzer.py

This module handles analysis of text for ambiguous words using regex and spaCy NLP. 
It identifies words with multiple meanings and categorizes them based on context and part of speech. 
This aids in enhancing clarity in technical documents by resolving linguistic ambiguities.
"""


def find_ambiguous_words(text, ambiguous_words: List[AmbiguousWord], nlp):
    """
    Identifies and returns a list of ambiguous words found in the provided text, based on a list of AmbiguousWord instances.
    It distinguishes between different types of words (e.g., nouns, verbs, others) using both regular expressions and spaCy NLP analysis,
    to ensure accurate matching according to the word type and context.

    :param text: The text in which to find ambiguous words.
    :param ambiguous_words: A list of AmbiguousWord instances to search for in the text.
    :param nlp: An initialized spaCy language model for natural language processing.
    :return: A sorted list of tuples, each containing the matched word, its start position in the text, and its ID from the ambiguous words list.

    The function first searches for 'other' types of words using regular expressions for exact matches.
    Then, it uses spaCy's tokenization and part-of-speech tagging to identify nouns and verbs accurately.
    Results are sorted by the start position of each found word to maintain their order in the text.
    """

    results = []
    covered_positions = set()

    # Search for 'Other' type words using regular expressions
    for word in ambiguous_words:
        if word.Type == TypeReadable.Other.value:
            pattern = re.compile(r'\b' + re.escape(word.Word) + r'\b', re.IGNORECASE)
            matches = pattern.finditer(text)
            for match in matches:
                start = match.start()
                if start not in covered_positions:
                    results.append((match.group(), start, word.Id, False, -1, -1))
                    covered_positions.update(range(start, match.end()))

    # Use spaCy NLP to find and categorize nouns and verbs
    doc = nlp(text)
    for token in doc:
        start = token.idx
        end = start + len(token.text)
        if start in covered_positions:
            continue  # Skip if this start position is already covered

        for word in ambiguous_words:
            if word.Type != TypeReadable.Other.value and token.lemma_.lower() == word.Word.lower():
                if (word.Type == TypeReadable.Noun.value and token.pos_ == "NOUN") or \
                        (word.Type == TypeReadable.Verb.value and token.pos_ == "VERB"):
                    results.append((token.text, start, word.Id, False, -1, -1))
                    covered_positions.update(range(start, end))

    results.sort(key=lambda x: x[1])
    return results
