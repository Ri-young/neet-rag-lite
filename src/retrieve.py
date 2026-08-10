import chromadb

client = chromadb.PersistentClient(path='./chroma_db')

def retrieve_chunks(question, subject='Biology', top_k=5):
    """
    Given a student question and subject, finds the most relevant chunks.
    Returns a list of dicts with: text, source, page_number, similarity_score
    question: the student's question (plain text)
    subject: which collection to search ('Biology', 'Chemistry', 'Physics')
    top_k: how many chunks to return (5 is the sweet spot)
    """
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Step 1: embed the question
    question_embedding = model.encode(question).tolist()
    
    # Step 2: get the right collection
    collection_name = f'neet_{subject.lower()}'
    try:
        collection = client.get_collection(collection_name)
    except Exception:
        print(f'Collection {collection_name} not found. Did you run embed_store.py?')
        return []
        
    # Step 3: search ChromaDB
    results = collection.query(
        query_embeddings = [question_embedding],
        n_results = top_k,
        include = ['documents', 'metadatas', 'distances']
    )
    
    # Step 4: format results nicely
    chunks = []
    if not results or not results['documents'] or not results['documents'][0]:
        return chunks
        
    for i in range(len(results['documents'][0])):
        chunks.append({
            'text': results['documents'][0][i],
            'source': results['metadatas'][0][i]['source'],
            'page_number': results['metadatas'][0][i]['page_number'],
            'subject': results['metadatas'][0][i]['subject'],
            'score': round(1 - results['distances'][0][i], 3) # convert distance to similarity
        })
    return chunks

if __name__ == '__main__':
    question = 'What is the Calvin Cycle and where does it happen?'
    results = retrieve_chunks(question, subject='Biology', top_k=5)
    print(f'Top {len(results)} chunks for: "{question}"\n')
    for i, chunk in enumerate(results):
        print(f'--- Chunk {i+1} ---')
        print(f'Source: {chunk["source"]} │ Page: {chunk["page_number"]} │ Score: {chunk["score"]}')
        print(f'Text: {chunk["text"][:200]}...')
        print()
