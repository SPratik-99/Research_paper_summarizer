import requests
import PyPDF2
from io import BytesIO
import re

def download_pdf(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    
    # Read PDF content
    with BytesIO(response.content) as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        content = ""
        for page in reader.pages:
            content += page.extract_text() + "\n"
    
    return {
        "content": content,
        "source_url": url
    }

def extract_metadata(content: str) -> dict:
    # Simple metadata extraction (title, authors)
    title = "Unknown"
    authors = []
    
    # Try to extract title from first line
    lines = content.split('\n')
    if lines:
        title = lines[0].strip()
    
    # Try to find authors (heuristic: look for common patterns)
    for i in range(min(5, len(lines))):  # Check first 5 lines
        line = lines[i].strip()
        if "author" in line.lower() or "by " in line.lower():
            authors = re.split(r',|\band\b', line)
            authors = [a.strip() for a in authors if a.strip()]
            break
    
    return {
        "title": title,
        "authors": authors
    }