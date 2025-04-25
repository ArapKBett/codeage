# Use full Python 3.10 image for robust dependency support
FROM python:3.10

WORKDIR /app

# Install system dependencies and build tools
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    curl \
    gcc \
    g++ \
    python3-dev \
    libstdc++6 \
    libgomp1 \
    gfortran \
    libffi-dev \
    libssl-dev \
    make \
    cmake \
    libblas-dev \
    liblapack-dev \
    libopenblas-dev && \
    mkdir -p /usr/share/keyrings /usr/local && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install core programming language runtimes
RUN apt-get update && \
    apt-get install -y \
    nodejs \
    npm \
    openjdk-17-jdk \
    golang-go \
    ruby \
    php \
    r-base \
    lua5.3 \
    erlang \
    ocaml \
    scala \
    clisp \
    perl \
    tcl \
    racket \
    clang \
    llvm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install additional runtimes (handle failures gracefully)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    mono-complete \
    fsharp \
    ghc || true && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Haskell platform (optional)
RUN apt-get update && \
    apt-get install -y haskell-platform || true && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install additional tools
RUN npm install -g typescript && \
    gem install bundler

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install all Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --verbose -r requirements.txt --index-url https://download.pytorch.org/whl/cpu > pip_requirements.log 2>&1 || { cat pip_requirements.log; exit 1; }

COPY . .

ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
