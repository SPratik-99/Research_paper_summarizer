import json
import os
from utils.ollama_integration import ollama_chat_completion

class PaperSummarizer:
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.system_prompt = (
            "You are an academic research assistant. Summarize research papers using:\n"
            "- Key contributions\n- Methodology\n- Results\n- Limitations\n\n"
            "Format your response as JSON with keys: title, summary, contributions (list), methods (list), results (list)"
        )
    
    def summarize(self, paper_data: dict) -> dict:
        content = paper_data["content"][:12000]  # First 12K characters
        
        response = ollama_chat_completion(
            model=self.model,
            system=self.system_prompt,
            messages=[{"role": "user", "content": content}],
            format="json"
        )
        
        try:
            summary = json.loads(response)
            # Add metadata
            if "metadata" in paper_data:
                summary["metadata"] = paper_data["metadata"]
            summary["source_url"] = paper_data["source_url"]
            return summary
        except json.JSONDecodeError:
            return {
                "title": "Summary Error",
                "summary": response,
                "contributions": [],
                "methods": [],
                "results": [],
                "metadata": paper_data.get("metadata", {}),
                "source_url": paper_data["source_url"]
            }