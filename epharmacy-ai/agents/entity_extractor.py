import re

def extract_entities(query: str):
    """
    Very lightweight entity extractor.
    Works generically for drug names.
    """
    words = re.findall(r"[A-Za-z]{4,}", query.lower())
    return list(set(words))
