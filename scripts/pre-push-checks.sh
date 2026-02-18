#!/usr/bin/env bash
#
# pre-push-checks.sh
# Run all CI quality checks locally before pushing code
#
# Usage: ./scripts/pre-push-checks.sh
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MIN_COVERAGE=80
REPORTS_DIR="reports"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  GxP Pre-Push Quality Checks${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Create reports directory
mkdir -p ${REPORTS_DIR}/coverage
mkdir -p ${REPORTS_DIR}/security

# Check 1: Code Formatting
echo -e "${YELLOW}[1/5] Checking code formatting with Black...${NC}"
if devbox run -- black --check src/ tests/; then
    echo -e "${GREEN}✓ Code formatting passed${NC}"
else
    echo -e "${RED}✗ Code formatting failed${NC}"
    echo -e "${YELLOW}Run 'devbox run -- black src/ tests/' to fix${NC}"
    exit 1
fi
echo ""

# Check 2: Linting
echo -e "${YELLOW}[2/5] Running flake8 linting...${NC}"
if devbox run -- flake8 src/ tests/ \
    --max-line-length=100 \
    --exclude=__pycache__,.git,__init__.py \
    --statistics; then
    echo -e "${GREEN}✓ Linting passed${NC}"
else
    echo -e "${RED}✗ Linting failed${NC}"
    exit 1
fi
echo ""

# Check 3: Security Scanning
echo -e "${YELLOW}[3/5] Running Bandit security scan...${NC}"
if devbox run -- bandit -r src/ \
    -f txt \
    -o ${REPORTS_DIR}/security/bandit_report.txt \
    -ll; then
    echo -e "${GREEN}✓ Security scan passed (no high severity issues)${NC}"
else
    echo -e "${RED}✗ High severity security issues found!${NC}"
    cat ${REPORTS_DIR}/security/bandit_report.txt
    exit 1
fi
echo ""

echo -e "${YELLOW}[4/5] Checking dependency vulnerabilities with Safety...${NC}"
devbox run -- safety check \
    --output ${REPORTS_DIR}/security/safety_report.txt \
    --continue-on-error || true
echo -e "${YELLOW}⚠  Safety check completed (warnings logged)${NC}"
echo ""

# Check 5: Tests with Coverage
echo -e "${YELLOW}[5/5] Running tests with coverage...${NC}"
if devbox run -- pytest tests/ \
    --verbose \
    --tb=short \
    --cov=src \
    --cov-report=html:${REPORTS_DIR}/coverage \
    --cov-report=term-missing \
    --cov-report=xml:${REPORTS_DIR}/coverage.xml \
    --html=${REPORTS_DIR}/test_report.html \
    --self-contained-html; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
    exit 1
fi
echo ""

# Check coverage threshold
echo -e "${YELLOW}Checking coverage threshold (minimum ${MIN_COVERAGE}%)...${NC}"
coverage_percent=$(python -c "import xml.etree.ElementTree as ET; tree = ET.parse('${REPORTS_DIR}/coverage.xml'); root = tree.getroot(); print(f'{float(root.attrib[\"line-rate\"]) * 100:.1f}')")

if (( $(echo "$coverage_percent < $MIN_COVERAGE" | bc -l) )); then
    echo -e "${RED}✗ Coverage ${coverage_percent}% is below required threshold of ${MIN_COVERAGE}%${NC}"
    echo -e "${YELLOW}Open ${REPORTS_DIR}/coverage/index.html to see uncovered lines${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Coverage ${coverage_percent}% meets required threshold${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ All quality checks passed!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Reports generated:"
echo "  • Test report:     ${REPORTS_DIR}/test_report.html"
echo "  • Coverage report: ${REPORTS_DIR}/coverage/index.html"
echo "  • Security report: ${REPORTS_DIR}/security/bandit_report.txt"
echo ""
echo -e "${GREEN}You're ready to push your code!${NC}"
