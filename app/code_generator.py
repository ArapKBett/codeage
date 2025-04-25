from transformers import pipeline
import os

# Initialize model
model_name = os.getenv("MODEL_NAME", "codellama/CodeLlama-7b-hf")
generator = None  # Lazy-load to reduce memory usage during startup

def generate_code(query: str, library_context: str, target_language: str = "") -> str:
    global generator
    if generator is None:
        generator = pipeline("text-generation", model=model_name, device=-1)  # CPU for Render

    # Construct language-specific prompt
    language_prompt = f"Write {target_language} code for the following request:\n" if target_language else ""
    prompt = f"{library_context}\n\n{language_prompt}User query: {query}\nGenerate code:\n```"
    response = generator(prompt, max_length=500, num_return_sequences=1)[0]["generated_text"]
    
    # Extract code from response
    code_start = response.find("```")
    code_end = response.rfind("```")
    if code_start != -1 and code_end != -1:
        return response[code_start + 3:code_end].strip()
    return response.strip()
