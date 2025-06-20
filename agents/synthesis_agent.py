import json
from utils.ollama_integration import ollama_chat_completion

class ResearchSynthesizer:
    def generate_topic_synthesis(self, topic: str, papers: list, depth: str = "overview") -> str:
        depth_levels = {
            "overview": "1-paragraph summary",
            "detailed": "3-paragraph analysis",
            "technical": "comprehensive technical report"
        }
        
        # Prepare input for synthesis
        context = "\n\n".join([
            f"Paper {i+1}: {p.get('metadata', {}).get('title', 'Untitled')}\nSummary: {p.get('summary', 'No summary')}"
            for i, p in enumerate(papers)
        ])
        
        # Generate synthesis with local LLM
        response = ollama_chat_completion(
            model="nous-hermes2",
            system=(
                "You are a research synthesis expert. Generate a comparative analysis of papers "
                "focusing on: trends, conflicts, breakthroughs, and research gaps. "
                "Use academic language suitable for a podcast."
            ),
            messages=[{
                "role": "user",
                "content": f"Topic: {topic}\nDepth: {depth_levels[depth]}\n\nPapers:\n{context}"
            }]
        )
        
        return response