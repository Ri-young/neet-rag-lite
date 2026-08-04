import fitz # this is PyMuPDF — 'fitz' is its import name
import os

def extract_text_from_pdf(pdf_path):
    """
    Opens a PDF file and extracts all text page by page.
    Returns a list of dicts — one dict per page.
    Each dict has: page_number, text, source (filename)
    """
    doc = fitz.open(pdf_path) # open the PDF
    pages = [] # we'll collect results here
    for page_num in range(len(doc)): # loop through every page
        page = doc[page_num] # get one page
        text = page.get_text() # extract all text from that page
        # clean up the text a little
        text = text.strip() # remove leading/trailing whitespace
        text = ' '.join(text.split()) # collapse multiple spaces into one
        if len(text) > 50: # skip pages with almost no text (images, blanks)
            pages.append({
                'page_number': page_num + 1, # humans count from 1, Python from 0
                'text': text,
                'source': os.path.basename(pdf_path) # just the filename, not full path
            })
    print(f'Extracted {len(pages)} pages from {pdf_path}')
    return pages

# TEST: run this file directly to see if extraction works
if __name__ == '__main__':
    sample_path = 'data/ncert_biology.pdf'
    if os.path.exists(sample_path):
        pages = extract_text_from_pdf(sample_path)
        print(f'First page preview:')
        if pages:
            print(pages[0]['text'][:300]) # show first 300 characters of page 1
        else:
            print("No text pages extracted (check if it is a scanned image PDF).")
    else:
        print(f"Please download your NCERT Biology PDF and place it at: {sample_path}")
