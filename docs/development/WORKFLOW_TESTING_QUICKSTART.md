# Workflow Testing Quickstart

Use this quick reference when you need to validate GitHub Actions workflows without running the entire CI pipeline:

1. **Format and lint only**
   ```bash
   ./scripts/run_workflow.sh lint
   ```

2. **Run unit tests**
   ```bash
   ./scripts/run_workflow.sh test
   ```

3. **Generate coverage reports**
   ```bash
   ./scripts/run_workflow.sh coverage
   ```

4. **Inspect workflow definitions**
   ```bash
   python scripts/validate_workflows.py
   ```

5. **List available workflows**
   ```bash
   ./scripts/run_workflow.sh all
   ```

6. **Inspect recent failed runs**
   ```bash
   python scripts/workflow_failures.py
   ```

Pair this sheet with `LOCAL_WORKFLOWS.md` for detailed explanations of each option and troubleshooting tips.
