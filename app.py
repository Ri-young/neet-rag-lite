import streamlit as st
import sys
import os

# Add src folder to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ingest import extract_text_from_pdf
from chunk import chunk_pages
from embed_store import embed_and_store
from retrieve import retrieve_chunks
from generate import generate_answer
from citations import format_citations

# ── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title = 'NEET RAG — Chat with NCERT',
    page_icon = '📚',
    layout = 'wide'
)

st.title('📚 NEET RAG — Chat with Your NCERT')
st.caption('Upload NCERT Biology PDF → Ask any NEET question → Get cited answers')

# Make sure data directory exists
os.makedirs('data', exist_ok=True)

# ── Sidebar: Upload + Index ───────────────────────────
with st.sidebar:
    st.header('📄 Upload Study Material')
    subject = st.selectbox('Subject', ['Biology', 'Chemistry', 'Physics'])
    uploaded = st.file_uploader('Upload NCERT PDF', type='pdf')
    if uploaded and st.button('Index This PDF'):
        # save uploaded file temporarily
        temp_path = os.path.join('data', 'temp.pdf')
        with open(temp_path, 'wb') as f:
            f.write(uploaded.read())
        with st.spinner('Reading and indexing your PDF...'):
            pages = extract_text_from_pdf(temp_path)
            chunks = chunk_pages(pages)
            # override subject from dropdown
            for c in chunks:
                c['subject'] = subject
            embed_and_store(chunks)
        st.success(f'Indexed {len(chunks)} chunks from {uploaded.name}!')
    st.divider()
    st.caption('Built as IIT Patna RAG Project 2')

# ── Main: Chat Interface ──────────────────────────────
st.subheader(f'Ask a {subject} Question')
question = st.text_input(
    'Your Question',
    placeholder='e.g. Explain the Calvin Cycle for NEET',
)

if st.button('🔍 Search & Answer', type='primary') and question:
    with st.spinner('Searching your study material...'):
        chunks = retrieve_chunks(question, subject=subject, top_k=5)
        answer = generate_answer(question, chunks)
        cites = format_citations(chunks)
        
    # Show Answer
    st.subheader('📝 Answer')
    st.markdown(answer)
    
    # Show Citations
    st.subheader('📚 Sources Used')
    if cites:
        for c in cites:
            st.info(c)
    else:
        st.warning('No relevant content found in uploaded material.')
        
    # Show raw chunks (expandable — for debugging + transparency)
    with st.expander('🔬 View Retrieved Chunks (Debug)'):
        for i, chunk in enumerate(chunks):
            st.markdown(f'**Chunk {i+1}** │ Page {chunk["page_number"]} │ Score: {chunk["score"]}')
            st.text(chunk['text'][:400])
            st.divider()
