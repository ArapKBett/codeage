async function generateCode() {
    const query = document.getElementById("query").value;
    const codeOutput = document.getElementById("code-output");
    const executionOutput = document.getElementById("execution-output");
    const lintingOutput = document.getElementById("linting-output");
    const librariesOutput = document.getElementById("libraries-output");

    try {
        const response = await fetch("/generate_code", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
        const data = await response.json();

        codeOutput.textContent = data.code;
        executionOutput.textContent = data.execution_result || "No execution performed.";
        lintingOutput.textContent = data.linting_result || "Linting not applicable.";
        librariesOutput.textContent = data.libraries;

        // Set Prism language class based on query
        codeOutput.className = query.toLowerCase().includes("javascript") ? "language-javascript" :
                              query.toLowerCase().includes("java") ? "language-java" : "language-python";
        Prism.highlightAll();
    } catch (error) {
        codeOutput.textContent = "Error: " + error.message;
    }
}
