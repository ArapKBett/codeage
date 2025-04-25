from transformers import pipeline
import os

# Initialize CodeLlama (use 7B for Render's resource constraints)
model_name = "codellama/CodeLlama-7b-hf"
generator = pipeline("text-generation", model=model_name, device=-1)  # CPU for Render

def generate_code(query: str, library_context: str) -> str:
    prompt = f"{library_context}\n\nUser query: {query}\nGenerate code:\n```"
    response = generator(prompt, max_length=500, num_return_sequences=1)[0]["generated_text"]
    
    # Extract code from response
    code_start = response.find("```")
    code_end = response.rfind("```")
    if code_start != -1 and code_end != -1:
        return response[code_start + 3:code_end].strip()
    return response.strip()
