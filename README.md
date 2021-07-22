[![Build Status](https://travis-ci.org/paulokuong/lotame.svg?branch=master)](https://travis-ci.org/paulokuong/lotame)[![Coverage Status](https://coveralls.io/repos/github/paulokuong/lotame/badge.svg?branch=master)](https://coveralls.io/github/paulokuong/lotame?branch=master)
Lotame API Wrapper
==================

Requirements
------------

* Python 3.7.0

Installation
------------
```
    pip install lotame
```

Goal
----

To provide a generic wrapper Lotame API

Code sample
-----------

### Getting api object:
```python
  from lotame import Api, Credentials, FirehoseService, BehaviorService
  api = Api(Credentials(client_id='xxx', token='yyy', access='zzz'))
```

### Using different service classes for different endpoints:
```python
  fs = FirehoseService(api=api)
  updates = fs.getUpdates(hours=1)
```

```python
  b = BehaviorService(api=api)
  b.get('types')
```


Contributors
------------

* Paulo Kuong ([@pkuong](https://github.com/paulokuong))
