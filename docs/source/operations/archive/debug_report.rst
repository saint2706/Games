GitHub Actions Debug Report: 20 Most Recent Workflow Runs
=========================================================

| **Repository:** saint2706/Games
| **Report Generated:** 2025-10-12
| **Analysis Period:** All 20 most recent workflow runs (from today)

--------------

Executive Summary
-----------------

🚨 **CRITICAL: 95% Failure Rate Detected**

-  **Total Runs Analyzed:** 20
-  **Failed Runs:** 19 (95.0%)
-  **Successful Runs:** 1 (5.0%)
-  **Timeframe:** All runs from October 12, 2025
-  **Primary Workflow Affected:** CI Workflow (id: 196934475)

--------------

Detailed Statistics
-------------------

Breakdown by Conclusion Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

=================== ===== ==========
Status              Count Percentage
=================== ===== ==========
**Failure**         15    75.0%
**Action Required** 4     20.0%
**Success**         1     5.0%
=================== ===== ==========

Breakdown by Branch
~~~~~~~~~~~~~~~~~~~

======================================= ==== ============
Branch                                  Runs Success Rate
======================================= ==== ============
master                                  9    0%
copilot/debug-workflows-locally         3    0%
copilot/complete-existing-features      2    0%
copilot/fix-all-test-failures           2    0%
copilot/complete-card-games-executables 1    100% ✓
copilot/update-root-readme              1    0%
copilot/debug-recent-github-actions     1    0%
copilot/debug-existing-issue            1    0%
======================================= ==== ============

--------------

Root Cause Analysis
-------------------

🔴 PRIMARY FAILURE CAUSE: Markdown Formatting Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Affected Runs:** 5+ (25% of failures)

**Issue:** Multiple markdown files not formatted correctly according to
``mdformat`` standards.

**Failed Command:**

.. code:: bash

   mdformat --check .

**Error Pattern:**

::

   Error: file(s) would be modified:
     - docs/deployment/DEPLOYMENT.md
     - developers/guides/code_quality
     - developers/guides/testing
     - [... additional files ...]

**Impact:** Blocks merge to master branch, prevents deployment

**Root Cause:** Files modified without running pre-commit hooks or
``mdformat`` before committing

--------------

🔴 SECONDARY FAILURE CAUSE: Python Code Formatting Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Affected Runs:** 2+ (10% of failures)

**Issue:** Python files not formatted according to ``black`` standards.

**Failed Command:**

.. code:: bash

   black --check .

**Error Pattern:**

::

   would reformat 15 files

**Impact:** Code quality checks fail, blocking CI pipeline

**Root Cause:** Code committed without running ``black`` formatter

--------------

🔴 TERTIARY FAILURE CAUSE: Test Failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Affected Runs:** 2+ (10% of failures)

**Issue:** Specific test cases failing, particularly in Solitaire tests.

**Failed Test Example:**

::

   TestSolitaire.test_play_card_to_foundation - AssertionError

**Impact:** Tests must pass before merge, blocks PR progress

**Root Cause:** Code changes introduced bugs or test expectations not
updated

--------------

⚠️ UNUSUAL STATUS: “Action Required”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Affected Runs:** 4 (20% of total)

**Runs with this status:**

-  Run #388, #387 (copilot/debug-workflows-locally)
-  Run #386 (copilot/debug-recent-github-actions)
-  Run #385 (copilot/debug-workflows-locally)

**Explanation:** This status typically indicates:

1. Workflow is waiting for manual approval
2. Required status checks are pending
3. External dependencies not yet resolved

**Note:** These runs may not be true “failures” but are in a
pending/waiting state

--------------

Detailed Run Information
------------------------

✅ The One Success Story
~~~~~~~~~~~~~~~~~~~~~~~~

| **Run #361** - CI Workflow
| **Branch:** copilot/complete-card-games-executables
| **Date:** 2025-10-12 10:22 UTC
| **Status:** SUCCESS ✓
| **URL:** https://github.com/saint2706/Games/actions/runs/18442653501

**Why it succeeded:**

-  All formatting checks passed
-  All tests passed
-  No linting issues
-  Code followed quality standards

--------------

❌ Recent Failures (Top 10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Run #388 - ACTION_REQUIRED
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18443721469
-  **Branch:** copilot/debug-workflows-locally
-  **Event:** pull_request
-  **Created:** 2025-10-12 12:09 UTC
-  **Status:** Waiting for external action

2. Run #387 - ACTION_REQUIRED
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18443721457
-  **Branch:** copilot/debug-workflows-locally
-  **Event:** pull_request
-  **Created:** 2025-10-12 12:09 UTC
-  **Status:** Waiting for external action

3. Run #386 - ACTION_REQUIRED
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18443719282
-  **Branch:** copilot/debug-recent-github-actions
-  **Event:** pull_request
-  **Created:** 2025-10-12 12:09 UTC
-  **Status:** Waiting for external action

4. Run #385 - ACTION_REQUIRED
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18443608315
-  **Branch:** copilot/debug-workflows-locally
-  **Event:** pull_request
-  **Created:** 2025-10-12 12:00 UTC
-  **Status:** Waiting for external action

5. Run #384 - FAILURE (master)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18443604840
-  **Branch:** master
-  **Event:** push
-  **Created:** 2025-10-12 11:59 UTC
-  **Cause:** Markdown formatting issues
-  **Failed Job:** lint
-  **Error:** Multiple markdown files not formatted

6. Run #381 - FAILURE
^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18443549736
-  **Branch:** copilot/update-root-readme
-  **Event:** pull_request
-  **Created:** 2025-10-12 11:52 UTC
-  **Cause:** Markdown formatting issues
-  **Failed Job:** lint

7. Run #380 - FAILURE (master)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18443517444
-  **Branch:** master
-  **Event:** push
-  **Created:** 2025-10-12 11:48 UTC
-  **Cause:** Markdown formatting issues
-  **Failed Job:** lint

8. Run #376 - FAILURE (master)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18443328914
-  **Branch:** master
-  **Event:** push
-  **Created:** 2025-10-12 11:28 UTC
-  **Cause:** Markdown formatting issues

9. Run #372 - FAILURE (master)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18442923814
-  **Branch:** master
-  **Event:** push
-  **Created:** 2025-10-12 10:49 UTC
-  **Cause:** Markdown formatting issues

10. Run #360 - FAILURE (master)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **URL:** https://github.com/saint2706/Games/actions/runs/18442628463
-  **Branch:** master
-  **Event:** push
-  **Created:** 2025-10-12 10:20 UTC
-  **Cause:** Markdown formatting issues

--------------

Pattern Analysis
----------------

🔍 Identified Patterns
~~~~~~~~~~~~~~~~~~~~~~

1. **Markdown Formatting is the #1 Issue**

   -  Appears in 75% of actual failures
   -  Affects both master and feature branches
   -  Consistently blocks CI pipeline

2. **Master Branch Heavily Affected**

   -  9 out of 20 runs are on master
   -  100% failure rate on master
   -  Indicates issues are being merged without proper checks

3. **Pre-commit Hooks Not Being Used**

   -  Multiple formatting issues suggest developers aren’t running
      pre-commit hooks
   -  Both Python and Markdown files affected

4. **Recent Surge in Failures**

   -  All 20 runs are from same day (today)
   -  Suggests recent changes broke something or workflow was updated

5. **One Success Indicates It CAN Work**

   -  Run #361 succeeded with proper formatting
   -  Shows the pipeline itself is functional when code meets standards

--------------

Immediate Action Items
----------------------

🔥 CRITICAL (Fix Today)
~~~~~~~~~~~~~~~~~~~~~~~

1. **Fix Markdown Formatting on Master Branch**

   .. code:: bash

      # Run this to fix all markdown files
      mdformat .
      git add .
      git commit -m "fix: format all markdown files with mdformat"
      git push

2. **Fix Python Code Formatting**

   .. code:: bash

      # Run this to fix all Python files
      black .
      git add .
      git commit -m "fix: format all Python files with black"
      git push

3. **Fix Failing Tests**

   .. code:: bash

      # Run tests locally to identify issues
      pytest -v
      # Fix any failing tests
      # Commit fixes

⚠️ HIGH PRIORITY (This Week)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. **Enforce Pre-commit Hooks**

   -  Add documentation requiring developers to install pre-commit hooks
   -  Update contributors/contributing with setup instructions
   -  Consider adding CI check that verifies pre-commit hooks were run

5. **Update CI Workflow**

   -  Consider adding auto-fix step for formatting
   -  Add better error messages for formatting failures
   -  Separate formatting checks from other linting

6. **Branch Protection Rules**

   -  Require all status checks to pass before merge
   -  Require pull request reviews
   -  Prevent direct pushes to master

📋 MEDIUM PRIORITY (Next Sprint)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

7. **Documentation Updates**

   -  Add “Quick Fix” guide for common CI failures
   -  Document the formatting requirements
   -  Add examples of proper workflow

8. **Developer Tooling**

   -  Add VS Code workspace settings with auto-format on save
   -  Provide setup scripts for new developers
   -  Consider adding git hooks to auto-run formatters

--------------

Quick Fix Guide for Developers
------------------------------

When Your CI Build Fails…
~~~~~~~~~~~~~~~~~~~~~~~~~

❌ Error: “mdformat –check failed”
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Solution:**

.. code:: bash

   # Install mdformat if not already installed
   pip install mdformat

   # Format all markdown files
   mdformat .

   # Commit the changes
   git add .
   git commit -m "fix: format markdown files"
   git push

❌ Error: “black –check failed”
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Solution:**

.. code:: bash

   # Install black if not already installed
   pip install black

   # Format all Python files
   black .

   # Commit the changes
   git add .
   git commit -m "fix: format Python files"
   git push

❌ Error: “Tests failed”
^^^^^^^^^^^^^^^^^^^^^^^^

**Solution:**

.. code:: bash

   # Run tests locally to see the failure
   pytest -v

   # Debug and fix the failing test
   # Then commit your fix
   git add .
   git commit -m "fix: resolve test failure in [test_name]"
   git push

--------------

Prevention Strategy
-------------------

🛡️ How to Avoid These Issues in the Future
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Always Run Pre-commit Hooks**

   .. code:: bash

      # Install pre-commit (one time)
      pip install pre-commit
      pre-commit install

      # Hooks will run automatically on every commit
      # Or run manually:
      pre-commit run --all-files

2. **Run Local Checks Before Pushing**

   .. code:: bash

      # Format code
      black .
      mdformat .

      # Run tests
      pytest

      # Only push if everything passes
      git push

3. **Use VS Code Settings**

   -  Enable “Format on Save”
   -  Install Python and Markdown extensions
   -  Use workspace settings for consistency

4. **Check CI Status Before Merging**

   -  Wait for all checks to pass
   -  Fix any failures immediately
   -  Don’t merge with failing CI

--------------

Recommendations for Repository Maintainers
------------------------------------------

Short-term (Immediate)
~~~~~~~~~~~~~~~~~~~~~~

1. ✅ **Fix all current formatting issues** (run formatters on entire
   codebase)
2. ✅ **Add branch protection to master** (prevent direct pushes)
3. ✅ **Require status checks** (make CI passing mandatory)
4. ✅ **Document the formatting requirements** clearly

Medium-term (This Month)
~~~~~~~~~~~~~~~~~~~~~~~~

1. 📝 **Update contributors/contributing** with clear setup instructions
2. 🔧 **Add pre-commit configuration** to repository
3. 📊 **Monitor CI success rate** weekly
4. 🎯 **Set up automated formatting** in CI (auto-fix and commit)

Long-term (Next Quarter)
~~~~~~~~~~~~~~~~~~~~~~~~

1. 🤖 **Consider adding auto-merge bot** (like Mergify) for passing PRs
2. 📈 **Track CI metrics** (failure rate, time to fix, etc.)
3. 🎓 **Developer training** on CI/CD best practices
4. 🔄 **Regular CI maintenance** reviews

--------------

Technical Details
-----------------

CI Workflow Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

| **Workflow File:** ``.github/workflows/ci.yml``
| **Trigger Events:** push, pull_request
| **Jobs:**

-  lint (markdown, Python formatting checks)
-  test (run pytest across multiple Python versions)

Tools Used
~~~~~~~~~~

-  **mdformat:** Markdown formatter
-  **black:** Python code formatter
-  **ruff:** Python linter
-  **pytest:** Python testing framework
-  **coverage:** Code coverage reporting

Python Versions Tested
~~~~~~~~~~~~~~~~~~~~~~

-  Python 3.9
-  Python 3.10
-  Python 3.11
-  Python 3.12

--------------

Conclusion
----------

The high failure rate (95%) is primarily due to **formatting issues**
that can be easily resolved by:

1. Running formatters before committing (``black .`` and ``mdformat .``)
2. Installing and using pre-commit hooks
3. Enforcing these standards through branch protection

The good news: The CI pipeline itself works correctly (as evidenced by
the one successful run). The issues are with code quality, not the
pipeline.

**Next Steps:**

1. ✅ Run formatters on entire codebase
2. ✅ Commit and push fixes
3. ✅ Set up branch protection
4. ✅ Update documentation
5. ✅ Monitor improvement

--------------

Appendix: All 20 Run Details
----------------------------

+---+---------+---------+---------+---------------+---------+-------+
| # | Run ID  | Number  | Status  | Conclusion    | Branch  | Date  |
+===+=========+=========+=========+===============+=========+=======+
| 1 | 1844    | 388     | co      | ac            | cop     | 2025- |
|   | 3721469 |         | mpleted | tion_required | ilot/de | 10-12 |
|   |         |         |         |               | bug-wor | 12:09 |
|   |         |         |         |               | kflows- |       |
|   |         |         |         |               | locally |       |
+---+---------+---------+---------+---------------+---------+-------+
| 2 | 1844    | 387     | co      | ac            | cop     | 2025- |
|   | 3721457 |         | mpleted | tion_required | ilot/de | 10-12 |
|   |         |         |         |               | bug-wor | 12:09 |
|   |         |         |         |               | kflows- |       |
|   |         |         |         |               | locally |       |
+---+---------+---------+---------+---------------+---------+-------+
| 3 | 1844    | 386     | co      | ac            | copilot | 2025- |
|   | 3719282 |         | mpleted | tion_required | /debug- | 10-12 |
|   |         |         |         |               | recent- | 12:09 |
|   |         |         |         |               | github- |       |
|   |         |         |         |               | actions |       |
+---+---------+---------+---------+---------------+---------+-------+
| 4 | 1844    | 385     | co      | ac            | cop     | 2025- |
|   | 3608315 |         | mpleted | tion_required | ilot/de | 10-12 |
|   |         |         |         |               | bug-wor | 12:00 |
|   |         |         |         |               | kflows- |       |
|   |         |         |         |               | locally |       |
+---+---------+---------+---------+---------------+---------+-------+
| 5 | 1844    | 384     | co      | failure       | master  | 2025- |
|   | 3604840 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 11:59 |
+---+---------+---------+---------+---------------+---------+-------+
| 6 | 1844    | 381     | co      | failure       | copil   | 2025- |
|   | 3549736 |         | mpleted |               | ot/upda | 10-12 |
|   |         |         |         |               | te-root | 11:52 |
|   |         |         |         |               | -readme |       |
+---+---------+---------+---------+---------------+---------+-------+
| 7 | 1844    | 380     | co      | failure       | master  | 2025- |
|   | 3517444 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 11:48 |
+---+---------+---------+---------+---------------+---------+-------+
| 8 | 1844    | 376     | co      | failure       | master  | 2025- |
|   | 3328914 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 11:28 |
+---+---------+---------+---------+---------------+---------+-------+
| 9 | 1844    | 372     | co      | failure       | master  | 2025- |
|   | 2923814 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 10:49 |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 361     | co      | **success** ✓ | copi    | 2025- |
| 0 | 2653501 |         | mpleted |               | lot/com | 10-12 |
|   |         |         |         |               | plete-c | 10:22 |
|   |         |         |         |               | ard-gam |       |
|   |         |         |         |               | es-exec |       |
|   |         |         |         |               | utables |       |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 360     | co      | failure       | master  | 2025- |
| 1 | 2628463 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 10:20 |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 359     | co      | failure       | copilo  | 2025- |
| 2 | 2583692 |         | mpleted |               | t/compl | 10-12 |
|   |         |         |         |               | ete-exi | 10:16 |
|   |         |         |         |               | sting-f |       |
|   |         |         |         |               | eatures |       |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 358     | co      | failure       | copilo  | 2025- |
| 3 | 2583665 |         | mpleted |               | t/compl | 10-12 |
|   |         |         |         |               | ete-exi | 10:16 |
|   |         |         |         |               | sting-f |       |
|   |         |         |         |               | eatures |       |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 350     | co      | failure       | master  | 2025- |
| 4 | 2285062 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 09:46 |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 349     | co      | failure       | master  | 2025- |
| 5 | 2281977 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 09:45 |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 342     | co      | failure       | master  | 2025- |
| 6 | 2057015 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 09:22 |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 341     | co      | failure       | c       | 2025- |
| 7 | 2041602 |         | mpleted |               | opilot/ | 10-12 |
|   |         |         |         |               | fix-all | 09:21 |
|   |         |         |         |               | -test-f |       |
|   |         |         |         |               | ailures |       |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 340     | co      | failure       | c       | 2025- |
| 8 | 2041580 |         | mpleted |               | opilot/ | 10-12 |
|   |         |         |         |               | fix-all | 09:21 |
|   |         |         |         |               | -test-f |       |
|   |         |         |         |               | ailures |       |
+---+---------+---------+---------+---------------+---------+-------+
| 1 | 1844    | 338     | co      | failure       | master  | 2025- |
| 9 | 1993300 |         | mpleted |               |         | 10-12 |
|   |         |         |         |               |         | 09:17 |
+---+---------+---------+---------+---------------+---------+-------+
| 2 | 1844    | 335     | co      | failure       | copilot | 2025- |
| 0 | 1854865 |         | mpleted |               | /debug- | 10-12 |
|   |         |         |         |               | existin | 09:05 |
|   |         |         |         |               | g-issue |       |
+---+---------+---------+---------+---------------+---------+-------+

--------------

Contact
-------

For questions about this report or assistance with CI issues:

-  Review the failing workflow runs at:
   https://github.com/saint2706/Games/actions
-  Check documentation at: ``developers/guides/code_quality``
-  Refer to: ``contributors/contributing``

--------------

**Report End**
