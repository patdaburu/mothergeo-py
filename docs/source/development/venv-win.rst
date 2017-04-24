.. _venv-setup-win:

*********************************************
Set Up a Virtual Python Environment (Windows)
*********************************************

``virtualenv`` is a tool to create isolated Python environments.  You can read more about it in the
`Virtualenv documentation <https://virtualenv.pypa.io/en/stable/>`_.  This article provides a quick summary to help
you set up and use a virtual environment.

Create a Virtual Python Environment
===================================

``cd`` to your project directory and run ``virtualenv`` to create the new virtual environment.

The following commands will create a new virtual environment under my-project/my-venv.

.. code-block:: doscon

    cd my-project
    virtualenv --python C:\Path\To\Python\python.exe venv

Activate the Environment
========================

Now that we have a virtual environment, we need to activate it.

.. code-block:: doscon

    .\venv\Scripts\activate

After you activate the environment, your command prompt will be modified to reflect the change.

Add Libraries and Create a *requirements.txt* File
====================================================

After you activate the virtual environment, you can add packages to it using ``pip``. You can also create a description
of your dependencies using ``pip``.

The following command creates a file called ``requirements.txt`` that enumerates the installed packages.

.. code-block:: doscon

    pip freeze > requirements.txt

This file can then be used by collaborators to update virtual environments using the following command.

.. code-block:: doscon

    pip install -r requirements.txt

Deactivate the Environment
==========================

To return to normal system settings, use the ``deactivate`` command.

.. code-block:: doscon

    deactivate

After you issue this command, you'll notice that the command prompt returns to normal.

Acknowledgments
---------------
Much of this article is taken from
`The Hitchhiker's Guide to Python <http://python-guide-pt-br.readthedocs.io/en/latest/>`_.  Go buy a copy right now.