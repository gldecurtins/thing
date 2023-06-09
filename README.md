# thing-srv
Thing server

Chat with websockets.

Installation
============

Clone repo and install library::

    $ git clone git@github.com:gldecurtins/thing.git
    $ cd thing

Install the app::

    $ pip install -e .

Run application::

    $ cd aiohttp_thing
    $ python main.py

Open browser::

    http://127.0.0.1:8080

Open several tabs, make them visible at the same time (to see messages sent from other tabs
without page refresh).


Requirements
============
* aiohttp_
* aiohttp_jinja2_


.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2