PyPI Publish Workflow Debug Report
==================================

| **Workflow Run:** #18520989869
| **Workflow:** Publish to PyPI
| **Status:** ❌ Failed
| **Date:** 2025-10-15 07:18 UTC
| **URL:** https://github.com/saint2706/Games/actions/runs/18520989869

--------------

Executive Summary
-----------------

The PyPI publish workflow failed during the “Publish to PyPI” step
because it attempted to upload a package version that already exists on
PyPI. This occurred due to a **version mismatch** between the Git tag
(v1.1.1) and the actual version in the code (1.0.1).

**Root Cause:** The release tag v1.1.1 was created pointing to a commit
where ``pyproject.toml`` contained version 1.0.1, not 1.1.1.

--------------

Detailed Analysis
-----------------

What Happened
~~~~~~~~~~~~~

1. **Release Created:** A GitHub release v1.1.1 was published on
   2025-10-15

2. **Workflow Triggered:** The ``publish-pypi.yml`` workflow was
   triggered by the release event

3. **Build Job Succeeded:** Built packages from the v1.1.1 tag

4. **Version Mismatch:** The v1.1.1 tag pointed to commit ``42ba227``
   which has version 1.0.1 in ``pyproject.toml``

5. **Build Output:** Created ``games_collection-1.0.1-py3-none-any.whl``
   and ``games_collection-1.0.1.tar.gz``

6. **PyPI Upload Failed:** PyPI rejected the upload with error:

   ::

      HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/
      File already exists ('games_collection-1.0.1-py3-none-any.whl', ...)

Job Details
~~~~~~~~~~~

✅ Build Job (Succeeded)
^^^^^^^^^^^^^^^^^^^^^^^^

-  **Job ID:** 52780695294
-  **Duration:** 26 seconds
-  **Steps:**

   -  Checked out repository ✓
   -  Built distribution packages ✓
   -  Created: ``games_collection-1.0.1.tar.gz`` and
      ``games_collection-1.0.1-py3-none-any.whl``
   -  Uploaded artifacts ✓

❌ Publish to PyPI Job (Failed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **Job ID:** 52780729147

-  **Duration:** 21 seconds

-  **Error:**

   ::

      ERROR   HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/
              File already exists ('games_collection-1.0.1-py3-none-any.whl', with
              blake2_256 hash
              'd38e2b65cf9355690e94bd122676ac22094075f949acce77fef085dc65577ca9').
              See https://pypi.org/help/#file-name-reuse for more information.

Version Analysis
~~~~~~~~~~~~~~~~

+----------------------------+------+-----------------------------------+
| Location                   | Ver  | Commit                            |
|                            | sion |                                   |
+============================+======+===================================+
| Tag v1.1.1                 | N/A  | Points to commit ``42ba227``      |
+----------------------------+------+-----------------------------------+
| pyproject.toml @ v1.1.1    | 1    | ❌ Mismatch!                      |
| tag                        | .0.1 |                                   |
+----------------------------+------+-----------------------------------+
| scripts/\__init\_\_.py @   | 1    | ❌ Mismatch!                      |
| tag                        | .0.1 |                                   |
+----------------------------+------+-----------------------------------+
| PyPI Current Version       | 1    | ❌ Already exists!                |
|                            | .0.1 |                                   |
+----------------------------+------+-----------------------------------+
| pyproject.toml @ master    | 1    | Latest development version        |
|                            | .1.0 |                                   |
+----------------------------+------+-----------------------------------+
| Expected for v1.1.1        | 1    | ❌ Tag and code versions don’t    |
|                            | .1.1 | align                             |
+----------------------------+------+-----------------------------------+

--------------

Root Cause
----------

The release was created **manually** without following the proper
version bump process. The correct workflow is:

1. Run workflow_dispatch on ``publish-pypi.yml`` to bump version
2. This creates a commit with updated version numbers
3. This creates and pushes the tag
4. This creates the release
5. The release event triggers the build and publish

Instead, what happened:

1. ❌ Release v1.1.1 created manually
2. ❌ Tag v1.1.1 created pointing to old commit with version 1.0.1
3. ❌ Workflow built packages with version 1.0.1
4. ❌ PyPI rejected upload (version already exists)

--------------

How to Fix
----------

Option A: Clean Up and Recreate v1.1.1 (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This approach maintains version number consistency:

.. code:: bash

   # 1. Delete the GitHub release (via GitHub UI or gh CLI)
   gh release delete v1.1.1 --yes

   # 2. Delete the tag locally and remotely
   git tag -d v1.1.1
   git push --delete origin v1.1.1

   # 3. Ensure you're on master with latest changes
   git checkout master
   git pull

   # 4. Use the workflow's built-in version bumping
   # Go to Actions > Publish to PyPI > Run workflow
   # Select branch: master
   # Bump version: minor (to get 1.1.1 from current 1.1.0)
   # Click "Run workflow"

   # The workflow will:
   # - Bump version to 1.1.1 in pyproject.toml and scripts/__init__.py
   # - Commit the change
   # - Create tag v1.1.1
   # - Create release v1.1.1
   # - Build and publish to PyPI (on the release event)

Option B: Move Forward to v1.1.2 (Simpler)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don’t want to deal with deleting tags:

.. code:: bash

   # 1. Leave v1.1.1 as a failed release (can document it)

   # 2. Use the workflow to create v1.1.2
   # Go to Actions > Publish to PyPI > Run workflow
   # Select branch: master
   # Bump version: patch (to get 1.1.2 from current 1.1.0)
   # Click "Run workflow"

Option C: Manual Fix (Not Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Only if automation is unavailable:

.. code:: bash

   # 1. Update versions in code
   sed -i 's/version = "1.1.0"/version = "1.1.1"/' pyproject.toml
   sed -i 's/__version__ = "1.1.0"/__version__ = "1.1.1"/' scripts/__init__.py

   # 2. Commit
   git add pyproject.toml scripts/__init__.py
   git commit -m "chore: bump version to 1.1.1"
   git push

   # 3. Delete old tag and create new one
   git tag -d v1.1.1
   git push --delete origin v1.1.1
   git tag -a v1.1.1 -m "Release v1.1.1"
   git push origin v1.1.1

   # 4. Delete and recreate release via GitHub UI

--------------

Prevention: Future Safeguards
-----------------------------

Immediate Actions Taken
~~~~~~~~~~~~~~~~~~~~~~~

1. **Added Version Validation:** New ``validate-version`` job in
   ``publish-pypi.yml`` that:

   -  Checks tag version matches ``pyproject.toml`` version
   -  Checks tag version matches ``scripts/__init__.py`` version
   -  Fails fast if versions don’t align
   -  Provides clear error messages

2. **Created Validation Script:**
   ``scripts/check_version_consistency.py``:

   -  Can be run locally before creating releases
   -  Used by the workflow automatically
   -  Provides detailed version mismatch information

3. **Documentation:** Created
   ``developers/guides/pypi_publishing_guide``:

   -  Documents the correct release process
   -  Explains common pitfalls
   -  Provides troubleshooting guidance

Recommended Practices
~~~~~~~~~~~~~~~~~~~~~

1. **Always Use Workflow Dispatch:** Use the built-in
   ``bump-and-release`` job for version bumps
2. **Never Create Tags Manually:** Let the workflow create tags after
   version bumping
3. **Validate Before Release:** Run
   ``python scripts/check_version_consistency.py --tag v1.X.X`` locally
4. **Check Workflow Status:** Ensure the bump-and-release job completed
   successfully before release is created
5. **Monitor Build Output:** Check that built package versions match the
   expected version

--------------

Lessons Learned
---------------

1. **Automation is Key:** Manual release creation bypasses important
   validation steps
2. **Version Consistency:** Tag names and code versions must always
   match
3. **Fail Fast:** Early validation prevents wasted resources on builds
4. **Clear Errors:** PyPI’s error message was cryptic - our validation
   provides clarity
5. **Documentation:** Process documentation prevents mistakes

--------------

Technical Details
-----------------

Workflow Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code:: yaml

   # publish-pypi.yml
   on:
     release:
       types: [published]
     workflow_dispatch:
       inputs:
         bump_part:
           description: 'Version part to bump (major, minor, patch)'
           required: false
           default: 'patch'

Version File Locations
~~~~~~~~~~~~~~~~~~~~~~

-  **Primary:** ``pyproject.toml`` → ``[project].version``
-  **Secondary:** ``scripts/__init__.py`` → ``__version__``
-  Both must be kept in sync

PyPI Behavior
~~~~~~~~~~~~~

-  PyPI does not allow overwriting existing versions
-  Once a version is uploaded, it’s permanent (can’t be
   deleted/replaced)
-  This is a security feature to prevent supply chain attacks
-  Solution: Always bump to a new version number

--------------

Related Resources
-----------------

-  PyPI Publishing
   Guide (developers/guides/pypi_publishing_guide)
-  `Version Consistency
   Checker <../../../scripts/check_version_consistency.py>`__
-  `Workflow Source <.github/workflows/publish-pypi.yml>`__
-  `PyPI Help: File Name
   Reuse <https://pypi.org/help/#file-name-reuse>`__
-  `Semantic Versioning <https://semver.org/>`__

--------------

Contact
-------

For questions or issues with PyPI publishing:

1. Check the PyPI Publishing
   Guide (developers/guides/pypi_publishing_guide)
2. Review this debug report
3. Run local validation: ``python scripts/check_version_consistency.py``
4. Open an issue with workflow logs

--------------

| **Report Generated:** 2025-10-15
| **Status:** Issue identified and prevention measures implemented ✅
