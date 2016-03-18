"""
Read in Dataverse TSV files
    Examples: https://github.com/IQSS/dataverse/tree/develop/scripts/api/data/metadatablocks
"""
import csv
from os.path import isfile, isdir, join
import csv


class MetadataReader(object):

    def __init__(self, fname):
        assert isfile(fname), "File not found: %s" % fname

        self.fname = fname
