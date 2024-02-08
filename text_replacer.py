"""
text_replacer.py

This module is responsible for replacing ambiguous words in a text with their selected alternatives. It not only performs the replacement but also calculates the offset resulting from the change in word length. This functionality is crucial for maintaining the correct positions of words in the text after a replacement, especially when processing multiple replacements in a single document. The module ensures that the integrity of the text structure is preserved while accommodating updates to ambiguous word instances.
"""

def replace_word_and_calculate_offset(text: str, current_word_position: int, current_word: str, new_word: str) -> (str, int):
    """
    Replaces a specified word in the text with a new word and calculates the offset caused by the length difference.

    :param text: The original text in which the word replacement is to be made.
    :param current_word_position: The starting index of the word to be replaced in the text.
    :param current_word: The word in the text to be replaced.
    :param new_word: The new word that will replace the current word in the text.
    :return: A tuple containing the updated text and the offset resulting from the replacement.

    The function asserts that the specified current word matches the text at the given position to ensure accuracy before replacement. It then performs the replacement and calculates the offset, which is essential for adjusting subsequent word positions.
    """
    end_position = current_word_position + len(current_word)
    assert text[current_word_position:end_position] == current_word, "The current word does not match the specified position in the text."

    updated_text = text[:current_word_position] + new_word + text[end_position:]
    offset = len(new_word) - len(current_word)

    return updated_text, offset
