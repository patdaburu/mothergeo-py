.. _gdal-ubuntu-pkg:

******************************************
How To Install GDAL/OGR Packages on Ubuntu
******************************************

`GDAL <http://gdal.org/>`_ is a translator library for raster and vector geospatial data formats.

`OGR <http://gdal.org/1.11/ogr/>`_ Simple Features Library is a C++ open source library (and commandline tools) providing
read (and sometimes write) access to a variety of vector file formats including ESRI Shapefiles, S-57, SDTS, PostGIS,
Oracle Spatial, and Mapinfo mid/mif and TAB formats.

OGR is a part of the GDAL library.

GDAL/OGR are used in `numerous GIS software projects <https://trac.osgeo.org/gdal/wiki/SoftwareUsingGdal>`_ and, lucky
for us, there are `bindings for python <https://pypi.python.org/pypi/GDAL>`_.  In fact, you may want to check out the
`Python GDAL/OGR Cookbook <https://pcjericks.github.io/py-gdalogr-cookbook/>`_.

This article describes a process you can follow to install GDAL/OGR on Ubuntu.

Before You Begin: Python 3.6
----------------------------

If you are installing the GDAL/OGR packages into a virtual environment based on Python 3.6, you may need to install the
`python3.6-dev package <https://packages.ubuntu.com/zesty/python3.6-dev>`_.

.. code-block:: bash

    sudo apt-get install python3.6-dev

For more information about creating virtual environments on Ubuntu 16.04 LTS, see :ref:`venv-setup-ubuntu-1604`.

Install GDAL/OGR
----------------
Much of this section is taken from a really helpful
`blog post by Sara Safavi <http://www.sarasafavi.com/installing-gdalogr-on-ubuntu.html>`_.  Follow these steps to get
GDAL/OGR installed.

To get the latest GDAL/OGR version, add the PPA to your sources, then install the gdal-bin package (this should
automatically grab any necessary dependencies, including at least the relevant libgdal version).

.. code-block:: bash

    sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update

Once you add the repository, go ahead and update your source packages.

.. code-block:: bash

    sudo apt-get update

Now you should be able to install the GDAL/OGR package.

.. code-block:: bash

    sudo apt-get install gdal-bin

To verify the installation, you can run ``ogrinfo --version``.

.. code-block:: bash

    ogrinfo

Install GDAL for Python
-----------------------

Before installing the `GDAL Python libraries <https://pypi.python.org/pypi/GDAL>`_, you'll need to install the
GDAL development libraries.

.. code-block:: bash

    sudo apt-get install libgdal-dev

You'll also need to ``export`` a couple of environment variables for the compiler.

.. code-block:: bash

    export CPLUS_INCLUDE_PATH=/usr/include/gdal
    export C_INCLUDE_PATH=/usr/include/gdal

Now you can use ``pip`` to install the Python GDAL bindings.

.. code-block:: bash

    pip install GDAL

Putting It All Together
-----------------------

If you want to run the whole process at once, we've collected all the commands above in the script below.

.. code-block:: bash

    #!/usr/bin/env bash

    sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
    sudo apt-get update
    sudo apt-get install gdal-bin
    sudo apt-get install libgdal-dev
    export CPLUS_INCLUDE_PATH=/usr/include/gdal
    export C_INCLUDE_PATH=/usr/include/gdal
    pip install GDAL



Try It Out
----------

Now that GDAL/OGR is installed, and you can program against it in Python, why not try it out?  The code block below
is a `sample <https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html#get-all-layers-in-an-esri-file-geodatabase>`_
from the `Python OGR/GDAL Cookbook <https://pcjericks.github.io/py-gdalogr-cookbook/index.html>`_ that gets all the
layers in an Esri file geodatabase.

.. code-block:: python

    # standard imports
    import sys

    # import OGR
    from osgeo import ogr

    # use OGR specific exceptions
    ogr.UseExceptions()

    # get the driver
    driver = ogr.GetDriverByName("OpenFileGDB")

    # opening the FileGDB
    try:
        gdb = driver.Open(gdb_path, 0)
    except Exception, e:
        print e
        sys.exit()

    # list to store layers'names
    featsClassList = []

    # parsing layers by index
    for featsClass_idx in range(gdb.GetLayerCount()):
        featsClass = gdb.GetLayerByIndex(featsClass_idx)
        featsClassList.append(featsClass.GetName())

    # sorting
    featsClassList.sort()

    # printing
    for featsClass in featsClassList:
        print featsClass

    # clean close
    del gdb


Acknowledgements
----------------

Thanks to `Sara Safavi <http://www.sarasafavi.com/installing-gdalogr-on-ubuntu.html>`_ and
`Paul Whipp
<https://gis.stackexchange.com/questions/28966/python-gdal-package-missing-header-file-when-installing-via-pip>`_ for
contributing some of the leg work on this.
