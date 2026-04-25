import re

def clean_text(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)  # remove extra newlines
    text = re.sub(r'\s+', ' ', text)        # normalize spaces
    return text.strip()