import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.planner_agent import ResearchPlanner
from agents.research_agent import PaperResearchAgent
from agents.summarization_agent import PaperSummarizer
from agents.synthesis_agent import ResearchSynthesizer
from agents.audio_agent import PodcastGenerator
from utils.citation_manager import CitationManager

app = FastAPI()

class ResearchRequest(BaseModel):
    topic: str
    depth: str = "overview"

@app.post("/research")
async def run_research(request: ResearchRequest):
    try:
        # Initialize components
        planner = ResearchPlanner(request.topic)
        researcher = PaperResearchAgent()
        summarizer = PaperSummarizer()
        synthesizer = ResearchSynthesizer()
        audio_gen = PodcastGenerator()
        citation_mgr = CitationManager()
        
        # Generate research plan
        research_plan = planner.generate_plan()
        print(f"Research Plan: {research_plan}")
        
        if len(papers) < 2:
            planner.revise_plan("Not enough relevant papers found.")
        
        # Execute research
        papers = await researcher.execute_plan(research_plan)
        print(f"Found {len(papers)} papers")
        
        # Process and summarize papers
        summarized_papers = []
        for paper in papers[:3]:  # Limit to top 3 papers
            paper_summary = summarizer.summarize(paper)
            summarized_papers.append(paper_summary)
            citation_mgr.add_paper(paper_summary)
        
        # Cross-paper synthesis
        synthesis = synthesizer.generate_topic_synthesis(
            request.topic, 
            summarized_papers, 
            request.depth
        )
        print("Synthesis completed")
        
        # Generate podcast
        audio_path = audio_gen.text_to_podcast(synthesis, style="academic")
        print(f"Audio generated at: {audio_path}")
        
        # Prepare response
        return {
            "topic": request.topic,
            "synthesis": synthesis,
            "papers": summarized_papers,
            "audio_path": audio_path,
            "citations": citation_mgr.export_bibtex()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)