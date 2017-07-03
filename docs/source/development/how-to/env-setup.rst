.. _env-setup:

******************************************
How To Set Up Your Development Environment
******************************************

This article describes the steps you can follow to get the mothergeo-py project set up for development.

Get the Source
--------------

This project is managed under source control in GitHub, so you'll need to install ``git``.  Once you have that going,
getting the latest version of the code is just a matter of cloning the repository into your development directory.

.. code-block:: bash

    git clone https://github.com/patdaburu/mothergeo-py.git

Get the Requirements
--------------------

The project uses a number of modules that are available from the
`PyPI package repository <https://pypi.python.org/pypi>`_.  All of the required modules should be listed in the
:ref:`requirements-txt` file in the root directory, and you can get them using ``pip``.

.. code-block:: bash

    pip install -r requirements.txt

