.. _logging:

**************************************
How To Use Mother's ``logging`` Module
**************************************

Mother has her own ``logging`` module which you are *strongly* encouraged to use within the project.

--------------------------------------
Using the ``loggable_class`` Decorator
--------------------------------------

When you create a new class, you can provide it with a Python logger just by decorating it with the ``@loggable_class``
decorator (abbreviated to ``@loggable`` in the example).  The code sample below will provide a ``logger`` property to
the decorated class.

.. code-block:: python

    import logging
    import sys
    # (Let's alias the decorator's name for brevity's sake.)
    from mothergeo.logging import loggable_class as loggable

    # We'll just create a simple test configuration so we can see logging occur.
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG
    )

    @loggable
    class MyUsefulClass(object):

        def my_useful_method(self):
            self.logger.debug("I'm using the logger that was provided by the decorator.")
            print("You should see some logging output.")

    if __name__ == "__main__":
        my_useful_object = MyUsefulClass()
        my_useful_method()

----------------------------------
Overriding the Default Logger Name
----------------------------------

By default, the name of the Python logger a class decorated with the ``@logger_class`` decorator creates a logger
based on the module in which the class is found, and the name of the class.  You can override this behavior by
providing a ``logger_name`` property on the decorated class, as in the example below.

.. code-block:: python
    :emphasize-lines: 15

    import logging
    import sys
    # (Let's alias the decorator's name for brevity's sake.)
    from mothergeo.logging import loggable_class as loggable

    # We'll just create a simple test configuration so we can see logging occur.
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG
    )

    @loggable
    class MyUsefulClass(object):

        logger_name = 'alterate.logger.name'  # Override the default logger name formula.

        def my_useful_method(self):
            self.logger.debug("The logger's name should reflect the 'logger_name' property.")
            print("You should see some logging output.")

    if __name__ == "__main__":
        my_useful_object = MyUsefulClass()
        my_useful_method()

.. seealso::

    If you're interested in reading more about logging in Python, have a look at :ref:`logging-boilerplate`.