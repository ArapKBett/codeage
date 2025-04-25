import subprocess
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported languages for execution (reduced to match installed runtimes)
SUPPORTED_EXECUTION_LANGUAGES = {
    "py", "js", "java", "cpp", "c", "go", "php", "rb", "lua", "pl",
    "scala", "erl", "clj", "rkt", "r", "ts", "ocaml"
}

def execute_code(file_path: str, language: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{language}") as temp_file:
            with open(file_path, "r") as f:
                temp_file.write(f.read().encode())
            temp_file_path = temp_file.name

        cmd = []
        if language == "py":
            cmd = ["python", temp_file_path]
        elif language == "js":
            cmd = ["node", temp_file_path]
        elif language == "java":
            compile_cmd = ["javac", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Java compilation error: {compile_result.stderr}"
            class_name = os.path.basename(temp_file_path).replace(".java", "")
            cmd = ["java", "-cp", os.path.dirname(temp_file_path), class_name]
        elif language == "cpp":
            compile_cmd = ["g++", temp_file_path, "-o", "temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"C++ compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "c":
            compile_cmd = ["gcc", temp_file_path, "-o", "temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"C compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "go":
            cmd = ["go", "run", temp_file_path]
        elif language == "php":
            cmd = ["php", temp_file_path]
        elif language == "rb":
            cmd = ["ruby", temp_file_path]
        elif language == "lua":
            cmd = ["lua", temp_file_path]
        elif language == "pl":
            cmd = ["perl", temp_file_path]
        elif language == "scala":
            compile_cmd = ["scalac", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Scala compilation error: {compile_result.stderr}"
            class_name = os.path.basename(temp_file_path).replace(".scala", "")
            cmd = ["scala", class_name]
        elif language == "erl":
            cmd = ["erl", "-noshell", "-s", os.path.basename(temp_file_path).replace(".erl", ""), "-s", "init", "stop"]
        elif language == "clj":
            cmd = ["clojure", temp_file_path]
        elif language == "rkt":
            cmd = ["racket", temp_file_path]
        elif language == "r":
            cmd = ["Rscript", temp_file_path]
        elif language == "ts":
            compile_cmd = ["tsc", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"TypeScript compilation error: {compile_result.stderr}"
            cmd = ["node", temp_file_path.replace(".ts", ".js")]
        elif language == "ocaml":
            cmd = ["ocaml", temp_file_path]
        else:
            return f"Execution not supported for {language}."

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        os.unlink(temp_file_path)

        # Clean up compiled files
        if language in ["java", "cpp", "c", "scala", "ts"]:
            compiled_files = [
                "temp_code", temp_file_path.replace(".java", ".class"),
                temp_file_path.replace(".ts", ".js")
            ]
            for f in compiled_files:
                if os.path.exists(f):
                    os.unlink(f)

        if result.stderr:
            return f"Error: {result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Execution timed out after 10 seconds."
    except Exception as e:
        return f"Execution error: {str(e)}"

def lint_python_code(file_path: str) -> str:
    try:
        result = subprocess.run(
            ["pylint", "--disable=C0301,C0114,C0115,C0116", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return "No linting issues found."
        return f"Linting issues:\n{result.stdout}"
    except Exception as e:
        return f"Linting error: {str(e)}"
