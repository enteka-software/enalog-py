# enalog-py

Python library for sending events to EnaLog

### Usage

```python
from enalog import push

push(api_token='dummy_api_token', event={
    'name': 'user-subscribed',
    'description': 'User has subscribed to EnaLog',
    'push': False,
    'icon': '💰',
    'tags': {
        'app': 'EnaLog'
    }
})
```