FROM python:3.10-slim

WORKDIR /app

# Install prerequisites and create directories
RUN apt-get update && \
    apt-get install -y wget gnupg curl libstdc++6 && \
    mkdir -p /usr/share/keyrings /usr/local && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install core dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    python3-dev \
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
    make \
    cmake \
    clang \
    llvm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install additional dependencies (handle failures gracefully)
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

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
