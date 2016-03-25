from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'tsv_reader.views',
    url(r'^tsv-files/$', 'view_tsv_files', name='view_tsv_files'),
    url(r'^tsv-json-form/$', 'view_json_form', name='view_json_form'),
    url(r'^make-json-schema/$', 'view_make_json_schema', name='view_make_json_schema'),
    url(r'^make-all-json-schemas/$', 'view_make_all_json_schemas', name='view_make_all_json_schemas'),
    url(r'^delete-all-json-schemas/$', 'view_delete_all_json_schemas', name='view_delete_all_json_schemas'),
)
