from sentence_transformers import SentenceTransformer
import chromadb

# Load the embedding model — this downloads ~90MB on first run, then it's cached
# 'all-MiniLM-L6-v2' is fast, free, runs locally — no API needed
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create ChromaDB client — stores data in a local folder called 'chroma_db'
client = chromadb.PersistentClient(path='./chroma_db')

def get_or_create_collection(subject='Biology'):
    """
    Creates or retrieves a separate collection for the subject.
    """
    collection_name = f'neet_{subject.lower()}'
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={'hnsw:space': 'cosine'} # use cosine similarity for search
    )
    return collection

def embed_and_store(chunks):
    """
    Takes chunks from chunk.py
    Converts each chunk's text into an embedding vector
    Stores vector + original text + metadata in ChromaDB
    """
    # Group chunks by subject (for separate collections)
    subjects = set(c['subject'] for c in chunks)
    
    for subject in subjects:
        subject_chunks = [c for c in chunks if c['subject'] == subject]
        collection = get_or_create_collection(subject)
        
        # Extract just the text for batch embedding
        texts = [c['text'] for c in subject_chunks]
        
        # Embed ALL chunks at once (batch is faster than one by one)
        print(f'Embedding {len(texts)} chunks for {subject}...')
        embeddings = model.encode(texts, show_progress_bar=True)
        
        # Store in ChromaDB
        collection.add(
            ids = [str(c['chunk_id']) for c in subject_chunks],
            embeddings = embeddings.tolist(), # ChromaDB wants a plain list
            documents = texts, # original text (for citations)
            metadatas = [{ # metadata per chunk
                'source': c['source'],
                'page_number': c['page_number'],
                'subject': c['subject'],
            } for c in subject_chunks]
        )
        print(f'Stored {len(subject_chunks)} chunks in ChromaDB collection: neet_{subject.lower()}')

if __name__ == '__main__':
    import os
    import sys
    # Add src to python path if not present to allow relative imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from ingest import extract_text_from_pdf
    from chunking import chunk_pages
    
    sample_path = 'data/ncert_biology.pdf'
    if os.path.exists(sample_path):
        pages = extract_text_from_pdf(sample_path)
        chunks = chunk_pages(pages)
        embed_and_store(chunks)
        print('Done! Your NCERT Biology is now searchable.')
    else:
        print(f"Please download your NCERT Biology PDF and place it at: {sample_path}")
