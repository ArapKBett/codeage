FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for multiple language runtimes
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
    haskell-platform \
    ocaml \
    scala \
    clisp \
    mono-complete \
    fsharp \
    julia \
    perl \
    tcl \
    racket \
    ghc \
    make \
    cmake \
    clang \
    llvm \
    swift \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install additional tools for specific languages
RUN npm install -g typescript \
    && gem install bundler \
    && pip install --no-cache-dir matlab-kernel \
    && curl -fsSL https://install.julialang.org | sh \
    && echo 'export PATH="$PATH:/root/.juliaup/bin"' >> /root/.bashrc

# Upgrade pip to handle complex dependencies
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000

EXPOSE 8000

# Ensure uvicorn binds to 0.0.0.0 and the PORT environment variable
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
