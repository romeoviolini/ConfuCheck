MAX_CHARACTERS = 10000000  # Example limit for maximum characters allowed
ALLOWED_FORMATS = ['.docx','.txt','.doc',]  # List of allowed file formats, extendable for future formats
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FONT_SIZE = 14
SELECTED_COLOR = "#f96d00"
UNSELECTED_COLOR = "#000000"
BACKGROUND_COLOR = "#faebcd"
APP_NAME = "ConfuCheck"
APP_VERSION = "1.0.0"

def formatTextAsHTML(text):
    #font_stack = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Ubuntu, 'Helvetica Neue', sans-serif"
    font_stack = "'Times New Roman', Times, serif"
    text = text.replace('\n', '<br>')
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: {font_stack};
            }}
        </style>
    </head>
    <body>
        <p>{text}</p>
    </body>
    </html>
    """