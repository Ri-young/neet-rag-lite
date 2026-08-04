# NEET RAG Lite

A lightweight Retrieval-Augmented Generation (RAG) project for NEET preparation.

## What it does

- Extracts text from uploaded PDF documents
- Splits the text into overlapping chunks
- Embeds each chunk with sentence-transformers
- Stores vectors in ChromaDB for similarity search
- Retrieves the most relevant passages for a question
- Generates an answer with Gemini and shows source citations

## Setup

1. Create and activate a virtual environment.
2. Install requirements:
   `pip install -r requirements.txt`
3. Add your Gemini API key to a `.env` file:
   `GEMINI_API_KEY=your-key-here`
4. Put a PDF in the `data/` folder (for example `data/ncert_biology.pdf`).
5. Run the app:
   `streamlit run app.py`

## Project structure

- `src/ingest.py` – PDF text extraction
- `src/chunk.py` – chunking logic
- `src/embed_store.py` – embedding + vector storage
- `src/retrieve.py` – semantic retrieval
- `src/generate.py` – Gemini answer generation
- `src/citations.py` – citation formatting
- `app.py` – Streamlit UI

## Next steps

- Add more subjects and chapters
- Improve retrieval with reranking
- Add quiz generation and flashcards
