# Docker Setup - Quick Reference Guide

## Overview

This directory contains Docker configuration for the GxP-validated clinical trial data validation system. The containerized environment ensures reproducibility, security, and compliance with regulatory requirements.

## Files

- **Dockerfile** - Main image definition with Python 3.13-slim base
- **docker-compose.yml** - Multi-service orchestration configuration
- **../.dockerignore** - Build optimization (excludes unnecessary files)

## Quick Start

### Build the Image

```bash
# From project root
docker build -t clinical-validation:1.0.0 -f docker/Dockerfile .

# Or using docker-compose
docker-compose build
```

### Run Tests

```bash
# Run default command (test suite)
docker run --rm clinical-validation:1.0.0

# Using docker-compose
docker-compose up
```

### Interactive Shell

```bash
# For debugging
docker run -it --rm clinical-validation:1.0.0 /bin/bash

# Using docker-compose
docker-compose run --rm app /bin/bash
```

## Common Workflows

### 1. Development Testing

```bash
# Run specific test file
docker run --rm \
  -v $(pwd)/tests:/app/tests \
  clinical-validation:1.0.0 \
  pytest tests/test_patient_validator.py -v

# With docker-compose
docker-compose run --rm app pytest tests/test_patient_validator.py -v
```

### 2. Generate Validation Report

```bash
# Mount reports directory
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  clinical-validation:1.0.0 \
  python scripts/generate_validation_report.py \
    reports/test-results.xml \
    reports/validation-report.md \
    reports/coverage.json \
    $(git rev-parse HEAD)
```

### 3. Process Clinical Data

```bash
# Mount data and reports directories
docker run --rm \
  -v $(pwd)/data:/app/data:ro \
  -v $(pwd)/reports:/app/reports:rw \
  clinical-validation:1.0.0 \
  python -m src.clinical.adverse_event_processor /app/data/events.csv
```

## Security Features

### Non-Root User

Container runs as UID/GID 10001 (clinicalapp user):

```bash
# Verify
docker run --rm clinical-validation:1.0.0 id
# Output: uid=10001(clinicalapp) gid=10001(clinicalapp)
```

### Read-Only Root Filesystem

For maximum security in production:

```bash
docker run --rm --read-only \
  --tmpfs /tmp \
  --tmpfs /app/.pytest_cache \
  clinical-validation:1.0.0
```

### Health Checks

Built-in health monitoring:

```bash
# Check container health status
docker inspect clinical-validation:1.0.0 \
  --format='{{json .State.Health}}' | jq
```

## GxP Compliance

### Image Metadata

View compliance labels:

```bash
docker inspect clinical-validation:1.0.0 \
  --format='{{json .Config.Labels}}' | jq
```

Key labels:
- `compliance.standards` - Regulatory standards (21CFR11, EU Annex 11, etc.)
- `compliance.validated` - Validation status
- `compliance.validation-date` - Last validation date
- `gxp.system-type` - System classification
- `gxp.risk-category` - GAMP 5 category

### Traceability

```bash
# View image history and layers
docker history clinical-validation:1.0.0

# Export image for archival (7-year retention)
docker save clinical-validation:1.0.0 | gzip > clinical-validation-1.0.0.tar.gz
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Build Docker Image
  run: |
    docker build \
      -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
      -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest \
      -f docker/Dockerfile .

- name: Run Container Tests
  run: |
    docker run --rm \
      ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
      pytest tests/ -v --cov=src

- name: Scan for Vulnerabilities
  run: |
    docker run --rm \
      -v /var/run/docker.sock:/var/run/docker.sock \
      aquasec/trivy image \
      ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

## Troubleshooting

### Build Issues

**Problem**: "Permission denied" errors during build
```bash
# Ensure proper file permissions
chmod -R 755 src/ tests/ scripts/
```

**Problem**: Package installation fails
```bash
# Clear Docker build cache
docker builder prune -f
docker build --no-cache -f docker/Dockerfile .
```

### Runtime Issues

**Problem**: Tests fail in container but work locally
```bash
# Check Python version match
docker run --rm clinical-validation:1.0.0 python --version

# Compare dependencies
docker run --rm clinical-validation:1.0.0 pip list
```

**Problem**: Permission errors with mounted volumes
```bash
# Ensure host files are readable by UID 10001
chown -R 10001:10001 data/ reports/

# Or run with current user (less secure)
docker run --rm --user $(id -u):$(id -g) ...
```

### Health Check Failures

```bash
# View health check logs
docker inspect --format='{{json .State.Health}}' <container_id> | jq

# Run health check manually
docker exec <container_id> \
  python -c "import src.clinical.patient_validator; print('OK')"
```

## Performance Optimization

### Layer Caching

The Dockerfile is optimized for layer caching:
1. System dependencies (rarely changes)
2. Python dependencies (changes occasionally)
3. Application code (changes frequently)

### Multi-Stage Builds (Future Enhancement)

Consider multi-stage build for production:

```dockerfile
# Build stage
FROM python:3.13-slim AS builder
RUN pip install --user ...

# Production stage
FROM python:3.13-slim
COPY --from=builder /root/.local /root/.local
```

## Best Practices for Validated Environments

1. **Version Pinning**
   - Always use specific image tags (not `latest`)
   - Pin all dependencies in requirements.txt

2. **Image Registry**
   - Use private registry for validated images
   - Implement access controls (RBAC)
   - Enable vulnerability scanning

3. **Change Control**
   - Document all Dockerfile changes
   - Require approval for production images
   - Maintain version history

4. **Testing**
   - Test images in validation environment
   - Run full test suite before release
   - Verify security scan results

5. **Archival**
   - Export and archive validated images
   - Retain for regulatory period (7+ years)
   - Include metadata and documentation

## Additional Resources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [GAMP 5 Guide - Computerized Systems](https://ispe.org/publications/guidance-documents/gamp-5)
- [FDA Software Validation Guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-principles-software-validation)

## Version History

- **1.0.0** (2026-02-18) - Initial Docker configuration
  - Python 3.13-slim base image
  - Non-root user security
  - GxP compliance labels
  - Health check implementation
  - Docker Compose orchestration

---

*This Docker setup is part of the GxP-validated clinical trial data validation system and must be maintained under change control procedures.*
