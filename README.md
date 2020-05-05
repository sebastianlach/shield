# shield
Django application for authorizing access to files and links

#### Setup
```bash
docker-compose up
```

### Testing
```bash
virtualenv venv
source venv/bin/activate
pip install -e .
python manage.py test
```

#### Tasks
```bash
invoke --list
```

Available tasks:
```
  clean   Clean up cache files.
  tests   Run test cases.
```
