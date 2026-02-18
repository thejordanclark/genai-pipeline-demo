# GenAI Bootcamp - AI-Enhanced Pipeline Demo

This repository demonstrates AI-assisted CI/CD pipeline development for GxP-validated systems.

## Purpose
- Build validation-ready CI/CD pipelines using GitHub Copilot
- Automate compliance checks and evidence capture
- Demonstrate audit-ready pipeline practices

## Pipeline Components
1. **CI Pipeline** - Automated testing, linting, security scanning
2. **Validation Pipeline** - Evidence capture, compliance checks, approval gates
3. **Security Pipeline** - Dependency scanning, SAST, secrets detection

## Pipeline Features
- Automated testing with coverage thresholds
- Code quality gates (linting, formatting)
- Security scanning (dependencies, secrets, SAST)
- Validation evidence capture
- Approval workflows for production deployments
- Audit logging and traceability

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ --cov=src --cov-report=html

# Run linting
flake8 src/ tests/
black --check src/ tests/

# Run security scan
bandit -r src/
safety check
```

## Pipeline Execution

Pipelines run automatically on:

- **Push to master/develop** - Full CI + Validation pipeline
- **Pull requests** - CI pipeline only
- **Manual trigger** - Any pipeline with custom parameters

## Validation Evidence

All pipeline executions generate validation evidence:

- Test execution reports
- Coverage reports
- Security scan results
- Audit logs
- Approval records

Evidence is stored in GitHub Actions artifacts and logged in `validation/pipeline_execution_log.md`.

## Compliance Notes

- All pipeline changes require QA review
- Production deployments require dual approval
- Pipeline execution logs are retained per retention policy
- Failed pipelines block deployment
