GitHub Actions Workflows Documentation
======================================

This directory contains documentation related to GitHub Actions
workflows, validation, and maintenance. The most frequently used
references are listed below, while historical troubleshooting material
now lives in the archive overview (``operations/archive/overview``) subdirectory.

Documentation Files
-------------------

- **Validation report** (``operations/workflows/validation_report``) – Comprehensive status for every GitHub Actions workflow, covering results, payload validation, and referenced scripts.
- **Validation summary** (``operations/workflows/validation_summary``) – Overview of validation tooling, test suite highlights, and integration guidance.

Historical References
~~~~~~~~~~~~~~~~~~~~~

Need the deep-dive debug timelines or release remediation notes? Visit the archive overview (``operations/archive/overview``) for:

- ``operations/archive/debug_report`` – Detailed analysis of past CI failures.
- ``operations/archive/fix_summary`` – Point-in-time notes about workflow fixes.
- ``operations/archive/how_to_fix_v1_1_1`` – Recovery plan for the v1.1.1 release.
- ``operations/archive/pypi_publish_debug_run_18520989869`` – PyPI publish failure investigation.

Quick Reference
---------------

Validate Workflows
~~~~~~~~~~~~~~~~~~

.. code:: bash

   make workflow-validate
   # or
   python scripts/validate_workflows.py

Show Workflow Information
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   make workflow-info
   # or
   python scripts/workflow_info.py ci.yml -v

Run Workflow Tests
~~~~~~~~~~~~~~~~~~

.. code:: bash

   pytest tests/test_workflows.py -v

Run Workflows Locally
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Using act (requires installation)
   make workflow-ci
   make workflow-lint
   make workflow-test

Workflow Files
--------------

All workflow files are located in ``.github/workflows/``:

-  ``ci.yml`` - Continuous integration
-  ``format-and-lint.yml`` - Code formatting and linting
-  ``manual-tests.yml`` - Manual test execution
-  ``manual-coverage.yml`` - Manual coverage reporting
-  ``mutation-testing.yml`` - Mutation testing
-  ``build-executables.yml`` - Build standalone executables
-  ``codeql.yml`` - Code security scanning
-  ``publish-pypi.yml`` - PyPI package publishing
-  ``test-act-setup.yml`` - Local workflow testing setup

Event Payloads
--------------

Test event payloads for local workflow testing are in
``.github/workflows/events/``:

-  ``push.json`` - Mock push event
-  ``pull_request.json`` - Mock PR event
-  ``release.json`` - Mock release event
-  ``workflow_dispatch.json`` - Mock manual trigger event

Validation Tools
----------------

scripts/validate_workflows.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comprehensive validation script that checks:

-  YAML syntax
-  JSON payloads
-  Workflow structure
-  Script references
-  GitHub Actions versions
-  Documentation consistency

scripts/workflow_info.py
~~~~~~~~~~~~~~~~~~~~~~~~

Information display tool showing:

-  Trigger events
-  Required permissions
-  Environment variables
-  Jobs and dependencies
-  Actions used

Development Guides
------------------

For detailed guides on working with workflows:

-  Local Workflows Guide (developers/guides/local_workflows)
-  Workflow Testing
   Quickstart (developers/guides/workflow_testing_quickstart)
-  Workflow Validation Guide (developers/guides/workflow_validation)

scripts/check_version_consistency.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Version consistency validation script that checks:

-  Version in ``pyproject.toml``
-  Version in ``scripts/__init__.py``
-  Git tag version (optional)
-  Provides clear error messages
-  Used by CI to prevent version mismatches

Common Issues
-------------

PyPI Publishing Version Mismatch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:** ``File already exists on PyPI``

**Cause:** Git tag version doesn’t match code version

**Solution:**

.. code:: bash

   # Check version consistency
   python scripts/check_version_consistency.py --tag v1.2.3

   # Follow fix guide
   See: operations/archive/how_to_fix_v1_1_1

Markdown Formatting Failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:** ``mdformat --check failed``

**Solution:**

.. code:: bash

   mdformat .
   git add .
   git commit -m "fix: format markdown files"

Python Formatting Failures
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:** ``black --check failed``

**Solution:**

.. code:: bash

   black .
   git add .
   git commit -m "fix: format Python files"

Test Failures
~~~~~~~~~~~~~

**Error:** ``Tests failed``

**Solution:**

.. code:: bash

   pytest -v  # Run locally to identify issue
   # Fix the failing test
   git add .
   git commit -m "fix: resolve test failure"

Best Practices
--------------

1. **Always run pre-commit hooks** - ``pre-commit install``
2. **Test locally first** - ``make workflow-validate``
3. **Check formatting** - ``black .`` and ``mdformat .``
4. **Run tests** - ``pytest``
5. **Use validation tools** - ``python scripts/validate_workflows.py``

Related Documentation
---------------------

-  CI/CD
   Documentation (developers/guides/build_executables_workflow)
-  Testing Guide (developers/guides/testing)
-  Code Quality Standards (developers/guides/code_quality)
-  Contributing Guidelines (contributors/contributing)
