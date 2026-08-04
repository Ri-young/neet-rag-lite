def format_citations(chunks):
    """
    Takes the retrieved chunks and formats them as clean citations.
    Every answer must show WHERE it came from.
    """
    citations = []
    seen = set() # avoid duplicate citations
    for i, chunk in enumerate(chunks):
        key = f"{chunk['source']}_{chunk['page_number']}"
        if key not in seen:
            seen.add(key)
            citations.append(
                f'[{len(citations)+1}] {chunk["source"]} │ Page {chunk["page_number"]} │ Relevance: {chunk["score"]}'
            )
    return citations
