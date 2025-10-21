Quick Start: Testing Workflows Locally
======================================

This is a quick 5-minute guide to get you started with testing GitHub
Actions workflows locally.

Why?
----

-  ✅ Test workflow changes before pushing
-  ✅ Debug failed workflows faster
-  ✅ Save CI/CD minutes
-  ✅ Work offline

Prerequisites
-------------

-  Docker installed and running
-  10GB+ free disk space

Installation (One Time)
-----------------------

Option 1: Use Our Script (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   ./scripts/setup_act.sh

This installs ``act`` (the GitHub Actions local runner) automatically.

Option 2: Manual Install
~~~~~~~~~~~~~~~~~~~~~~~~

**macOS:**

.. code:: bash

   brew install act

**Linux:**

.. code:: bash

   curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

**Windows:**

.. code:: powershell

   choco install act-cli

Basic Usage
-----------

1. List All Workflows
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   make workflow-list
   # or
   ./scripts/run_workflow.sh all

2. Run the CI Workflow
~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   make workflow-ci
   # or
   ./scripts/run_workflow.sh ci

The first time you run this, ``act`` will ask you to choose a Docker
image size:

-  Choose **Medium** (recommended for most cases)

3. Run a Specific Job
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Run only the lint job
   ./scripts/run_workflow.sh ci --job lint

   # Run only the test job
   ./scripts/run_workflow.sh ci --job test

4. Dry Run (See What Would Run)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   ./scripts/run_workflow.sh ci --dry-run

Common Workflows
----------------

.. code:: bash

   # Format and lint
   make workflow-lint

   # Run tests
   make workflow-test

   # Coverage report
   make workflow-coverage

   # Build executables
   make workflow-build

Tips
----

Speed Up Testing
~~~~~~~~~~~~~~~~

After the first run, containers are reused automatically (configured in
``.actrc``).

Debugging Failed Workflows
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Run with verbose output
   ./scripts/run_workflow.sh ci --verbose

   # List all jobs in a workflow
   ./scripts/run_workflow.sh ci --list-jobs

   # Run specific job that's failing
   ./scripts/run_workflow.sh ci --job test

Clean Up Docker Resources
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Remove old containers and images
   make clean-docker

   # Or manually
   docker system prune -a

What Gets Tested?
-----------------

When you run workflows locally:

-  ✅ Linting and formatting checks
-  ✅ Unit and integration tests
-  ✅ Code quality checks
-  ✅ Build processes
-  ⚠️ Some features won’t work (GitHub secrets, some actions)

Common Issues
-------------

“Cannot connect to Docker daemon”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Start Docker Desktop or the Docker daemon

.. code:: bash

   # Linux
   sudo systemctl start docker

   # macOS/Windows
   # Open Docker Desktop

“No space left on device”
~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Clean up Docker

.. code:: bash

   docker system prune -a

Workflow hangs or is slow
~~~~~~~~~~~~~~~~~~~~~~~~~

**First run:** Docker needs to download images (one-time, ~2GB)

**Subsequent runs:** Should be much faster with container reuse

Next Steps
----------

1. ✅ You’ve tested your first workflow!
2. Read the full guide: developers/guides/local_workflows (developers/guides/local_workflows)
3. Customize ``.actrc`` for your needs
4. Add secrets to ``.secrets`` (copy from ``.secrets.example``)

Example Workflow
----------------

Here’s a typical development workflow:

.. code:: bash

   # 1. Make code changes
   vim src/games_collection/games/card/poker/poker.py

   # 2. Test locally (fast feedback)
   make workflow-ci

   # 3. If it passes, commit and push
   git add .
   git commit -m "Add new feature"
   git push

   # 4. GitHub Actions runs automatically

Help
----

-  Full documentation: developers/guides/local_workflows (developers/guides/local_workflows)
-  act documentation: https://github.com/nektos/act
-  Issues: https://github.com/saint2706/Games/issues

Summary
-------

.. code:: bash

   # One-time setup
   ./scripts/setup_act.sh

   # Run workflows
   make workflow-ci              # Main CI workflow
   make workflow-lint            # Linting
   make workflow-test            # Tests
   ./scripts/run_workflow.sh all # List all workflows

   # Debugging
   ./scripts/run_workflow.sh ci --dry-run    # See what would run
   ./scripts/run_workflow.sh ci --list-jobs  # List jobs
   ./scripts/run_workflow.sh ci --job lint   # Run specific job

That’s it! You’re now running GitHub Actions locally. 🚀
