import re
from langchain_core.documents import Document

def chunk_documents(documents):
    chunks = []

    for doc in documents:
        text = doc.page_content

        sections = re.split(r"\n\n+", text)

        for section in sections:
            section = section.strip()
            if len(section) < 80:
                continue

            content_lower = section.lower()

            # ---- classify chunk type ----
            if "interaction" in content_lower or "+" in content_lower:
                chunk_type = "interaction"
            elif "dosage" in content_lower:
                chunk_type = "dosage"
            elif "indications" in content_lower or "used for" in content_lower:
                chunk_type = "drug_info"
            else:
                chunk_type = "general"

            # ---- extract drug name (best-effort) ----
            match = re.match(r"([A-Z][a-zA-Z]+)", section)
            drug = match.group(1).lower() if match else "unknown"

            chunks.append(
                Document(
                    page_content=section,
                    metadata={
                        "drug": drug,
                        "type": chunk_type
                    }
                )
            )

    return chunks
