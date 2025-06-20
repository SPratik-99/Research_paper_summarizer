class CitationManager:
    def __init__(self):
        self.papers = []
    
    def add_paper(self, paper: dict):
        self.papers.append(paper)
    
    def export_bibtex(self) -> str:
        bibtex = ""
        for i, paper in enumerate(self.papers):
            title = paper.get('metadata', {}).get('title', 'Untitled')
            authors = paper.get('metadata', {}).get('authors', ['Unknown'])
            bibtex += f"""@article{{paper{i+1},
  title = {{{title}}},
  author = {{{', '.join(authors)}}},
  url = {{{paper.get('source_url', '')}}},
  year = {{2024}}
}}\n\n"""
        return bibtex