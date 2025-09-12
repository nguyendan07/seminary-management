# Stage 1: Base build stage
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

# Install system dependencies
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get clean && apt-get update \
    && apt-get install -y libmaxminddb0 libmaxminddb-dev \
    && rm -rf /var/lib/apt/lists/*
 
# Set the working directory
WORKDIR /seminary-management

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock requirements.txt /seminary-management/

# First sync dependencies from lock file
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Add all project files
COPY . /seminary-management/

# Sync all dependencies including project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Stage 2: Final image, use a final image without uv
FROM python:3.13-slim-bookworm

# Install system dependencies
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get clean && apt-get update \
    && apt-get install -y libmaxminddb0 libmaxminddb-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the application from the builder
WORKDIR /seminary-management
COPY --from=builder /seminary-management /seminary-management

# Make the virtual environment accessible
ENV PATH="/seminary-management/.venv/bin:$PATH"

# Run Django collectstatic (ensure we're in the right directory)
WORKDIR /seminary-management

RUN python /seminary-management/manage.py collectstatic --noinput

EXPOSE 5000

CMD ["gunicorn", "seminary-management.wsgi", "-b:5000", "-w 10"]
