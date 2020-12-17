AlarmBot
========
Stack
=====
- Python 3
- Django 3.0+ as backend framework
- PostgreSQL for database

Setup for development
=====================
- Requires python 3.7+
- create a python virtual environment for project
- Install dependency package from Ubuntu repository::

    sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib

create a database name ``alarmbot`` in PostgreSQL.To ease development, we connect PostgreSQL via Unix socket. This method let you access database without specifying username and password in project's config.
::

    sudo -u postgres createuser --superuser $USER

    sudo -u postgres createdb alarmbot --owner $USER

- Install `Poetry <https://python-poetry.org/>`_ . We use it to manage Python dependencies for this project.

-Create a Python virtual environment for this project. There are many tools for this. You can also use Poetry (but please not use Pipenv).

-Go to the source folder, activate the virtual environment.
::

    (venv)$ poetry install --no-root


- to install Python projects.

Telegram bot to send message to a user via Telegram.


Deploy
======

- Run::

    ./runbot.py

to run Telegram bot (which chats with user)

- Run::

    ./runserver.py

to launch REST API server, for other application to send message to user

TelegramBot
===========
In your telegram , we need create telegrambot to get Token in alarmbot projects.
Search `BotFather` in search telegram and start. `/help` instruct to create bot and get Token.


Authentication
==============

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
We need  API tools in order to test API in projects.In this project , i use `Postman <https://www.postman.com/downloads/>`_ to test API.

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
