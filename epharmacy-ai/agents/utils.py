import re

def extract_keywords(query: str):
    """
    Extract meaningful keywords from query.
    Very simple but effective baseline.
    """
    words = re.findall(r"[a-zA-Z]{4,}", query.lower())
    stopwords = {"what", "used", "for", "with", "take", "does", "can"}
    return [w for w in words if w not in stopwords]
