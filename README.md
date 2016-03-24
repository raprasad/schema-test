# schema-test
quick test

```
mkvirtualenv schema-test
pip install -r requirements.txt
cd filemetadata/
#
python manage.py check  # ignore deprecations for now
python manage.py runserver # to run a differnt port, e.g. 8070; python manage.py runserver 8070
```

- open http://127.0.0.1:8000/tsv-files/
- click one of the links
