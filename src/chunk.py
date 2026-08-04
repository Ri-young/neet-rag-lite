def chunk_pages(pages, chunk_size=500, overlap=100):
    """
    Takes the list of pages from ingest.py
    Returns a list of chunks — each chunk is a dict with:
    chunk_id, text, source, page_number, subject
    chunk_size = how many words per chunk (500 is the industry standard)
    overlap = how many words to repeat between chunks to prevent losing context
    """
    chunks = []
    chunk_id = 0
    for page in pages:
        words = page['text'].split() # split text into individual words
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end] # grab the window of words
            chunk_text = ' '.join(chunk_words) # join back into a string
            chunks.append({
                'chunk_id': chunk_id,
                'text': chunk_text,
                'source': page['source'],
                'page_number': page['page_number'],
                'subject': 'Biology', # default subject
            })
            chunk_id += 1
            start += (chunk_size - overlap) # slide forward (overlap keeps context)
            if end >= len(words): # reached end of this page
                break
    print(f'Created {len(chunks)} chunks from {len(pages)} pages')
    return chunks

if __name__ == '__main__':
    import os
    from ingest import extract_text_from_pdf
    
    sample_path = 'data/ncert_biology.pdf'
    if os.path.exists(sample_path):
        pages = extract_text_from_pdf(sample_path)
        chunks = chunk_pages(pages)
        if chunks:
            print('\nSample chunk:')
            print(f'  ID: {chunks[0]["chunk_id"]}')
            print(f'  Page: {chunks[0]["page_number"]}')
            print(f'  Subject: {chunks[0]["subject"]}')
            print(f'  Text Preview: {chunks[0]["text"][:200]}...')
    else:
        print(f"Please download your NCERT Biology PDF and place it at: {sample_path}")
