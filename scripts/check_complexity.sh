#!/bin/bash
# Code complexity analysis script
# This script uses radon to analyze code complexity and generate reports

set -e

echo "=== Code Complexity Analysis ==="
echo ""

# Check if radon is installed
if ! command -v radon &> /dev/null; then
    echo "radon is not installed. Installing..."
    pip install radon
fi

echo "Analyzing cyclomatic complexity..."
echo "Files with complexity > 10 (moderate complexity or higher):"
radon cc . -a -s -n B --exclude="tests/*,colorama/*"

echo ""
echo "Analyzing maintainability index..."
echo "Files with maintainability < 20 (low maintainability):"
radon mi . -s -n B --exclude="tests/*,colorama/*"

echo ""
echo "=== Summary ==="
echo "Cyclomatic Complexity (CC) Ratings:"
echo "  A: 1-5   (simple, low risk)"
echo "  B: 6-10  (moderate complexity)"
echo "  C: 11-20 (moderate to high complexity)"
echo "  D: 21-30 (high complexity)"
echo "  E: 31-40 (very high complexity)"
echo "  F: 41+   (extremely high complexity)"
echo ""
echo "Maintainability Index (MI) Ratings:"
echo "  A: 20-100 (highly maintainable)"
echo "  B: 10-19  (moderately maintainable)"
echo "  C: 0-9    (difficult to maintain)"
