MAX_CHARACTERS = 10000000  # Example limit for maximum characters allowed
ALLOWED_FORMATS = ['.docx','.txt','.doc',]  # List of allowed file formats, extendable for future formats
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FONT_SIZE = 14


def formatTextAsHTML(text):
    font_stack = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Ubuntu, 'Helvetica Neue', sans-serif"
    text = text.replace('\n', '<br>')
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: {font_stack}; margin: 20px; font-size: {FONT_SIZE}px; }}
            p {{ text-indent: 20px; }}
        </style>
    </head>
    <body>
        <p>{text}</p>
    </body>
    </html>
    """