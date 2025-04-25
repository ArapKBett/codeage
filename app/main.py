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
    target_language = data.get("language", "").lower()  # Allow explicit language selection

    # Retrieve relevant libraries
    library_context = retrieve_libraries(query)

    # Generate code
    code = generate_code(query, library_context, target_language)

    # Determine language for sandbox
    language = target_language if target_language else detect_language(query)
    if not language:
        language = "py"  # Default to Python

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
    elif language in SUPPORTED_EXECUTION_LANGUAGES:
        execution_result = execute_code(temp_file, language)
    else:
        execution_result = f"Execution not supported for {language}. Code generation only."

    if os.path.exists(temp_file):
        os.remove(temp_file)

    return {
        "code": code,
        "execution_result": execution_result,
        "linting_result": linting_result,
        "libraries": library_context,
        "language": language
    }

def detect_language(query: str) -> str:
    """Detect programming language from query keywords."""
    query = query.lower()
    language_map = {
        "python": "py",
        "javascript": "js",
        "js": "js",
        "java": "java",
        "cpp": "cpp",
        "c++": "cpp",
        "c": "c",
        "csharp": "cs",
        "c#": "cs",
        "go": "go",
        "golang": "go",
        "rust": "rs",
        "kotlin": "kt",
        "swift": "swift",
        "typescript": "ts",
        "php": "php",
        "ruby": "rb",
        "scala": "scala",
        "perl": "pl",
        "lua": "lua",
        "dart": "dart",
        "elixir": "ex",
        "haskell": "hs",
        "ocaml": "ml",
        "fsharp": "fs",
        "f#": "fs",
        "r": "r",
        "matlab": "m",
        "sql": "sql",
        "powershell": "ps1",
        "bash": "sh",
        "shell": "sh",
        "awk": "awk",
        "sed": "sed",
        "verilog": "v",
        "vhdl": "vhdl",
        "erlang": "erl",
        "clojure": "clj",
        "racket": "rkt",
        "scheme": "scm",
        "lisp": "lisp",
        "fortran": "f90",
        "cobol": "cbl",
        "pascal": "pas",
        "ada": "ada",
        "prolog": "pl",
        "apl": "apl",
        "forth": "fs",
        "groovy": "groovy",
        "nim": "nim",
        "zig": "zig",
        "v": "v",
        "odin": "odin",
        "haxe": "hx",
        "red": "red",
        "rebol": "reb",
        # Add more as needed
    }
    for lang, ext in language_map.items():
        if lang in query:
            return ext
    return ""  # Default to empty if undetected
