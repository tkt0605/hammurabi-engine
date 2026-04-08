FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends \
    z3 \
    libz3-dev \
    pkg-config \
    build-essential \
    curl \
    git \
    rm -rf /var/lib/apt/lists/*

USER vscode
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    
ENV PATH="/home/vscode/.local/bin:/home/vscode/.cargo/bin:${PATH}"

RUN uv pip install --no-cache-dir \
    maturin \
    pyo3 \
    django \
    djangorestframework \
    pytest
ENV Z3_SYS_Z3_HEADER_PATH=/usr/include/z3.h

WORKDIR /workspaces/hammurabi