import subprocess
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_code(file_path: str, language: str) -> str:
    """
    Execute code in a sandbox for Python, JavaScript, or Java.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{language}") as temp_file:
            with open(file_path, "r") as f:
                temp_file.write(f.read().encode())
            temp_file_path = temp_file.name

        if language == "py":
            cmd = ["python", temp_file_path]
        elif language == "js":
            cmd = ["node", temp_file_path]
        elif language == "java":
            # Compile Java code
            compile_cmd = ["javac", temp_file_path]
            compile_result = subprocess.run(
                compile_cmd, capture_output=True, text=True, timeout=10
            )
            if compile_result.returncode != 0:
                return f"Java compilation error: {compile_result.stderr}"
            # Run Java code (assume class name matches file name without .java)
            class_name = os.path.basename(temp_file_path).replace(".java", "")
            cmd = ["java", "-cp", os.path.dirname(temp_file_path), class_name]
        else:
            return f"Unsupported language: {language}"

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10
        )
        os.unlink(temp_file_path)
        if language == "java":
            # Clean up compiled .class file
            class_file = temp_file_path.replace(".java", ".class")
            if os.path.exists(class_file):
                os.unlink(class_file)

        if result.stderr:
            return f"Error: {result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Execution timed out after 10 seconds."
    except Exception as e:
        return f"Execution error: {str(e)}"

def lint_python_code(file_path: str) -> str:
    """
    Lint Python code using Pylint.
    """
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
