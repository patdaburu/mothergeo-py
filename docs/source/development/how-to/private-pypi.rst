.. _private-pypi:

How To Run Your Own PyPI Server
===============================

This article includes some notes we hope will be helpful in setting up your own PyPI server for those times when you
need to share modules, but you're not ready to publish them to the rest of the World.

The Server Side
---------------

There are a few different ways to host your repository.  This article focuses on
`pypi-server <https://pypi.python.org/pypi/pypiserver>`_ which you can get from
`the public package index <https://pypi.python.org/pypi/pypiserver>`_.

The Client Side
---------------

Installing Modules with ``pip``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the tricks to installing packages from your private repository is telling ``pip`` about it.

On Windows, you can place a ``pip.ini`` file at ``%APPDATA%\pip\pip.ini``

.. code-block:: ini

    [global]
    extra-index-url = http://<host>:<port>/

    [install]
    trusted-host = <host>

.. note::

    If you are using SSL with a verified certificate, you won't need the ``trusted-host`` directive.

Publishing Updates
^^^^^^^^^^^^^^^^^^

To keep life a little simpler, you probably want to modify your ``.pypirc`` file to include information about your new
repository server.  You can do this by adding an alias for the server in your list of *index-servers*. When you're
finished, your ``.pypirc`` file might look something like the one below assuming your give your new repository
**myownpypi** as an alias.

.. code-block:: ini

    [distutils]
    index-servers =
      pypi
      pypitest
      myownpypi

    [pypi]
    username=<pypi_user>
    password=<pypi_password>

    [pypitest]
    username=<pypitest_user>
    password=<pypitest_password>

    [myownpypi]
    repository: http://<host>:<port>
    username: <myownpypi_user>
    password: <myownpypi_password>

.. note::

    There are refinements to this process and we'll update this document as we go along.


