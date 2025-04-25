from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.code_generator import generate_code
from app.rag_retriever import retrieve_libraries
from app.sandbox import execute_code, lint_python_code
import os

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_code")
async def generate_code_endpoint(request: Request):
    data = await request.json()
    query = data.get("query", "")

    # Retrieve relevant libraries
    library_context = retrieve_libraries(query)

    # Generate code
    code = generate_code(query, library_context)

    # Determine language for sandbox
    language = "py"  # Default to Python
    if "javascript" in query.lower() or "js" in query.lower():
        language = "js"
    elif "java" in query.lower():
        language = "java"

    # Execute code in sandbox
    execution_result = None
    linting_result = None
    temp_file = f"temp_code.{language}"
    with open(temp_file, "w") as f:
        f.write(code)
    
    if language == "py":
        # Lint Python code
        linting_result = lint_python_code(temp_file)
        execution_result = execute_code(temp_file, language)
    elif language in ["js", "java"]:
        execution_result = execute_code(temp_file, language)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)

    return {
        "code": code,
        "execution_result": execution_result,
        "linting_result": linting_result,
        "libraries": library_context
    }
