from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'tsv_reader.views',
    url(r'^tsv-files/$', 'view_tsv_files', name='view_tsv_files'),
    url(r'^tsv-json-form/$', 'view_json_form', name='view_json_form'),

)
