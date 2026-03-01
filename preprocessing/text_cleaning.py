import re


def clean_text(text: str):
    """
    Clean resume or job description text.
    """

    # Remove extra spaces and line breaks
    text = re.sub(r"\s+", " ", text)

    # Remove special characters (keep words & numbers)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Convert to lowercase
    text = text.lower()

    return text.strip()