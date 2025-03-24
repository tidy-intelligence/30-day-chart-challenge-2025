## Basic navigation app

Record the environment:

```
python -m pip freeze > requirements.txt
```

Reset the environment

```
python -m venv .venv
source .venv/bin/activatepip freeze > requirements.txt
python -m pip install -r requirements.txt
```

To build the app:

```
shinylive export . docs
```
