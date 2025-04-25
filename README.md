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
- **Domain Registrar** (optional): For custom domain (e.g., GoDaddy, Namecheap, Google Domains).
- **Python 3.10+** (optional, for local development).
- **Docker** (optional, for local testing).

## Deployment Steps on Render

Follow these steps to deploy the Coding Agent on Render and optionally set up a custom domain.

### Step 1: Prepare the Codebase
1. **Clone or Create the Repository**:
   - If using an existing repository, clone it:
     ```bash
     git clone https://github.com/your-repo/coding-agent.git
     cd coding-agent
     ```
   - Alternatively, create a new directory and copy all project files (`app/`, `static/`, `data/`, `Dockerfile`, `render.yaml`, `requirements.txt`, `README.md`).
2. **Verify Files**:
   - Ensure the project structure matches the one provided in this repository.
   - Check that `data/libraries.json` contains the sample library data or update it with additional libraries.
3. **Obtain a Libraries.io API Key**:
   - Sign up at https://libraries.io/api and generate an API key.
   - Note the key for use in Step 4.

### Step 2: Set Up a GitHub Repository
1. **Initialize a Git Repository**:
   - If not already a Git repository, initialize it:
     ```bash
     git init
     ```
2. **Add and Commit Files**:
   - Add all files to Git:
     ```bash
     git add .
     git commit -m "Initial commit for Render deployment"
     ```
3. **Create a GitHub Repository**:
   - Go to https://github.com and create a new repository (e.g., `coding-agent`).
   - Copy the repository URL (e.g., `https://github.com/your-username/coding-agent.git`).
4. **Push to GitHub**:
   - Link the local repository to GitHub and push:
     ```bash
     git remote add origin https://github.com/your-username/coding-agent.git
     git branch -M main
     git push -u origin main
     ```

### Step 3: Create a Web Service on Render
1. **Log in to Render**:
   - Go to https://dashboard.render.com and sign in or create an account.
2. **Start a New Web Service**:
   - Click **New** > **Web Service** in the Render dashboard.
3. **Connect GitHub**:
   - Click **Connect GitHub** and authorize Render to access your repositories.
   - Select the `coding-agent` repository from the list.
4. **Configure the Web Service**:
   - **Name**: Enter `coding-agent` (or a custom name).
   - **Environment**: Select **Docker**.
   - **Branch**: Choose `main`.
   - **Region**: Select the closest region (e.g., Oregon for US users).
   - **Instance Type**:
     - **Free**: Suitable for testing but slow (512MB RAM, 0.5 CPU). May timeout during model loading.
     - **Standard** (recommended): ~$7/month, 1 CPU, 2GB RAM for reliable performance.
   - **Environment Variables**:
     - Add two variables:
       - **Key**: `PORT`, **Value**: `8000`
       - **Key**: `LIBRARIES_IO_API_KEY`, **Value**: Your libraries.io API key from Step 1.
   - **Disks** (optional):
     - If preloading CodeLlama-7B weights, click **Add Disk**:
       - Name: `model-weights`
       - Mount Path: `/app/models`
       - Size: 10GB
       - Update `app/code_generator.py` to load weights from `/app/models` (see code comments).
5. **Review and Deploy**:
   - Click **Create Web Service** to start the build process.

### Step 4: Monitor the Build and Deployment
1. **Check Build Progress**:
   - In the Render dashboard, go to your `coding-agent` service and view the **Logs** tab.
   - The build process (Docker image creation, dependency installation, model download) takes 10-15 minutes due to CodeLlama-7B and Node.js/OpenJDK installation.
2. **Handle Build Errors**:
   - If the build fails, check logs for issues (e.g., missing `LIBRARIES_IO_API_KEY`, insufficient memory on free tier).
   - For free tier timeouts, switch to the Standard plan or preload model weights.
3. **Confirm Deployment**:
   - Once deployed, Render provides a URL (e.g., `https://coding-agent.onrender.com`).
   - Open the URL in a browser to access the web interface.

### Step 5: Test the Application
1. **Test the Web Interface**:
   - Visit `https://coding-agent.onrender.com`.
   - Enter queries like:
     - "Write a Python script using pandas to analyze a CSV"
     - "Write a JavaScript function using Express"
     - "Write a Java program with Spring"
   - Verify that code, execution results, linting (for Python), and library suggestions display correctly.
2. **Test the API**:
   - Use `curl` or a tool like Postman:
     ```bash
     curl -X POST https://coding-agent.onrender.com/generate_code \
     -H "Content-Type: application/json" \
     -d '{"query": "Write a Python script using pandas to analyze a CSV"}'
     ```
   - Check for code, execution, linting, and library data in the response.
3. **Verify Extended Features**:
   - **Libraries**: Ensure `libraries.io` API and `libraries.json` provide relevant suggestions.
   - **Linting**: Python queries return Pylint results (e.g., "No linting issues found" or specific issues).
   - **Sandbox**: Python, JavaScript, and Java code execute correctly (e.g., "Hello, World!" output).

### Step 6: Set Up a Custom Domain (Optional)
1. **Purchase a Domain**:
   - Buy a domain from a registrar like GoDaddy, Namecheap, or Google Domains (e.g., `mycodingagent.com`).
   - Ensure you can access the DNS management panel.
2. **Add the Custom Domain in Render**:
   - In the Render dashboard, go to your `coding-agent` service.
   - Navigate to **Settings** > **Custom Domains**.
   - Click **Add Custom Domain** and enter your domain (e.g., `mycodingagent.com` or `app.mycodingagent.com`).
   - Render provides DNS records (CNAME for subdomains, A for root domains).
3. **Configure DNS Records**:
   - Log in to your registrar’s DNS management panel.
   - Add the records from Render:
     - **Subdomain** (e.g., `app.mycodingagent.com`):
       - Type: `CNAME`
       - Name: `app`
       - Value: `coding-agent.onrender.com` (your Render URL)
     - **Root Domain** (e.g., `mycodingagent.com`):
       - Type: `A`
       - Name: `@`
       - Value: Render’s IP address (check Render’s DNS instructions)
   - Save changes. DNS propagation may take 1-48 hours.
4. **Verify the Custom Domain**:
   - In Render, wait for the domain status to show **Verified** (indicating DNS is configured).
   - Access the app at `https://mycodingagent.com` or `https://app.mycodingagent.com`.
   - Render automatically provisions an SSL certificate via Let’s Encrypt for HTTPS.
5. **Test the Custom Domain**:
   - Open the custom domain in a browser to confirm the web interface loads.
   - Test the API:
     ```bash
     curl -X POST https://mycodingagent.com/generate_code \
     -H "Content-Type: application/json" \
     -d '{"query": "Write a Python script using pandas to analyze a CSV"}'
     ```

## Local Development (Optional)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
