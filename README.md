# QiRub
Client for Rubika Messenger

# Explain

QiRub is a Project for Rubika Client Handler
+ QiRub includes ( 'httpx', 'pycryptodome', 'fake_useragent', 'rich', 'mutagen' )

In fact when you import the ClientMessenger class or
    run the source what called ClientMessenger class, its automatically set a
        random fake user agent to have a better connection, you can off/on that on ClientMessenger class on the
            `UseFakeUserAgent` Parameter with boolean types, also you can use Proxy, on the `Proxy` Parameter to set your proxies and have a better connection
        

Make Sure you use the latest version of QiRub, for
More info you can visit our github, also you can access
To new News, Updates, Bug Fixes, ... with github

# Installation
+ for python:
      `pip install QiRub`
+ by git:
      `git clone https://github.com/Rubier-Project/QiRub`

# Usage
### import
```python
from QiRub import ClientMessenger

app = ClientMessenger("AUTH", "KEY")
```

### account information
```python
from QiRub import ClientMessenger

app = ClientMessenger("AUTH", "KEY")

print(app.accountInfo) # you can use getMe method too
```
### print colorize data
```python
from QiRub import ClientMessenger, Parse

app = ClientMessenger("AUTH", "KEY")
parse = Parse()

data = app.getMe()
parse.JsonRichParse(data)
```

# Update 1.1.0
+ Added Method `onAutoMessage`
+ Added Method `downloadSomething`
+ Added Method `getChatInfo`
+ Added New Module `urllib3`
