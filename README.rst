Telegram bot to send message to a user via Telegram.


Deploy
======

- Run::

    ./runbot.py

to run Telegram bot (which chats with user)

- Run::

    ./runserver.py

to launch REST API server, for other application to send message to user

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
