import os
import sys
import tempfile
import unittest

import fitz

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from src.chunk import chunk_pages
from src.citations import format_citations
from src.ingest import extract_text_from_pdf


class PipelineTests(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, "sample.pdf")
            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 72), "Photosynthesis is the process plants use to make food")
            doc.save(pdf_path)
            doc.close()

            pages = extract_text_from_pdf(pdf_path)

            self.assertTrue(pages)
            self.assertEqual(pages[0]["page_number"], 1)
            self.assertIn("Photosynthesis", pages[0]["text"])

    def test_chunk_pages_with_overlap(self):
        pages = [{
            "page_number": 1,
            "text": " ".join([f"word{i}" for i in range(700)]),
            "source": "sample.pdf",
        }]

        chunks = chunk_pages(pages, chunk_size=200, overlap=50)

        self.assertGreaterEqual(len(chunks), 3)
        self.assertEqual(chunks[0]["page_number"], 1)
        self.assertEqual(chunks[0]["subject"], "Biology")
        self.assertTrue(chunks[0]["text"].startswith("word0"))

    def test_format_citations_deduplicates(self):
        chunks = [
            {"source": "sample.pdf", "page_number": 2, "score": 0.91},
            {"source": "sample.pdf", "page_number": 2, "score": 0.89},
            {"source": "sample.pdf", "page_number": 5, "score": 0.73},
        ]

        citations = format_citations(chunks)

        self.assertEqual(len(citations), 2)
        self.assertIn("Page 2", citations[0])
        self.assertIn("Page 5", citations[1])


if __name__ == "__main__":
    unittest.main()
