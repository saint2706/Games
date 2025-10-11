#!/bin/bash
# Script to run tests locally with various options

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Games Project Test Runner${NC}"
echo "=============================="
echo ""

# Parse arguments
TEST_TYPE="${1:-all}"
COVERAGE="${2:-no}"

case "$TEST_TYPE" in
  "all")
    echo -e "${GREEN}Running all tests...${NC}"
    if [ "$COVERAGE" = "coverage" ]; then
      python -m pytest tests/ -v --cov=paper_games --cov=card_games --cov-report=html --cov-report=term-missing
    else
      python -m pytest tests/ -v
    fi
    ;;
  
  "unit")
    echo -e "${GREEN}Running unit tests...${NC}"
    python -m pytest tests/ -v -m unit
    ;;
  
  "integration")
    echo -e "${GREEN}Running integration tests...${NC}"
    python -m pytest tests/ -v -m integration
    ;;
  
  "gui")
    echo -e "${GREEN}Running GUI tests...${NC}"
    python -m pytest tests/ -v -m gui
    ;;
  
  "performance")
    echo -e "${GREEN}Running performance tests...${NC}"
    python -m pytest tests/ -v -m performance
    ;;
  
  "fast")
    echo -e "${GREEN}Running fast tests (excluding slow tests)...${NC}"
    python -m pytest tests/ -v -m "not slow"
    ;;
  
  "coverage")
    echo -e "${GREEN}Running tests with coverage report...${NC}"
    python -m pytest tests/ -v \
      --cov=paper_games \
      --cov=card_games \
      --cov-report=html \
      --cov-report=term-missing \
      -m "not slow"
    echo ""
    echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
    ;;
  
  "mutation")
    echo -e "${GREEN}Running mutation tests (this may take a while)...${NC}"
    mutmut run --paths-to-mutate paper_games/nim/,paper_games/tic_tac_toe/
    mutmut results
    echo ""
    echo "Run 'mutmut html' to generate HTML report"
    ;;
  
  "help"|"-h"|"--help")
    echo "Usage: $0 [test_type] [coverage]"
    echo ""
    echo "Test types:"
    echo "  all         - Run all tests (default)"
    echo "  unit        - Run only unit tests"
    echo "  integration - Run only integration tests"
    echo "  gui         - Run only GUI tests"
    echo "  performance - Run only performance tests"
    echo "  fast        - Run tests excluding slow tests"
    echo "  coverage    - Run tests with coverage report"
    echo "  mutation    - Run mutation testing"
    echo "  help        - Show this help message"
    echo ""
    echo "Coverage option (for 'all' test type):"
    echo "  coverage    - Generate coverage report"
    echo ""
    echo "Examples:"
    echo "  $0                      # Run all tests"
    echo "  $0 all coverage         # Run all tests with coverage"
    echo "  $0 fast                 # Run fast tests only"
    echo "  $0 integration          # Run integration tests"
    echo "  $0 coverage             # Generate coverage report"
    echo "  $0 mutation             # Run mutation testing"
    exit 0
    ;;
  
  *)
    echo -e "${RED}Unknown test type: $TEST_TYPE${NC}"
    echo "Run '$0 help' for usage information"
    exit 1
    ;;
esac

echo ""
echo -e "${GREEN}Tests complete!${NC}"
