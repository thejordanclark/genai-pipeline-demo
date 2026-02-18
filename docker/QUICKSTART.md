# Docker Compose Quick Start Guide

## Overview

The docker-compose.yml has been enhanced to support a complete development and validation workflow with separate services for different tasks.

## Services

### 1. **app** - Main Application Service
- **Purpose**: Long-running application container for development
- **Features**:
  - Mounts local source code (`src/`, `tests/`, `scripts/`) for live editing
  - Exposes ports 8000 and 8080 for future API/web interface
  - Stays running with `tail -f /dev/null` for interactive access
  - Includes comprehensive environment variables
- **Command**: `docker-compose up -d app`

### 2. **test** - Test Runner Service
- **Purpose**: Dedicated service for running test suite
- **Features**:
  - Runs pytest with coverage reports
  - Generates HTML, JSON, and XML reports
  - Outputs to named volume `validation-reports`
  - Exits after completion
- **Command**: `docker-compose run --rm test`

### 3. **validator** - Validation Report Generator
- **Purpose**: Generates GxP validation reports from test results
- **Features**:
  - Creates validation report from JUnit XML
  - Generates audit logs
  - Checks for test results before running
  - Includes timestamp in output files
- **Command**: `docker-compose run --rm validator`

## Complete Workflow

### Development Workflow
```bash
# 1. Start the application container
cd docker
docker-compose up -d app

# 2. View logs
docker-compose logs -f app

# 3. Access interactive shell
docker exec -it clinical-validation-app /bin/bash

# 4. Edit code locally - changes are immediately available in container
# (Edit files in src/, tests/, scripts/)

# 5. Run tests
docker-compose run --rm test

# 6. Generate validation report
docker-compose run --rm validator

# 7. Stop everything
docker-compose down
```

### CI/CD Simulation
```bash
# Complete validation workflow
cd docker
docker-compose build --no-cache
docker-compose run --rm test
docker-compose run --rm validator
docker-compose up -d app
docker-compose logs app
```

## Volume Mounts

### Development (Live Code Editing)
- `../src:/app/src:rw` - Source code (read-write)
- `../tests:/app/tests:rw` - Test files (read-write)
- `../scripts:/app/scripts:rw` - Utility scripts (read-write)

### Data & Reports
- `../data:/app/data:ro` - Input data (read-only)
- `validation-reports:/app/reports:rw` - Output reports (named volume)
- `../validation:/app/validation:rw` - Validation logs
- `../test_data:/app/test_data:ro` - Test data (read-only)

## Environment Variables

All services include comprehensive environment variables:

### Application (`app`)
- `APP_ENV=development`
- `APP_VERSION=1.0.0`
- `LOG_LEVEL=INFO`
- `DATA_DIR=/app/data`
- `REPORTS_DIR=/app/reports`
- `ENABLE_API=false`
- `GXP_VALIDATION_MODE=development`
- `AUDIT_LOGGING=true`

### Test (`test`)
- `APP_ENV=test`
- `LOG_LEVEL=DEBUG`
- `PYTEST_CURRENT_TEST=true`

### Validator (`validator`)
- `APP_ENV=validation`
- `GXP_VALIDATION_MODE=production`

## Exposed Ports

The `app` service exposes:
- **8000**: Main application port (for future API)
- **8080**: Alternative/admin port

Access via: `http://localhost:8000`

## Common Commands

### View Reports
```bash
# List generated reports
docker-compose run --rm app ls -la reports/

# Copy reports to host
docker cp clinical-validation-app:/app/reports ./local-reports

# View coverage report
open reports/coverage/index.html  # macOS
```

### Troubleshooting
```bash
# Rebuild image
docker-compose build --no-cache

# View service logs
docker-compose logs -f app
docker-compose logs test

# Clean everything
docker-compose down -v
docker system prune -f

# Verify configuration
docker-compose config --services
docker-compose config --quiet && echo "✅ Valid"
```

### Running Specific Tests
```bash
# Run specific test file
docker-compose run --rm test pytest tests/test_patient_validator.py -v

# Run with specific markers
docker-compose run --rm test pytest -m "not slow" -v

# Run with additional options
docker-compose run --rm test pytest tests/ -v --tb=short
```

## Environment File

An `.env.example` file has been created with all available environment variables. To use:

```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your values
nano .env

# Docker Compose will automatically load .env
docker-compose up -d app
```

## Security Notes

- All services run as non-root user (UID 10001)
- Resource limits prevent resource exhaustion (2GB RAM, 2 CPUs max)
- Source code mounted read-only in test and validator services
- Data directory mounted read-only for integrity
- Temporary filesystems for `/tmp` and pytest cache

## GxP Compliance

The setup includes:
- Audit logging enabled (`AUDIT_LOGGING=true`)
- Validation mode tracking (`GXP_VALIDATION_MODE`)
- Comprehensive environment variable documentation
- Named volumes with retention labels (7 years)
- Traceable configuration through labels

## File Structure

```
genai-pipeline-demo/
├── docker/
│   ├── Dockerfile              # Image definition
│   ├── docker-compose.yml      # Service orchestration
│   └── README.md              # Detailed documentation
├── .dockerignore              # Build optimization
├── .env.example               # Environment variables template
├── data/                      # Input data (mounted)
├── reports/                   # Output reports (named volume)
├── validation/                # Validation logs (mounted)
└── test_data/                 # Test datasets (mounted)
```

## Next Steps

1. **Copy environment file**: `cp .env.example .env`
2. **Build image**: `cd docker && docker-compose build`
3. **Run tests**: `docker-compose run --rm test`
4. **Generate validation report**: `docker-compose run --rm validator`
5. **Start development**: `docker-compose up -d app`

---

*For detailed information, see `docker/README.md` and inline documentation in the docker-compose.yml file.*
