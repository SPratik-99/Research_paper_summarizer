import os
import requests
import json

def ollama_chat_completion(model: str, system: str, messages: list, format: str = "text") -> str:
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    url = f"{OLLAMA_HOST}/api/chat"
    
    payload = {
        "model": model,
        "system": system,
        "messages": messages,
        "options": {
            "temperature": 0.3,
            "num_ctx": 8192
        },
        "format": format
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if 'message' in chunk and 'content' in chunk['message']:
                        full_response += chunk['message']['content']
                except json.JSONDecodeError:
                    continue
        
        return full_response
    except Exception as e:
        return f"Error: {str(e)}"