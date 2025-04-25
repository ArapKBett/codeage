FROM python:3.10-slim

WORKDIR /app

# Add repositories for Swift, Julia, and other packages
RUN apt-get update && \
    apt-get install -y wget gnupg curl && \
    # Add Swift repository (Swift 5.9 for Debian Bullseye)
    curl -s https://archive.swift.org/keys/swift-release.asc | gpg --dearmor -o /usr/share/keyrings/swift-release.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/swift-release.gpg] https://archive.swift.org/debian bullseye main" > /etc/apt/sources.list.d/swift.list && \
    # Add Julia repository (manual download for Julia 1.8.5)
    wget -q https://julialang-s3.julialang.org/bin/linux/x64/1.8/julia-1.8.5-linux-x86_64.tar.gz -O /tmp/julia.tar.gz && \
    tar -xzf /tmp/julia.tar.gz -C /usr/local && \
    ln -s /usr/local/julia-1.8.5/bin/julia /usr/local/bin/julia && \
    rm /tmp/julia.tar.gz && \
    apt-get clean

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

# Install Haskell platform (if ghc alone is insufficient)
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
