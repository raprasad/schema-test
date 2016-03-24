# schema-test
quick test. A mix of:
  - JSON schema editor
    - http://jeremydorn.com/json-editor/
    - https://github.com/jdorn/json-editor
  - TSV from Dataverse
    - https://github.com/IQSS/dataverse/tree/develop/scripts/api/data/metadatablocks
  
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

You should see something like:

![editor example](https://raw.githubusercontent.com/raprasad/schema-test/master/JSON_Editor_Example.png)

