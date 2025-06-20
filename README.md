# Research Paper Summarization System

## Overview
This multi-agent system automates the process of discovering, analyzing, and summarizing research papers. Key components:
- **Research Planning**: STORM-inspired planning for comprehensive coverage
- **Paper Discovery**: GPT Researcher for finding relevant papers
- **Summarization**: Llama 3 via Ollama for local processing
- **Synthesis**: Cross-paper analysis and trend identification
- **Podcast Generation**: High-quality audio summaries

## Setup
1. Install Docker and Docker Compose
2. Create `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_key
SERPAPI_API_KEY=your_serpapi_key