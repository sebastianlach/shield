# shield
Django application for authorizing access to files and links

#### Setup
```bash
virtualenv venv
source venv/bin/activate
pip install -e .
```

### Testing
```bash
python manage.py test
```

#### Usage
```bash
invoke --list
```

Available tasks:
```
  clean   Clean up cache files.
  tests   Run test cases using nose.
```
