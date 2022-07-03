Lotame API Wrapper
==================

Requirements
------------

* Python 3.8

Installation
------------
```shell
    pip install lotame
```

Goal
----

To provide a generic wrapper Lotame API?

Code sample
-----------

```python
from lotame.api import Api
from lotame.credentials import Credentials
from lotame.services.audience import AudienceService
from lotame.services.behavior import BehaviorService
from lotame.services.firehose import FirehoseService

# Getting api object:

api = Api(Credentials(client_id='xxx', token='yyy', access='zzz'))

# Using different service classes for different endpoints:

f = FirehoseService(api=api)
updates = f.get_updates(hours=1)

b = BehaviorService(api=api)
types = b.get('types')

a = AudienceService(api=api)
audiences = a.get('audience')
```


Contributors
------------

* Paulo Kuong ([@pkuong](https://github.com/paulokuong))
* BK Murchison ([@bkmurchison](https://github.com/bkmurchison))
