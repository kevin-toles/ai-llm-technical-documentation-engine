# ==============================================================================
# LLM Document Enhancer - Dockerfile
# ==============================================================================
# Multi-stage build for Python application
# See WBS 3.1.3.2: Docker Compose Updates
# ==============================================================================

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install runtime dependencies (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY workflows/ /app/workflows/
COPY config/ /app/config/
COPY tools/ /app/tools/
COPY ui/ /app/ui/
COPY scripts/ /app/scripts/
COPY examples/ /app/examples/

# Create directories for outputs and logs
RUN mkdir -p /app/outputs /app/logs /app/cache

# Environment defaults
ENV DOC_ENHANCER_ENV=production \
    DOC_ENHANCER_LOG_LEVEL=INFO \
    DOC_ENHANCER_GATEWAY_ENABLED=true \
    DOC_ENHANCER_GATEWAY_TIMEOUT=30.0 \
    DOC_ENHANCER_GATEWAY_SESSION_TTL=3600.0 \
    SBERT_FALLBACK_MODE=api \
    SBERT_API_URL=http://code-orchestrator:8083 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose application port
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
# Note: Update entrypoint when web server is implemented
CMD ["python", "-m", "workflows.main"]
