# Coding Agent

A web-based AI agent that generates code across multiple programming languages, leveraging popular libraries without requiring training. Built with **FastAPI**, **CodeLlama-7B**, **LangChain**, and **Chroma**, it uses retrieval-augmented generation (RAG) with the `libraries.io` API, validates code with Pylint, and supports execution in Python, JavaScript, and Java. Optimized for deployment on **Render**.

## Features
- **Multi-language Support**: Generates code in Python, JavaScript, Java, C++, and more using CodeLlama-7B.
- **Library Awareness**: Fetches library data from `libraries.io` API and a local `libraries.json`.
- **Code Validation**: Lints Python code with Pylint and executes code in a sandbox for Python, JavaScript, and Java.
- **Web Interface**: User-friendly frontend with syntax highlighting via Prism.js.
- **Render Deployment**: Docker-based hosting with custom domain support.

## Prerequisites
- **Render Account**: Sign up at https://render.com.
- **GitHub Account**: For hosting the code repository.
- **Libraries.io API Key**: Sign up at https://libraries.io/api.
- **Domain Registrar** (optional): For custom domain (e.g., GoDaddy, Namecheap).
- **Python 3.10+** (optional, for local development).
- **Docker** (optional, for local testing).

## Deployment Steps on Render

### Step 1: Clone or Create the Repository
1. Clone this repository or create a new one:
   ```bash
   git clone https://github.com/your-repo/coding-agent.git
   cd coding-agent
