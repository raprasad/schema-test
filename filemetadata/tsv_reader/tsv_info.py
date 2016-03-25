from os.path import dirname, isfile, isdir, join, realpath, basename

from static_values import TSV_FILE_DIR, JSON_SCHEMA_DIR

class TSVInfo(object):
    """
    Pair TSV files and associated JSON SCHEMA
    """
    def __init__(self, tsv_filename):
        self.tsv_filename = basename(tsv_filename)
