#!/bin/bash
# This script will run when the container starts to download models
echo "Downloading Ollama models..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "llama3"}' &
curl -X POST http://ollama:11434/api/pull -d '{"name": "nous-hermes2"}' &
wait
echo "Model download completed!"