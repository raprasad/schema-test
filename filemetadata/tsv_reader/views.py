from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect # Http404
from django.core.urlresolvers import reverse
from os.path import dirname, realpath, join, isfile, isdir, basename
from collections import OrderedDict
import os
import json
from static_values import TSV_FILE_DIR, JSON_SCHEMA_DIR

from tsv_file_reader import MetadataReader

def get_json_schema_dir():
    current_dir = dirname(realpath(__file__))
    json_schema_dir = join(current_dir, 'json_schemas')
    assert isdir(json_schema_dir), "json_schema_dir dir not found: %s" % json_schema_dir

    return json_schema_dir

def get_triple(fname):

    tsv_fname = fname.replace('.json', '.tsv')
    tsv_file = join(TSV_FILE_DIR, tsv_fname)

    if not isfile(tsv_file):
        tsv_file = None

    return (fname, join(JSON_SCHEMA_DIR, fname), tsv_fname)


def get_json_file_list():
    """
    [(tsv file name, json file name or None), ]
    """
    # get existing tsv file list
    tsv_files = [x for x in os.listdir(TSV_FILE_DIR) if x.endswith('.tsv')]
    print 'tsv_files', tsv_files
    file_pairs = []
    # iterate through actual tsv files
    for tsv_file in tsv_files:
        json_file = join(JSON_SCHEMA_DIR, tsv_file.replace('.tsv', '.json'))
        print '\n', tsv_file, json_file
        # Does a JSON schema exist?
        if isfile(json_file):
            print 'YES'
            # Yes:  (tsv_file, json_file)   - basenames only
            file_pairs.append((tsv_file, basename(json_file)))
        else:
            print 'NO'
            # No:  (tsv_file, None)   - basenames only
            file_pairs.append((tsv_file, None))

    return file_pairs

def view_tsv_files(request):
    """
    Quick (insecure) hack
    """

    context = { 'json_files' : get_json_file_list(),\
             'JSON_SCHEMA_DIR' : JSON_SCHEMA_DIR,\
             'TSV_FILE_DIR' : TSV_FILE_DIR }
    return render(request, 'tsv_reader/tsv_list.html', context)

def get_json_schema(fname):
    """
    Return the contents of a JSON schema file
    """
    schema_file = join(JSON_SCHEMA_DIR, basename(fname))
    if os.path.isfile(schema_file):
        return open(schema_file, 'r').read()


def view_delete_all_json_schemas(request):

    for fname in os.listdir(JSON_SCHEMA_DIR):
        if fname.lower().endswith('json'):
            os.remove(join(JSON_SCHEMA_DIR, fname))

    return HttpResponseRedirect(reverse('view_tsv_files', kwargs={}))


def view_make_all_json_schemas(request):
    """
    Make JSON schema from all TSV files
    Overwrite existing schemas if they exist
    """
    for tsv_fname in os.listdir(TSV_FILE_DIR):
        tsv_fullname = join(TSV_FILE_DIR, tsv_fname)
        if not isfile(tsv_fullname):
            return HttpResponse('The file was not found: %s\
            <br>(Please use the back button on your browser)' % tsv_fullname)

        mr = MetadataReader(tsv_fullname)
        mr.read_metadata()
        mr.create_schema_file()

    return HttpResponseRedirect(reverse('view_tsv_files', kwargs={}))


def view_make_json_schema(request):
    """
    Make a schema from a TSV and redirect to the file listing page
    (proof of concept)
    """
    if not 'tsv' in request.GET:
        return HttpResponse('Sorry! No TSV file specified<br>(Please use the back button on your browser)')

    tsv_fname = request.GET['tsv']
    tsv_fullname = join(TSV_FILE_DIR, tsv_fname)
    if not isfile(tsv_fullname):
        return HttpResponse('The file was not found: %s\
            <br>(Please use the back button on your browser)' % tsv_fullname)

    #tsv_name = 'tsv_files/biomedical.tsv'
    mr = MetadataReader(tsv_fullname)
    mr.read_metadata()
    mr.create_schema_file()

    return HttpResponseRedirect(reverse('view_tsv_files', kwargs={}))

def view_json_form(request):

    context = {}

    if 'schema' in request.GET:
        schema_content = get_json_schema(request.GET['schema'])

        if schema_content:
            #context['schema_content'] = schema_content
            #
            schema_dict = json.loads(schema_content,\
                        object_pairs_hook=OrderedDict)
            context['schema_content'] = json.dumps(schema_dict)

    #context = {}#'latest_question_list': latest_question_list}

    return render(request, 'tsv_reader/view_json_form.html', context)
