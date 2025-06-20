import os
import asyncio
from gpt_researcher import GPTResearcher
from utils.file_processing import download_pdf, extract_metadata

class PaperResearchAgent:
    async def execute_plan(self, research_plan: list) -> list:
        papers = []
        for query in research_plan:
            # Initialize researcher for each query
            researcher = GPTResearcher(query=query, report_type="custom_report", config_path=None)
            report = await researcher.run()
            
            # Extract and process papers from sources
            for source in report.get("sources", []):
                if source["url"].endswith(".pdf"):
                    try:
                        paper_data = download_pdf(source["url"])
                        paper_data["metadata"] = extract_metadata(paper_data["content"])
                        paper_data["source_url"] = source["url"]
                        papers.append(paper_data)
                    except Exception as e:
                        print(f"Error processing {source['url']}: {str(e)}")
                        continue
        
        return papers