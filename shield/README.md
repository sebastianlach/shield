# shield
Django application for authorizing access to files and links

#### Setup
```bash
virtualenv venv
source venv/bin/activate
cd shield
pip install -e .
python manage.py runserver
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
