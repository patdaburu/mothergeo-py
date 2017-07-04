.. _pycharm-configure-folders:

*********************************
How to Exclude Folders in PyCharm
*********************************

If you're using `PyCharm <https://www.jetbrains.com/pycharm/>`_  to develop, you may have noticed that it has some
pretty righteous searching and refactoring capabilities; *however,* there are likely to be some folders in your
project's directory tree that contain files you don't want PyCharm to look at when it comes time to search or perform
automatic refactoring.  Examples of these directories include:

* the Python virtual environment (because you *definitely* don't want to modify the stuff in there);
* the ``docs`` directory (because you don't really *need* to refactor the stuff in there); and
* the ``lib`` directory (because nothing in there should depend on the code you're writing, *right?*).

There may be others as well.

PyCharm allows you to *exclude* directories from consideration when searching and refactoring.  You can exclude a
directory by right-clicking on it and selecting **Mark Directory as → Excluded**.

.. seealso::

    JetBrains' website has an article called
    `Configuring Folders Within a Content Root <https://www.jetbrains.com/help/pycharm/configuring-folders-within-a-content-root.html>`_
    which has additional insights on how and why you might want to configure the folders in the project.

