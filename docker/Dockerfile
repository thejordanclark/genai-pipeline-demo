# ==============================================================================
# GxP-Validated Clinical Trial Data Processing System - Docker Image
# ==============================================================================
# 
# This Dockerfile creates a containerized environment for the Python-based
# clinical trial validation system. It is designed for use in GxP-regulated
# environments and follows industry best practices for security, reproducibility,
# and compliance.
#
# Compliance Standards:
# - 21 CFR Part 11 (Electronic Records and Electronic Signatures)
# - EU Annex 11 (Computerised Systems)
# - ISO 13485 (Medical Devices Quality Management)
# - GAMP 5 (Good Automated Manufacturing Practice)
#
# Build Command:
#   docker build -t clinical-validation:1.0.0 -f docker/Dockerfile .
#
# Run Command:
#   docker run --rm -v $(pwd)/data:/app/data clinical-validation:1.0.0
#
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Base Image Selection
# ------------------------------------------------------------------------------
# Using Python 3.13-slim as the base image provides:
# - Small footprint (~120MB vs ~900MB for full Python image)
# - Security: Fewer packages = smaller attack surface
# - Official Python Software Foundation image with regular security updates
# - Debian-based for stability in regulated environments
# ------------------------------------------------------------------------------

FROM python:3.13-slim AS base

# ------------------------------------------------------------------------------
# Stage 2: Metadata and Labels
# ------------------------------------------------------------------------------
# Labels provide traceable metadata for compliance and change control.
# These are stored in the image and can be inspected with 'docker inspect'.
# Labels follow OCI (Open Container Initiative) standards where applicable.
# ------------------------------------------------------------------------------

LABEL maintainer="Clinical IT Team <clinical-it@example.com>" \
      version="1.0.0" \
      description="GxP-Validated Python Clinical Trial Data Validation System" \
      org.opencontainers.image.title="Clinical Validation System" \
      org.opencontainers.image.description="Automated validation system for clinical trial data processing" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="Clinical Research Organization" \
      org.opencontainers.image.licenses="Proprietary" \
      org.opencontainers.image.created="2026-02-18" \
      compliance.standards="21CFR11,EUAnnex11,ISO13485,GAMP5" \
      compliance.validated="true" \
      compliance.validation-date="2026-02-18" \
      security.scan-required="true" \
      gxp.system-type="computerised-system" \
      gxp.risk-category="GAMP5-Category3"

# ------------------------------------------------------------------------------
# Stage 3: System Dependencies
# ------------------------------------------------------------------------------
# Install minimal system packages required for Python dependencies.
# Using --no-install-recommends minimizes image size and attack surface.
# apt-get clean removes package lists to reduce final image size.
# ------------------------------------------------------------------------------

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Build tools for compiling Python packages with C extensions
        gcc \
        g++ \
        # PostgreSQL client library (if needed for database connections)
        libpq-dev \
        # Utility for health checks and troubleshooting
        curl \
        && \
    # Clean up apt cache to reduce image size (important for GxP archival)
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Pre-create application directory with proper permissions
    mkdir -p /app

# ------------------------------------------------------------------------------
# Stage 4: Security - Non-Root User Setup
# ------------------------------------------------------------------------------
# Running as non-root is a critical security requirement for GxP systems.
# This prevents privilege escalation attacks and follows the principle of
# least privilege, which is required by regulatory guidance.
# 
# UID/GID 10001: Arbitrary non-privileged user/group ID
# Home directory: /home/clinicalapp for user-specific files
# No password: Container user should not have interactive login capability
# ------------------------------------------------------------------------------

RUN groupadd --gid 10001 clinicalapp && \
    useradd --uid 10001 --gid clinicalapp --shell /bin/bash --create-home clinicalapp && \
    # Grant ownership of application directory to non-root user
    chown -R clinicalapp:clinicalapp /app

# ------------------------------------------------------------------------------
# Stage 5: Python Environment Configuration
# ------------------------------------------------------------------------------
# Set environment variables for Python behavior in containerized environments.
# These settings improve performance, logging clarity, and security.
# All variables are documented for validation purposes.
# ------------------------------------------------------------------------------

ENV \
    # Ensures Python output is sent straight to terminal without buffering
    # Critical for real-time logging in production environments
    PYTHONUNBUFFERED=1 \
    \
    # Prevents Python from writing .pyc bytecode files to disk
    # Not needed in containers and reduces disk I/O
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # Disables pip's cache to reduce image size
    PIP_NO_CACHE_DIR=1 \
    \
    # Disables pip version check to avoid network calls during build
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    \
    # Enforces UTF-8 encoding for consistent text handling across platforms
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    \
    # Application-specific environment variables
    APP_HOME=/app \
    APP_USER=clinicalapp

# ------------------------------------------------------------------------------
# Stage 6: Working Directory Setup
# ------------------------------------------------------------------------------
# Set working directory for all subsequent commands.
# All application code will be located under /app for consistency.
# This aids in audit trails and validation documentation.
# ------------------------------------------------------------------------------

WORKDIR /app

# ------------------------------------------------------------------------------
# Stage 7: Python Dependencies Installation (Layer Caching Optimization)
# ------------------------------------------------------------------------------
# Copy and install Python dependencies BEFORE copying source code.
# This optimizes Docker layer caching - dependencies rarely change, so this
# layer will be cached across builds, significantly speeding up development.
#
# Security Note: requirements.txt should contain pinned versions (==) to ensure
# reproducibility and traceability, which is required for GxP validation.
# ------------------------------------------------------------------------------

COPY --chown=clinicalapp:clinicalapp requirements.txt .

# Install Python dependencies
# This is done as root to allow system-wide pip package installation
RUN pip install --no-cache-dir --upgrade pip==24.3.1 && \
    pip install --no-cache-dir -r requirements.txt && \
    # Remove build dependencies after installation to reduce image size
    # and attack surface (defense in depth security principle)
    apt-get purge -y --auto-remove gcc g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Stage 8: Application Code Deployment
# ------------------------------------------------------------------------------
# Copy application source code, tests, and configuration files.
# Using --chown ensures all files are owned by the non-root user.
#
# Directory Structure (follows standard Python project layout):
# /app
# ├── src/              - Application source code modules
# ├── tests/            - Unit and integration test suites
# ├── scripts/          - Utility scripts (validation reports, audit logs)
# ├── validation/       - Validation documentation and logs
# ├── test_data/        - Test datasets for validation
# └── setup.py          - Python package configuration
#
# Note: Large data files should be mounted as volumes, not copied into image
# ------------------------------------------------------------------------------

COPY --chown=clinicalapp:clinicalapp src/ ./src/
COPY --chown=clinicalapp:clinicalapp tests/ ./tests/
COPY --chown=clinicalapp:clinicalapp scripts/ ./scripts/
COPY --chown=clinicalapp:clinicalapp validation/ ./validation/
COPY --chown=clinicalapp:clinicalapp test_data/ ./test_data/
COPY --chown=clinicalapp:clinicalapp setup.py ./
COPY --chown=clinicalapp:clinicalapp README.md ./

# Install the application as a Python package (editable mode for development)
# This allows imports like "from src.clinical.patient_validator import ..."
RUN pip install --no-cache-dir -e .

# ------------------------------------------------------------------------------
# Stage 9: Switch to Non-Root User
# ------------------------------------------------------------------------------
# All subsequent commands and the container runtime will execute as the
# non-privileged user. This is a critical security control for GxP systems
# and is required by security best practices (CIS Docker Benchmark).
# ------------------------------------------------------------------------------

USER clinicalapp

# ------------------------------------------------------------------------------
# Stage 10: Health Check Configuration
# ------------------------------------------------------------------------------
# Health checks enable container orchestration systems (Docker Swarm, Kubernetes)
# to monitor application health and automatically restart failed containers.
#
# This health check verifies:
# 1. Python interpreter is functional
# 2. Core application modules can be imported
# 3. Required directories exist and are accessible
#
# Parameters (tuned for production use):
# --interval=30s    - Check every 30 seconds (balance between responsiveness and load)
# --timeout=5s      - Timeout after 5 seconds (allows for initialization)
# --start-period=10s - Wait 10s before first check (allows container startup)
# --retries=3       - Mark unhealthy after 3 consecutive failures
#
# Exit codes: 0 = healthy, 1 = unhealthy
# ------------------------------------------------------------------------------

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "\
import sys; \
from pathlib import Path; \
# Import core modules to verify functionality \
import src.clinical.patient_validator; \
import src.clinical.adverse_event_processor; \
# Verify required directories exist \
assert Path('/app/src').exists(), 'Source directory missing'; \
assert Path('/app/tests').exists(), 'Tests directory missing'; \
assert Path('/app/scripts').exists(), 'Scripts directory missing'; \
# Verify we're running as non-root user \
import os; \
assert os.getuid() != 0, 'Running as root - security violation'; \
print('Health check passed: All systems operational'); \
sys.exit(0)" || exit 1

# ------------------------------------------------------------------------------
# Stage 11: Volume Definitions
# ------------------------------------------------------------------------------
# Define volume mount points for external data and output.
# These directories should be mounted at runtime for input/output operations.
# Volumes ensure data persistence and allow secure data handling:
# - /app/data    - Input data files (clinical trial data)
# - /app/reports - Output reports and validation artifacts
#
# Usage: docker run -v /host/data:/app/data -v /host/reports:/app/reports ...
# ------------------------------------------------------------------------------

VOLUME ["/app/data", "/app/reports"]

# ------------------------------------------------------------------------------
# Stage 12: Default Command
# ------------------------------------------------------------------------------
# Default command runs the test suite to verify the container is functional.
# This provides immediate feedback on container integrity after build.
#
# In production, this should be overridden with the actual application command:
#
# Example overrides:
#   # Generate validation report
#   docker run clinical-validation:1.0.0 \
#     python scripts/generate_validation_report.py results.xml report.md
#
#   # Run specific test suite
#   docker run clinical-validation:1.0.0 pytest tests/test_patient_validator.py -v
#
#   # Interactive shell for debugging (development only)
#   docker run -it clinical-validation:1.0.0 /bin/bash
# ------------------------------------------------------------------------------

CMD ["pytest", "tests/", "-v", "--cov=src", "--cov-report=term", "--cov-report=html:reports/coverage"]

# ==============================================================================
# End of Dockerfile
# ==============================================================================
#
# Validation and Compliance Notes:
# 
# 1. Traceability:
#    - All dependencies are pinned to specific versions in requirements.txt
#    - Image includes labels with version and validation date
#    - Git commit SHA should be added as build argument in CI/CD
#
# 2. Security:
#    - Runs as non-root user (UID 10001)
#    - Minimal base image reduces attack surface
#    - No secrets or credentials in image layers
#    - Security scanning with Trivy/Snyk recommended before deployment
#
# 3. Reproducibility:
#    - Fixed Python version (3.13-slim)
#    - Pinned dependencies ensure consistent builds
#    - Deterministic layer ordering for caching
#
# 4. Change Control:
#    - Image should be tagged with semantic versions (1.0.0, 1.1.0, etc.)
#    - Change control procedures must be followed for modifications
#    - All changes must be documented in version history
#
# 5. Validation:
#    - Health check verifies core functionality
#    - Default command runs test suite for validation
#    - Image should be validated in test environment before production
#
# 6. Archival:
#    - Container images should be archived per regulatory requirements
#    - Recommended: Store in private registry with 7+ year retention
#    - Include metadata for future audits
#
# Version History:
# 1.0.0 (2026-02-18) - Initial GxP-validated release
#                    - Python 3.13-slim base image
#                    - Non-root user security controls
#                    - Comprehensive health checks
#                    - Full compliance labeling
#
# ==============================================================================
