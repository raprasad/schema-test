import sys
from os.path import dirname, isfile, isdir, join, realpath
import os

CURRENT_DIR = dirname(realpath(__file__))

TSV_FILE_DIR = join(CURRENT_DIR, 'tsv_files')
JSON_SCHEMA_DIR = join(CURRENT_DIR, 'json_schemas')

DELIMITER = '\t'

VOCAB_FIELD_NAMES = 'field value identifier display_order'.split()

FIELD_NAMES = ('datasetField name title description'
            ' watermark  fieldType displayOrder displayFormat'
            ' advancedSearchField allowControlledVocabulary'
            ' allowmultiples facetable showabovefold required'
            ' parent metadatablock_id'.split())
