import subprocess
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported languages for execution
SUPPORTED_EXECUTION_LANGUAGES = {
    "py", "js", "java", "cpp", "c", "cs", "go", "rs", "kt", "swift", "ts",
    "php", "rb", "scala", "pl", "lua", "dart", "ex", "hs", "ml", "fs", "r",
    "m", "sql", "ps1", "sh", "awk", "sed", "erl", "clj", "rkt", "scm", "lisp",
    "f90", "pas", "ada", "groovy", "nim", "zig", "v", "odin", "hx"
}

def execute_code(file_path: str, language: str) -> str:
    """
    Execute code in a sandbox for supported languages.
    """
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
        elif language == "cs":
            compile_cmd = ["mcs", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"C# compilation error: {compile_result.stderr}"
            cmd = ["mono", temp_file_path.replace(".cs", ".exe")]
        elif language == "go":
            cmd = ["go", "run", temp_file_path]
        elif language == "rs":
            compile_cmd = ["rustc", temp_file_path, "-o", "temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Rust compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "kt":
            compile_cmd = ["kotlinc", temp_file_path, "-include-runtime", "-d", "temp_code.jar"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Kotlin compilation error: {compile_result.stderr}"
            cmd = ["java", "-jar", "temp_code.jar"]
        elif language == "swift":
            compile_cmd = ["swiftc", temp_file_path, "-o", "temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Swift compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "ts":
            compile_cmd = ["tsc", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"TypeScript compilation error: {compile_result.stderr}"
            cmd = ["node", temp_file_path.replace(".ts", ".js")]
        elif language == "php":
            cmd = ["php", temp_file_path]
        elif language == "rb":
            cmd = ["ruby", temp_file_path]
        elif language == "scala":
            compile_cmd = ["scalac", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Scala compilation error: {compile_result.stderr}"
            class_name = os.path.basename(temp_file_path).replace(".scala", "")
            cmd = ["scala", class_name]
        elif language == "pl":
            cmd = ["perl", temp_file_path]
        elif language == "lua":
            cmd = ["lua", temp_file_path]
        elif language == "dart":
            cmd = ["dart", temp_file_path]
        elif language == "ex":
            cmd = ["elixir", temp_file_path]
        elif language == "hs":
            compile_cmd = ["ghc", temp_file_path, "-o", "temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Haskell compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "ml":
            cmd = ["ocaml", temp_file_path]
        elif language == "fs":
            compile_cmd = ["fsharpc", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"F# compilation error: {compile_result.stderr}"
            cmd = ["mono", temp_file_path.replace(".fs", ".exe")]
        elif language == "r":
            cmd = ["Rscript", temp_file_path]
        elif language == "m":
            cmd = ["matlab", "-batch", f"run('{temp_file_path}');"]
        elif language == "sql":
            cmd = ["sqlite3", ":memory:", f".read {temp_file_path}"]
        elif language == "ps1":
            cmd = ["powershell", "-File", temp_file_path]
        elif language == "sh":
            cmd = ["bash", temp_file_path]
        elif language == "awk":
            cmd = ["awk", "-f", temp_file_path]
        elif language == "sed":
            cmd = ["sed", "-f", temp_file_path]
        elif language == "erl":
            cmd = ["erl", "-noshell", "-s", os.path.basename(temp_file_path).replace(".erl", ""), "-s", "init", "stop"]
        elif language == "clj":
            cmd = ["clojure", temp_file_path]
        elif language == "rkt":
            cmd = ["racket", temp_file_path]
        elif language == "scm":
            cmd = ["scheme", "--script", temp_file_path]
        elif language == "lisp":
            cmd = ["clisp", temp_file_path]
        elif language == "f90":
            compile_cmd = ["gfortran", temp_file_path, "-o", "temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Fortran compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "pas":
            compile_cmd = ["fpc", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Pascal compilation error: {compile_result.stderr}"
            cmd = [temp_file_path.replace(".pas", "")]
        elif language == "ada":
            compile_cmd = ["gnatmake", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Ada compilation error: {compile_result.stderr}"
            cmd = [temp_file_path.replace(".ada", "")]
        elif language == "groovy":
            cmd = ["groovy", temp_file_path]
        elif language == "nim":
            compile_cmd = ["nim", "c", "-o:temp_code", temp_file_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Nim compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "zig":
            compile_cmd = ["zig", "build-exe", temp_file_path, "-femit-bin=temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Zig compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "v":
            compile_cmd = ["v", temp_file_path, "-o", "temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"V compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "odin":
            compile_cmd = ["odin", "build", temp_file_path, "-out:temp_code"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Odin compilation error: {compile_result.stderr}"
            cmd = ["./temp_code"]
        elif language == "hx":
            compile_cmd = ["haxe", "-main", os.path.basename(temp_file_path).replace(".hx", ""), "-js", "temp_code.js"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Haxe compilation error: {compile_result.stderr}"
            cmd = ["node", "temp_code.js"]
        else:
            return f"Execution not supported for {language}."

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        os.unlink(temp_file_path)

        # Clean up compiled files
        if language in ["java", "cpp", "c", "cs", "rs", "kt", "swift", "hs", "fs", "f90", "pas", "ada", "nim", "zig", "v", "odin"]:
            compiled_files = [
                "temp_code", temp_file_path.replace(".cs", ".exe"), temp_file_path.replace(".fs", ".exe"),
                temp_file_path.replace(".java", ".class"), "temp_code.jar", temp_file_path.replace(".pas", ""),
                temp_file_path.replace(".ada", "")
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
