from openai import OpenAI
import os

class ResearchPlanner:
    def __init__(self, topic: str):
        self.topic = topic
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_plan(self) -> list:
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a research planning expert. Generate a search plan for academic papers."},
                {"role": "user", "content": f"Create a detailed research plan for: {self.topic}. Include 5 key aspects to investigate."}
            ],
            temperature=0.2
        )
        
        plan = response.choices[0].message.content.split('\n')
        return [p.strip() for p in plan if p.strip()]