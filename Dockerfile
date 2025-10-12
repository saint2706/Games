# Dockerfile for Games Collection
# Multi-stage build for smaller final image

FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Install the package
RUN pip install --user --no-cache-dir -e .

# Final stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libncurses5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 games && \
    mkdir -p /home/games/.game_stats && \
    chown -R games:games /home/games

# Copy Python packages from builder
COPY --from=builder /root/.local /home/games/.local
COPY --from=builder /app /app

# Set environment variables
ENV PATH=/home/games/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Switch to non-root user
USER games

# Default command: show help
CMD ["python", "-m", "scripts.launcher"]
