====================================
PyTICDB
====================================

.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. image:: https://github.com/mit-kavli-institute/pyticdb/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/mit-kavli-institute/pyticdb/actions
   :alt: Build Status

.. image:: https://img.shields.io/pypi/v/pyticdb.svg
   :target: https://pypi.org/project/pyticdb/
   :alt: PyPI version

.. image:: https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release
   :target: https://github.com/semantic-release/semantic-release
   :alt: semantic-release

This project initially was created to wrap around the TESS Input Catalog
database. Various functions were made to easily filter results by stellar
identifiers and spatial cone searches. However as the mission progressed and
more stellar catalogs required by scientists, PyTICDB became a wrapper around
SQLAlchemy's reflection and Q3C's spatial indexing capabilities.

Key Features
------------
* Accessing static and spatially index PostgreSQL databases.
* Session management with session pooling disabled to provide cleaner
  multiprocess use.

Documentation
-------------
Comprehensive documentation is available at:

* `GitHub Pages (if applicable) <https://your-username.github.io/your-repo/>`_

Installation
------------
To install pyticdb using PIP:

.. code-block:: bash

   pip install git+https://github.com/mit-kavli-institute/pyticdb.git

Or install from source:

.. code-block:: bash

   git clone https://github.com/mit-kavli-institute/pyticdb.git
   cd pyticdb
   pip install .

.. _configuration:

Configuration
------------------------
Utilizing ``pyticdb`` requires a configuration file to limit credential
exposure.

The expected configuration path is in ``~/.config/tic/db.conf``. The expected
structure is as follows (for each database desired).

.. code-block:: ini

   [database-alias]
   username=USERNAME
   password=PASSWORD
   database=DATABASE-NAME
   host=HOSTDOMAIN
   port=DATABASE-PORT

Please reference usage for more detailed use; however, the pattern of access
will be:

.. code-block:: python

   import pyticdb

   results = pyticdb.query_by_id([IDS], database="database-alias", table="your-table")

   # or for more refined control
   import sqlalchemy as sa
   from pyticdb import Databases

   metadata, Session = Databases["database-alias"]
   table = metadata.tables["your-table"]
   q = sa.select(table.c.your_column)
   with Session() as db:
       results = db.execute(q)

Usage
-----
PyTICDB requires a configuration file placed in your config directory for
the package to be used. Please reference :ref:`configuration` for details.

Examples will draw from the TESS Input Catalog as this was the primary purpose
of PyTICDB.


Querying by Stellar IDs
-----------------------
To query rows by stellar identifiers is to use the ``query_by_id`` function.

.. code-block:: python

   import pyticdb

   results = pyticdb.query_by_id(identifiers, "ra", "dec", "tmag")
   print(result)  # All results will be filtered to the specified ids

   # Or for non-tic databases
   results = pyticdb.query_by_id(
       identifiers, "field_1", "field_2", database="your-database", table="your-table"
   )

Testing
-------
Explain how to run tests, e.g.:

.. code-block:: bash

   nox -s tests

Or:

.. code-block:: bash

   pytest

Contributing
------------
We use conventional commits and semantic versioning for this project. **All commits must follow the conventional commit format.**

Commit Message Format
~~~~~~~~~~~~~~~~~~~~~

Each commit message must be structured as follows::

    <type>(<scope>): <subject>
    
    [optional body]
    
    [optional footer(s)]

**Required format**: ``type: subject`` (scope is optional)

**Types:**

* ``feat:`` A new feature (triggers minor version bump)
* ``fix:`` A bug fix (triggers patch version bump)
* ``docs:`` Documentation only changes
* ``style:`` Changes that do not affect the meaning of the code (formatting, etc.)
* ``refactor:`` A code change that neither fixes a bug nor adds a feature
* ``perf:`` A code change that improves performance (triggers patch version bump)
* ``test:`` Adding missing tests or correcting existing tests
* ``build:`` Changes that affect the build system or external dependencies
* ``ci:`` Changes to our CI configuration files and scripts
* ``chore:`` Other changes that don't modify src or test files
* ``revert:`` Reverts a previous commit

**Examples:**

* ✅ ``feat: add spatial query optimization``
* ✅ ``fix: resolve connection pooling issue in multiprocess environments``
* ✅ ``docs: update installation instructions``
* ✅ ``ci: add semantic release workflow``
* ❌ ``added new feature`` (missing type prefix)
* ❌ ``Fix bug`` (incorrect capitalization)

License
-------
This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details.

Authors
-------
- William Fong ( `@WilliamCFong <https://github.com/WilliamCFong>`_ )