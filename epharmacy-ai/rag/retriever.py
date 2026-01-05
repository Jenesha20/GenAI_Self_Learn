def retrieve_documents(vectordb, query, k=4):
    results = vectordb.similarity_search_with_score(query, k=k)

    formatted = []
    for doc, distance in results:
        similarity = max(0.0, min(1.0, 1 / (1 + distance)))
        formatted.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": round(similarity, 3)
        })

    return formatted
