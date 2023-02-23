# enalog-py

Python library for sending events to EnaLog

### Usage

```python
from enalog import push

push_event(api_token='dummy_api_token', event={
    'project': 'enalog'
    'name': 'user-subscribed',
    'description': 'User has subscribed to EnaLog',
    'push': False,
    'icon': '💰',
    'tags': ['app': 'EnaLog'],
    'meta': {'user_id': 123}
})
```
