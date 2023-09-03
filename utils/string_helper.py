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
