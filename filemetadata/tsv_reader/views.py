from django.shortcuts import render
from os.path import dirname, realpath, join, isfile, isdir, basename
import os
import json

def get_tsv_dir():
    current_dir = dirname(realpath(__file__))
    tsv_dir = join(current_dir, 'tsv_files')
    assert isdir(tsv_dir), "tsv_dir not found: %s" % tsv_dir

    return tsv_dir

def get_json_schema_dir():
    current_dir = dirname(realpath(__file__))
    json_schema_dir = join(current_dir, 'json_schemas')
    assert isdir(json_schema_dir), "json_schema_dir dir not found: %s" % json_schema_dir

    return json_schema_dir

def get_triple(fname, schema_dir, tsv_dir):

    tsv_fname = fname.replace('.json', '.tsv')
    tsv_file = join(tsv_dir, tsv_fname)

    if not isfile(tsv_file):
        tsv_file = None

    return (fname, join(schema_dir, fname), tsv_fname)

def get_json_file_list():
    """
    [(file name, full file path), (file name, full file path), ]
    """
    tsv_dir = get_tsv_dir()
    schema_dir = get_json_schema_dir()

    fnames = [ get_triple(x, schema_dir, tsv_dir)\
                for x in os.listdir(schema_dir) if x.endswith('.json')]
    fnames = [ x for x in fnames if isfile(x[1])]
    return fnames

def view_tsv_files(request):
    """
    Quick (insecure) hack
    """

    context = { 'json_files' : get_json_file_list() }
    return render(request, 'tsv_reader/tsv_list.html', context)

def get_json_schema(fname):

    schema_dir = get_json_schema_dir()
    schema_file = join(schema_dir, basename(fname))
    if os.path.isfile(schema_file):
        return open(schema_file, 'r').read()

def view_json_form(request):

    context = {}

    if 'schema' in request.GET:
        schema_content = get_json_schema(request.GET['schema'])

        if schema_content:
            schema_dict = json.loads(schema_content)
            context['schema_content'] = json.dumps(schema_dict)

    #context = {}#'latest_question_list': latest_question_list}

    return render(request, 'tsv_reader/view_json_form.html', context)
