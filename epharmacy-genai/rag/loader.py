from typing import List

def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_sources() -> List[str]:
    from pathlib import Path
    sources = []
    data_dir = Path("data")

    for file in ["faq.txt", "drug_interactions.txt"]:
        path = data_dir / file
        if path.exists():
            sources.append(load_txt(str(path)))

    return sources
