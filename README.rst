=======
PyTICDB
=======


.. image:: https://img.shields.io/pypi/v/pyticdb.svg
        :target: https://pypi.python.org/pypi/pyticdb

.. image:: https://img.shields.io/travis/wcfong/pyticdb.svg
        :target: https://travis-ci.com/wcfong/pyticdb

.. image:: https://readthedocs.org/projects/pyticdb/badge/?version=latest
        :target: https://pyticdb.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A python wrapper for the TESS Input Catalog.


* Free software: MIT license
* Documentation: https://pyticdb.readthedocs.io.


Installation
------------
Install by cloning and running ``pip install --upgrade -U .``

Configuration must be provided a file ``~/.config/tic/db.conf`` and populated as such

.. code-block:: ini

   [tic_82]
   username={POSTGRES_USERNAME}
   password={POSTGRES_PASSWORD}
   database=tic_82
   host={POSTGRES_HOST}
   port={POSTGRES_PORT}

You may also define any other catalog database as such:

.. code-block:: ini
   [meaningful-name]
   username={POSTGERS_USERNAME}
   password={POSTGRES_PASSWORD}
   database={POSTGRES_DATABASE}
   host={POSTGRES_HOST}
   port={POSTGRES_PORT}

Features
--------
Provides an easy interface with the TESS Input Catalog by default although
other spatial databases may be used as well.

By default, the TIC (8.2) is used. However any SQL database catalog may be
used so long as the configuration credentials are stored in the config file
under their own sections.


.. code-block:: python

    from pyticdb import query_by_id

    # Query a single id
    result = query_by_id(379824738, "ra", "dec", "tmag")
    print(result)  # [(324.599056601, 23.1191319106, 10.291)]

    # Or query by multiple_ids
    result = query_by_id([283471501, 398895470, 500], "id", "ra", "dec", "tmag")
    print(result)
    # [(500, 218.728664673, -29.1269141296, 11.6116),
    # (283471501, 314.547762642, 40.1913891016, 9.3206),
    # (398895470, 297.32266648, 4.67243988495, 10.5523)]


.. code-block:: python

    from pyticdb import query_by_loc

    result = query_by_loc(10.0, -18.0, 4.0, "id", "ra", "dec", "tmag")
    print(result)
    # [(322510862, 7.115643592, -20.8972242098, 18.9336),
    # (322494926, 7.00403786173, -20.8105061739, 16.6554),
    # (610234046, 7.01161890217, -20.8083484912, 19.8365),
    # (322510866, 7.05469912571, -20.8776725744, 15.7966)
    # ...

To use other databases you may provide the config section name and what table
you wish to query.

.. code-block:: python

    from pyticdb import query_by_id

    result = query_by_loc(
        10.0,
        -20.0,
        5.0,
        "source_id",
        database="gaia3",
        table="gaia_source"
    )


``PyTICDB`` also provides interfaces for further filtering queries; we provide
filtering through django-like parameters and filtering through SQLAlchemy expressions.

.. code-block:: python

    from pyticdb import query_by_loc

    # Django like filtering
    result = query_by_loc(10.0, -18.0, 4.0, "id", "ra", "dec", "tmag", tmag__le=13.5)
    # ^ resembles
    # SELECT id, ra, dec, tmag
    # FROM ticentries
    # WHERE q3c_radial_query(ra, dec, 10.0, -18.0, 4.0) AND tmag <= 13.5;


However, more complex querying functionality might be needed. In those cases
you can access the reflected tables in the global Databases cache.

.. code-block:: python

    # Or you may pass SQLAlchemy expressions.
    from pyticdb.conn import Databases

    meta, _ = Databases["tic_82"]
    TICEntry = meta.tables["ticentries"]

    filters = [TICEntry.c.tmag.between(9, 13.5)]
    result = query_by_loc(10.0, -18.0, 4.0, "id", "ra", "dec", "tmag", expression_filters=filters)
    # ^ resembles
    # SELECT id, ra, dec, tmag
    # FROM ticentries
    # WHERE q3c_radial_query(ra, dec, 10.0, -18.0, 4.0) AND tmag BETWEEN 9 AND 13.5;


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
