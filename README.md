# shield
Django application for authorizing access to files and links

#### Setup
```bash
virtualenv venv
source venv/bin/activate
pip install -e .
pip install -r tests/requirements.txt
```

#### Usage
```bash
invoke --list
```

Available tasks:
```
  clean   Clean up cache files.
  tests   Run test cases.
```

```bash
invoke clean
invoke tests
```
