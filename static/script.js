async function generateCode() {
    const query = document.getElementById("query").value;
    const language = document.getElementById("language").value;
    const codeOutput = document.getElementById("code-output");
    const executionOutput = document.getElementById("execution-output");
    const lintingOutput = document.getElementById("linting-output");
    const librariesOutput = document.getElementById("libraries-output");
    const detectedLanguage = document.getElementById("detected-language");

    try {
        const response = await fetch("/generate_code", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, language })
        });
        const data = await response.json();

        codeOutput.textContent = data.code;
        executionOutput.textContent = data.execution_result || "No execution performed.";
        lintingOutput.textContent = data.linting_result || "Linting not applicable.";
        librariesOutput.textContent = data.libraries;
        detectedLanguage.textContent = data.language || "Auto-detected";

        // Set Prism language class
        const prismLang = getPrismLanguage(data.language);
        codeOutput.className = `language-${prismLang}`;
        Prism.highlightAll();
    } catch (error) {
        codeOutput.textContent = "Error: " + error.message;
    }
}

function getPrismLanguage(lang) {
    const prismMap = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "java": "java",
        "cpp": "cpp",
        "c": "c",
        "cs": "csharp",
        "go": "go",
        "rs": "rust",
        "kt": "kotlin",
        "swift": "swift",
        "php": "php",
        "rb": "ruby",
        "scala": "scala",
        "pl": "perl",
        "lua": "lua",
        "dart": "dart",
        "ex": "elixir",
        "hs": "haskell",
        "ml": "ocaml",
        "fs": "fsharp",
        "r": "r",
        "m": "matlab",
        "sql": "sql",
        "ps1": "powershell",
        "sh": "bash",
        "awk": "awk",
        "sed": "sed",
        "erl": "erlang",
        "clj": "clojure",
        "rkt": "racket",
        "scm": "scheme",
        "lisp": "lisp",
        "f90": "fortran",
        "pas": "pascal",
        "ada": "ada",
        "groovy": "groovy",
        "nim": "nim",
        "zig": "zig",
        "v": "v",
        "odin": "odin",
        "hx": "haxe"
    };
    return prismMap[lang] || "plaintext";
            }
