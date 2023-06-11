# thing-srv
Thing server

Chat with websockets.

Installation
============

Clone repo and install library::

    $ git clone git@github.com:gldecurtins/thing.git
    $ cd thing

Run application::

    $ docker-compose up

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