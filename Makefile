OS:=$(shell uname -s)
download = [ ! -f $(1) ] && echo "[ downloading  ] $(1)" && curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36" -O $(2)/$(1) || echo "[ downloaded   ] $(1)"
unpack = [ ! -d $(2) ] && echo "[ unpacking    ] $(1)" && tar xzf $(1) || echo "[ unpacked     ] $(1)"

define get
	@ $(call download,$(2),$(3))
	@ $(call unpack,$(2),$(1))
endef

define compile
	@ cd $(1) && \
	([ -f ./configure ] && echo "[ configuring  ] $(1)" && ($(2) sh ./configure $(3) 2>&1) >> ../tracking.log || echo "[ configured   ] $(1)") && \
	echo "[ compiling    ] $(1) with $(NPROC) cores" && \
	(make -j $(NPROC) 2>&1) >> ../tracking.log && \
	echo "[ installing   ] $(1)" && \
	(sudo make $(4) 2>&1) >> ../tracking.log
endef

define install
	@ $(call get,$(1),$(2),$(3))
	@ $(call compile,$(1),,,install)
endef

update_shared_libs=sudo ldconfig
POSTGRES_PATH=/usr/local/pgsql/bin
ifeq ($(OS), Darwin)
	NPROC=$(shell sysctl -n hw.ncpu)
	update_shared_libs=
	LIBPOSTGRES=/usr/local/pgsql/lib/libpq.5.5.dylib
	LIBSQLITE3=/usr/local/lib/libsqlite3.0.dylib
	LIBHDF5=/usr/local/lib/libhdf5_hl.8.dylib
	LIBNETCDF=/usr/local/lib/libnetcdf.7.dylib
	CONFIGURE_USER_POSTGRES= \
		sudo dscl . -create /Users/postgres UniqueID 174 && \
		sudo dscl . -create /Users/postgres PrimaryGroupID 174 && \
		sudo dscl . -create /Users/postgres HomeDirectory /usr/local/pgsql && \
		sudo dscl . -create /Users/postgres UserShell /usr/bin/false && \
		sudo dscl . -create /Users/postgres RealName "PostgreSQL Administrator" && \
		sudo dscl . -create /Users/postgres Password \* && \
		dscl . -read /Users/postgres && \
		sudo dscl . -create /Groups/postgres PrimaryGroupID 174 && \
		sudo dscl . -create /Groups/postgres Password \* && \
		dscl . -read /Groups/postgres
endif
ifeq ($(OS), Linux)
	#DISTRO=$(shell lsb_release -si)
	#ifeq ($(DISTRO), CentOS)
	#endif
	NPROC=$(shell nproc)
	LIBPOSTGRES=/usr/local/pgsql/lib/libpq.so.5.5
	LIBSQLITE3=/usr/local/lib/libsqlite3.so.0.8.6
	LIBHDF5=/usr/local/lib/libhdf5.so.8.0.1
	LIBNETCDF=/usr/local/lib/libnetcdf.so.7.2.0
	CONFIGURE_USER_POSTGRES= ( sudo grep postgres /etc/passwd || \
		( sudo adduser postgres && \
		sudo passwd postgres ) && \
		sudo ln -fs /usr/local/pgsql/lib/libpq.so.5 /usr/lib/libpq.so.5)
endif

DEFAULT_VERSION=2.7.6
export PYLARGEVERSION=$(PYVERSION)
ifeq ($(PYLARGEVERSION),)
	export PYLARGEVERSION=$(DEFAULT_VERSION)
endif
PYCONCAT=-

export DOTS=$(shell ./dots_amount.sh $(PYLARGEVERSION))
export PYSHORTVERSION=$(shell ./short_version.sh $(PYLARGEVERSION))

ifeq ($(DOTS),1)
	PYSHORTVERSION=$(PYLARGEVERSION)
endif

export PYSHORTSUFIX_VER=$(PYCONCAT)$(PYSHORTVERSION)
export PYLARGESUFIX_VER=$(PYCONCAT)$(PYLARGEVERSION)

PYPREFIX_PATH=/usr/local
PYTHONLIBS=LD_LIBRARY_PATH=/usr/local/lib
PYTHONPATH=$(PYPREFIX_PATH)/bin/python$(PYSHORTVERSION)
FIRST_EASYINSTALL=$(PYTHONLIBS) $(PYPREFIX_PATH)/bin/easy_install$(PYSHORTSUFIX_VER)
PIP=bin/pip
PYTHON=bin/python
EASYINSTALL=bin/easy_install
VIRTUALENV=virtualenv
SOURCE_ACTIVATE=$(PYTHONLIBS) . bin/activate; 

ifneq ($(filter-out postgres,$(MAKECMDGOALS)),$(MAKECMDGOALS))
	DATABASE_REQUIREMENTS=postgres-requirements
	dbname=factopy
	user=postgres
endif

unattended:
	@ (sudo ls 2>&1) >> tracking.log

Python$(PYLARGESUFIX_VER):
	$(call get,Python$(PYLARGESUFIX_VER),Python$(PYLARGESUFIX_VER).tgz,https://www.python.org/ftp/python/$(PYLARGEVERSION))
	$(call compile,Python$(PYLARGESUFIX_VER),$(PYTHONLIBS),--prefix=$(PYPREFIX_PATH) --with-threads --enable-shared,altinstall)

$(PYTHONPATH): Python$(PYLARGESUFIX_VER)
	@ $(call download,ez_setup.py,https://bitbucket.org/pypa/setuptools/raw/bootstrap)
	@ (sudo rm /usr/local/lib/python2.7/site-packages/setuptools-*-py2.7.egg 2>&1) >> tracking.log
	@ (sudo $(PYTHONLIBS) $(PYTHONPATH) ez_setup.py 2>&1) >> tracking.log

$(LIBSQLITE3):
	$(call install,sqlite-autoconf-3080100,sqlite-autoconf-3080100.tar.gz,http://www.sqlite.org/2013)

sqlite3: $(LIBSQLITE3)
	@ echo "[ setting up   ] sqlite3 database"
	@ cd factopy_configuration && cp -f database.sqlite3.py database.py

$(LIBPOSTGRES):
	$(call get,postgresql-9.2.4,postgresql-9.2.4.tar.gz,ftp://ftp.postgresql.org/pub/source/v9.2.4)
	$(call compile,postgresql-9.2.4,,--without-readline --without-zlib,install)
	@ ($(CONFIGURE_USER_POSTGRES) && \
		sudo mkdir /usr/local/pgsql/data 2>&1 && \
		sudo chown postgres:postgres /usr/local/pgsql/data 2>&1) >> tracking.log
	@ (sudo -u postgres $(POSTGRES_PATH)/initdb -D /usr/local/pgsql/data 2>&1) >> tracking.log
	@ sleep 5

pg-start: $(POSTGRES_PATH)/pg_ctl
	@ echo "[ starting     ] postgres database"
	@ (sudo -u postgres $(POSTGRES_PATH)/pg_ctl -D /usr/local/pgsql/data start 2>&1) >> tracking.log || exit 0;
	@ sleep 20;

pg-restart: $(POSTGRES_PATH)/pg_ctl
	@ echo "[ restarting   ] postgres database"
	@ (sudo -u postgres $(POSTGRES_PATH)/pg_ctl -D /usr/local/pgsql/data reload 2>&1) >> tracking.log || exit 0;

pg-stop:
	@ echo "[ stoping      ] postgres database"
	@ (! (test -s $(POSTGRES_PATH)/data/postmaster.pid && test -s $(POSTGRES_PATH)/pg_ctl) || sudo -u postgres $(POSTGRES_PATH)/pg_ctl -D /usr/local/pgsql/data stop 2>&1) >> tracking.log
	@ (sudo killall postgres postmaster 2>&1) >> tracking.log || exit 0;

postgres: $(LIBPOSTGRES) pg-start
	@ (sudo -u postgres $(POSTGRES_PATH)/dropuser --if-exists $(shell whoami) 2>&1) >> tracking.log
	@ (sudo -u postgres $(POSTGRES_PATH)/createuser --superuser --createdb $(shell whoami) 2>&1) >> tracking.log
	@ echo "[ setting up   ] postgres database"
	@ cd factopy_configuration && cp -f database.postgres.py database.py

aspects.py:
	$(call get,python-aspects-1.3,python-aspects-1.3.tar.gz,http://www.cs.tut.fi/~ask/aspects)
	@ cp python-aspects-1.3/aspects.py aspects.py

libs-and-headers: $(PYTHONPATH) aspects.py
	@ $(update_shared_libs)

bin/activate: requirements.txt
	@ echo "[ using        ] $(PYTHONPATH)"
	@ echo "[ installing   ] $(VIRTUALENV)"
	@ (sudo $(FIRST_EASYINSTALL) virtualenv 2>&1) >> tracking.log
	@ echo "[ creating     ] $(VIRTUALENV) with no site packages"
	@ ($(PYTHONLIBS) $(VIRTUALENV) --python=$(PYTHONPATH) --no-site-packages . 2>&1) >> tracking.log
	@ echo "[ installing   ] $(PIP) inside $(VIRTUALENV)"
	@ ($(SOURCE_ACTIVATE) $(EASYINSTALL) pip 2>&1) >> tracking.log
	@ echo "[ installing   ] $(PIP) requirements"
	@ PATH="$(POSTGRES_PATH):$(PATH)"; $(SOURCE_ACTIVATE) $(PIP) install --default-timeout=100 -r requirements.txt 2>&1 | grep Downloading
	@ touch bin/activate

postgres-requirements:
	@ echo "[ installing   ] $(PIP) requirements for postgres"
	@ export PATH="${PATH}:$(POSTGRES_PATH)/" ; \
		($(SOURCE_ACTIVATE) $(PIP) install --default-timeout=100 -r requirements.postgres.txt --upgrade 2>&1 && \
		($(POSTGRES_PATH)/dropdb   $(dbname) -U $(user) --if-exists 2>&1 && \
		$(POSTGRES_PATH)/createdb $(dbname) -U $(user) 2>&1)) >> tracking.log

db-migrate: $(DATABASE_REQUIREMENTS)
	@ echo "[ migrating    ] setting up the database structure"	
	@ ($(SOURCE_ACTIVATE) $(PYTHON) manage.py syncdb --noinput 2>&1) >> ../tracking.log

deploy: libs-and-headers bin/activate db-migrate

show-version:
	@ $(SOURCE_ACTIVATE) $(PYTHON) --version

defaultsuperuser:
	@ echo "For the 'dev' user please select a password"
	@ $(SOURCE_ACTIVATE) $(PYTHON) manage.py createsuperuser --username=dev --email=dev@dev.com

run:
	@ $(SOURCE_ACTIVATE) $(PYTHON) manage.py runserver 0.0.0.0:8000

runbackend:
	@ $(SOURCE_ACTIVATE) $(PYTHON) manage.py runbackend 4

test:
	@ $(SOURCE_ACTIVATE) $(PYTHON) manage.py test factopy

test-coverage-travis-ci:
	@ $(SOURCE_ACTIVATE) coverage run --source='factopy/models/' manage.py test factopy

test-coveralls:
	@ $(SOURCE_ACTIVATE) coveralls

test-coverage: test-coverage-travis-ci test-coveralls

pypi-upload: test
	@ echo "[ uploading    ] package to pypi servers"
	@ ($(SOURCE_ACTIVATE) $(PYTHON) setup.py sdist upload 2>&1) >> tracking.log

clean: pg-stop
	@ echo "[ cleaning     ] remove deployment generated files that doesn't exists in the git repository"
	@ sudo rm -rf sqlite* postgresql* hdf5* netcdf-4* python-aspects* virtualenv* bin/ lib/ lib64 include/ build/ share Python-* .Python ez_setup.py setuptools-*.tar.gz get-pip.py tracking.log factopy.sqlite3 aspects.py subversion

hardclean: clean
	@ echo "[ cleaning     ] remove compiled libraries and the database engine"
	@ cd /usr/local/bin && sudo rm -rf python* sqlite3
	@ cd /usr/local/lib && sudo rm -rf libpython* libhdf5* libnetcdf* libsqlite3* python*
	@ cd /usr/local && sudo rm -rf pgsql*