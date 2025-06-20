import unittest
from unittest.mock import patch, MagicMock
from agents.summarization_agent import PaperSummarizer
import json

class TestSummarizationAgent(unittest.TestCase):
    @patch('utils.ollama_integration.ollama_chat_completion')
    def test_summarization(self, mock_ollama):
        # Mock response from Ollama
        mock_response = json.dumps({
            "title": "Test Paper",
            "summary": "This is a summary.",
            "contributions": ["Contribution 1", "Contribution 2"],
            "methods": ["Method A"],
            "results": ["Result X"]
        })
        mock_ollama.return_value = mock_response
        
        agent = PaperSummarizer()
        paper_data = {
            "content": "Abstract: This is a test paper...",
            "source_url": "http://example.com/paper.pdf",
            "metadata": {"title": "Test Paper", "authors": ["Author A"]}
        }
        result = agent.summarize(paper_data)
        
        self.assertEqual(result["title"], "Test Paper")
        self.assertEqual(len(result["contributions"]), 2)
        self.assertEqual(result["source_url"], "http://example.com/paper.pdf")

if __name__ == "__main__":
    unittest.main()