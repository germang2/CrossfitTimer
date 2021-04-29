class ColorPicker(object):
    DARK_BLUE = '#12232E'
    LIGHTER_BLUE = '#007CC7'
    LIGHTEST_BLUE = '#4DA8DA'
    SHADOW_OF_DARK_BLUE = '#203647'
    SHADOW_OF_LIGHT_BLUE = '#EEFBFB'
    TRANSPARENT_BACKGROUND = 'background-color: rgba(0,0,0,0%)'

    FONT_COLOR = f'color: {SHADOW_OF_LIGHT_BLUE}'
    LEFT_GRADIENT_COLOR = f'background-color:{DARK_BLUE}; {FONT_COLOR}'
    RIGHT_GRADIENT_COLOR = SHADOW_OF_DARK_BLUE
    BACKGROUND_GRADIENT_COLOR = f"""background-color:
        qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {DARK_BLUE}, 
        stop:1 {SHADOW_OF_DARK_BLUE});"""
    BUTTON_COLOR = f'background-color:{LIGHTER_BLUE};\ncolor:{SHADOW_OF_LIGHT_BLUE};'
    BUTTON_TABLE_COLOR = f'background-color:{LIGHTEST_BLUE};\ncolor:{SHADOW_OF_LIGHT_BLUE};'
    TABLE_HORIZONTAL_HEADER_COLOR = """QHeaderView::section{background:#203647;color: #EEFBFB;}"""
    TABLE_VERTICAL_HEADER_COLOR = """QHeaderView::section{background:#203647;color: #EEFBFB;}"""
    LABEL_COLOR = f'{TRANSPARENT_BACKGROUND}; {FONT_COLOR}'
    ERROR_COLOR = f'{TRANSPARENT_BACKGROUND}; color: #CC527A;'
