.. _alternate-pypi:

********************************************
How to Use an Alternate PyPI (Package Index)
********************************************

The `Python Package Index (PyPI) <https://pypi.python.org/pypi>`_ works great, but there may be times when, for
whatever reason, you need to host packages elsewhere.  You can set up your own index, or you can use a hosted
service like `Gemfury <https://gemfury.com/l/pypi-server>`_.

This article describes, in general terms, some of the things you'll need to do in your development environment to
make your use of an alternate package index a little smoother.

Installing Modules with ``pip``
===============================

One of the tricks to installing packages from your alternate repository is telling ``pip`` about it.

``pip.ini``
-----------

While you can use command line parameters with ``pip`` to indicate the location of your package index server, you
can also modify (or create) a special ``pip`` configuration file called ``pip.ini`` that will allow you install
packages from the command line just as you would if you were installing them from the public repositories.

Windows
^^^^^^^
On Windows, you can place a ``pip.ini`` file at ``%APPDATA%\pip\pip.ini``.  Use the ``extra-index-url`` option
to tell ``pip`` where your alternate package index lives.  If your package index doesn't support SSL, you can
supress warnings by identifying it as a ``trusted-host``.  The example below assumes the name of your server is
**pypi.mydomain.com** and you're running on non-standard port **8080**.

.. code-block:: ini

    [global]
    extra-index-url = http://pypi.mydomain.com:8080

    [install]
    trusted-host = pypi.mydomain.com

Linux
^^^^^
Coming soon.

.. note::

    If you are using SSL with a verified certificate, you won't need the ``trusted-host`` directive.

Publishing Modules
==================

This article doesn't go into much detail on the general process of publishing modules, but we'll assume that you're
using `setuptools <https://pypi.python.org/pypi/setuptools>`_ to publish.

``.pypirc``
-----------

You can automate the process of publishing your package with distutils by modifying the ``.pypirc`` file in your home
directory.  This file typically contains the common public indexes, but you can also add your alternate index.  The
example below assumes you're using `Gemfury <https://gemfury.com/l/pypi-server>`_, but the format will be fundamentally
similar regardless of where you're hosting your repository.

.. code-block:: ini

    [distutils]
    index-servers =
      pypi
      fury

    [pypi]
    username=mypypiuser
    password=$ecret-Pa$$w0rd

    [fury]
    repository: https://pypi.fury.io/myfuryusername/
    username: $ecret-K3y!
    password:

With that in place, you can build and upload your package by identifying the configured index server name.

.. code-block:: bash

    python setup.py sdist upload -r fury

.. note::

    Rembemer that the keys and passwords in your `.pypirc` are secrets, and should be kept away from prying eyes.