======
Karaka
======

Stack
~~~~~

- Python 3
- Django 3.0+ as backend framework
- PostgreSQL for database

Setup for development
~~~~~~~~~~~~~~~~~~~~~

- Requires python 3.7+
- create a python virtual environment for project
- Install dependency package from Ubuntu repository

  .. code-block:: sh

    sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib

- Create a database name ``alarmbot`` in PostgreSQL. To ease development, we connect PostgreSQL via Unix socket. This method let you access database without specifying username and password in project's config.

  .. code-block:: sh

    sudo -u postgres createuser --superuser $USER

    sudo -u postgres createdb alarmbot --owner $USER

- Install `Poetry <https://python-poetry.org/>`_ . We use it to manage Python dependencies for this project.

- Create a Python virtual environment for this project. There are many tools for this. You can also use Poetry (but please not use Pipenv).

- Go to the source folder, activate the virtual environment.

  .. code-block:: sh

    (venv)$ poetry install --no-root


  to install Python packages.


Deploy
~~~~~~

- Run:

  .. code-block:: sh

    ./runbot.py

  to run Telegram bot (which chats with user)

- Run:

  .. code-block:: sh

    ./runserver.py

  to launch REST API server, for other application to send message to user


Configuration
~~~~~~~~~~~~~

Telegram bot
------------

Register a Telegram bot to get token.


Authentication
--------------

Add to *.secrets.toml* file. Example

.. code-block:: toml

    [default]
    TELEGRAM_TOKEN = 'TOKEN_THAT_TELEGRAM_GAVE_YOU'

    API_USERS = [
        ['abc', '123456']
    ]


Translation
===========

.. code-block::

    pybabel extract alarmbot/*.py -o locales/alarmbot.pot
    pybabel compile -d locales -l vi -D alarmbot


API
===

Create user
-----------

.. code-block::

    POST /users/

.. code-block:: python

    {
        'username': 'someone',
        'first_name': '',
        'last_name': '',
        'language_code': 'vi'
    }

with ``username`` being Telegram username.

Send message to user
--------------------

.. code-block::

    POST /users/[username]/message

.. code-block:: python

    {
        'message': 'Your farm is on fire!'
    }
