.. _logging-boilerplate:

*********************************************************
From the Hitchhicker's Guide: Logging in Python Libraries
*********************************************************

.. note::

    If you're wondering how Mother likes to handle logging, take a look at :ref:`logging`.

It is, of course, desirable for library modules to perform logging.  However, we generally want to maintain consistency
and allow the consuming application to perform logging configuration.  This article details a strategy for achieving
those goals.

A Bit of Loging Boilerplate
---------------------------

From `The Hitchhiker's Guide to Python <http://python-guide-pt-br.readthedocs.io/en/latest/>`_, Chapter 4:

    Do not add any handlers other than ``NullHandler`` to your library's loggers.  Place the following code in your
    project's top-level ``__init__.py``.

.. code-block:: python

    # Set default logging handler to avoid "No handler found" warnings.
    import logging
    try: # Python 2.7+
        from logging import NullHandler
    except ImportError:
        class NullHandler(logging.Handler):
            def emit(self, record):
                pass

    logging.getLogger(__name__).addHandler(NullHandler())


Acknowledgments
---------------
Much of this article is taken from
`The Hitchhiker's Guide to Python <http://python-guide-pt-br.readthedocs.io/en/latest/>`_.  Go buy a copy right now.