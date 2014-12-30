factopy
=======

[![GNU/AGPL License](http://www.gnu.org/graphics/agplv3-88x31.png)](https://github.com/gersolar/factopy/blob/master/GNU-AGPL-3.0.txt) [![Build Status](https://travis-ci.org/gersolar/factopy.png?branch=master)](https://travis-ci.org/gersolar/factopy) [![Coverage Status](https://coveralls.io/repos/gersolar/factopy/badge.png)](https://coveralls.io/r/gersolar/factopy) [![Code Health](https://landscape.io/github/gersolar/factopy/master/landscape.png)](https://landscape.io/github/gersolar/factopy/master) [![django packages badge](https://pypip.in/d/factopy/badge.png)](https://www.djangopackages.com/packages/p/factopy/)
[![Supported Python versions](https://pypip.in/py_versions/factopy/badge.svg)](https://pypi.python.org/pypi/factopy/) [![Stories in Ready](https://badge.waffle.io/gersolar/factopy.png?label=ready&title=Ready)](https://waffle.io/gersolar/factopy)
**factopy** is a python framework and provides abstract classes for a high performance computing cluster based in a pipe and filter architecture.

Requirements
------------

If you want to deploy this repository with the default settings, on any GNU/Linux or OSX system you just need to execute the next bash command to setting up all the requirements (GNUMakefile should have been installed to this point).

	$ PYVERSION=2.7 make sqlite3 deploy

But, if you want use **postgresql** instead of sqlite3, you should execute the next bash command:

	$ PYVERSION=2.7 make postgres deploy

All the testing are made in **python2.7**. If you haven't installed **python2.7** it is automatically installed with the previous command.

As an exception, for **Ubuntu Desktop** (or Ubuntu in general) you can use the command:

    $ PYVERSION=2.7 make ubuntu postgres deploy

Last, you should configure a superuser access to the **frontend**. To do so, you should execute the next command and then fill the password field.

	$ make defaultsuperuser

Running
-------

There are 2 services, the **frontend** and the **backend**. First we recommend you to bootup the **frontend** using the command:

	$ make run

Now you can go to a browser on the same machine and use the address <http://localhost:8000/admin> to login to the service. You should complete the username field with "dev" and in the password field you should use your previously selected password.

Testing
-------

To test all the project you should use the command:

	$ make test

If you want to help us or report an issue use the [GitHub issue tracker](https://github.com/gersolar/factopy/issues).
