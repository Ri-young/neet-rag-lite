import unittest
from unittest.mock import patch

from google.api_core import exceptions

from src import generate


class GenerateTests(unittest.TestCase):
    def test_generate_answer_handles_model_not_found(self):
        with patch.object(generate, "_get_model", side_effect=exceptions.NotFound("model missing")):
            result = generate.generate_answer("What is photosynthesis?", [{"text": "dummy", "source": "demo.pdf", "page_number": 1}])

        self.assertIn("could not be used", result)


if __name__ == "__main__":
    unittest.main()
