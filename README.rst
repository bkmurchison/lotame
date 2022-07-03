..
  | |Build Status|

Lotame API Wrapper
------------------

Wrapper Class for Lotame API.

    | Wrapper class for Lotame REST API.
    | https://api.lotame.com/docs
    | https://github.com/bkmurchison/lotame

Requirements
------------

-  Python 3.8 (tested)

Goal
----

| To provide a generic wrapper Lotame API

Code sample
-----------

| Instantiate

.. code:: python

  from lotame import Api, Credentials, FirehoseService, BehaviorService
  api = Api(Credentials(client_id='xxx', token='yyy', access='zzz'))

.. code:: python

  fs = FirehoseService(api=api)
  updates = fs.getUpdates(hours=1)

.. code:: python

  b = BehaviorService(api=api)
  b.get('types')

Contributors
------------

-  Paulo Kuong (`@pkuong`_)
-  BK Murchison (`@bkmurchison`_)

.. _@pkuong: https://github.com/paulokuong
.. _@bkmurchison: https://github.com/bkmurchison

..
.. |Build Status| image:: https://travis-ci.org/paulokuong/lotame.svg?branch=master
..
.. target: https://travis-ci.org/paulokuong/lotame
