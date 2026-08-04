import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Use gemini-2.5-flash which is active and compatible with your API key
MODEL_NAME = 'gemini-2.5-flash'

def build_prompt(question, chunks):
    """
    Builds the full prompt that gets sent to Gemini.
    """
    context_block = ''
    for i, chunk in enumerate(chunks):
        context_block += f'[Source {i+1}: {chunk["source"]} │ Page {chunk.get("page_number", "?")}]\n'
        context_block += chunk['text'] + '\n\n'
        
    prompt = f"""You are a NEET Biology expert mentor. STRICT RULES:
1. Answer ONLY using the context provided below.
2. If the answer is not in the context, say: 'This topic is not found in your uploaded material.'
3. Structure your answer exactly like this:
CONCEPT: [one-line definition]
EXPLANATION: [detailed explanation using context]
NEET TIP: [what NEET specifically tests about this topic]
4. Never invent information. Never use outside knowledge.

CONTEXT FROM NCERT BIOLOGY:
{context_block}

STUDENT QUESTION: {question}

YOUR ANSWER:"""
    return prompt

def generate_answer(question, chunks):
    """
    Sends the question + retrieved chunks to Gemini.
    """
    if not chunks:
        return 'No relevant content found in your uploaded study material.'
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = build_prompt(question, chunks)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating answer with {MODEL_NAME}: {e}"

if __name__ == '__main__':
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from retrieve import retrieve_chunks
    
    question = 'Explain the light reactions of photosynthesis.'
    chunks = retrieve_chunks(question, subject='Biology')
    answer = generate_answer(question, chunks)
    print('QUESTION:', question)
    print('='*60)
    print(answer)
