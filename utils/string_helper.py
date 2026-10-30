# -*- coding: utf-8 -*-
import unicodedata
import regex


def remove_inner_new_lines(value: str):
    """
    Fix a string and remove inner new lines
    :param value: str, value to fix. Ie, 'This is\n a\n text'
    :return: str, 'This is a text'
    """
    return value.replace("\n", " ") if value else ""


def get_edit_box_value(ed_box, return_none=False):
    """
    Returns a strip value of the edit box
    :param ed_box: PyQt5 edit box
    :param return_none: boolean: if True returns a None instead of empty string
    :return: string, with input value
    """

    try:
        value = ed_box.text()
        if value and type(value) == str:
            return value.strip()
        return None if return_none else ""
    except Exception as e:
        print(f"Error getting value of edit box, error detail: {e}")


def remove_special_chars(text):
    """
    Remove special characters from text
    :param text: Text to remove special characters from
    :return: str, 'This is a text'
    """
    return regex.sub(r'\p{P}', '', text)

def allow_only_unicode_chars(text):
    """
    Allow only Unicode letters (including Spanish characters like ñ, accented vowels, etc.),
    combining marks, numbers, punctuation, symbols and spaces.
    :param text: Text to filter
    :return: str or None, filtered text
    """
    if text is None:
        return None
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='replace')
    elif not isinstance(text, str):
        text = str(text)

    # Normalize to NFC to compose decomposed characters (e.g. n + ~ -> ñ, a + ´ -> á)
    text = unicodedata.normalize('NFC', text)
    # Allow letters (\p{L}), marks/accents (\p{M}), numbers (\p{N}), punctuation (\p{P}), symbols (\p{S}), and whitespace (\s)
    filtered_text = regex.sub(r'[^\p{L}\p{M}\p{N}\p{P}\p{S}\s]', '', text)
    return unicodedata.normalize('NFKD', filtered_text).encode('ascii', errors='ignore').decode('utf-8')
