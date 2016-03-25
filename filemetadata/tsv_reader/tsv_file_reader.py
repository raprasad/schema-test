"""
Read in Dataverse TSV files
    Examples: https://github.com/IQSS/dataverse/tree/develop/scripts/api/data/metadatablocks
"""
import sys
from os.path import isfile, isdir, join, basename
import os
from tsv_field_info import MetadataLine
from vocab_info import VocabInfo
from static_values import DELIMITER
from utils import FormatHelper
import json
from collections import OrderedDict
from static_values import TSV_FILE_DIR, JSON_SCHEMA_DIR

def msg(m): print m
def dashes(): msg('-' * 40)
def msgt(m): dashes(); msg(m); dashes()
def msgx(m): msgt(m); sys.exit(0)



class MetadataReader(object):

    def __init__(self, fname):
        assert isfile(fname), "File not found: %s" % fname

        # the file
        self.fname = fname
        # metadata block info
        self.name = None
        self.dataverse_alias = None
        self.display_name = None

        self.vocab_lookup = {}     # { field_name : [VocabInfo, VocabInfo, VocabInfo ]}
        self.field_info_list = []

    def add_vocab_line(self, info_line):
        """
        Add controlled vocabular info to the lookup
        """
        if info_line is None or len(info_line.strip()) == 0:
            return

        vocab_info = VocabInfo(info_line)
        self.vocab_lookup.setdefault(vocab_info.field, []).append(vocab_info)


    def create_schema_file(self, as_json_schema=True):

        # Gather field info
        #
        field_ordered_dict = OrderedDict()
        for field_info in self.field_info_list:
            if 1:   #field_info.name == 'author':
                field_ordered_dict[field_info.name] =\
                    field_info.as_json_schema_property()
                #field_list.append(field_info.as_json_schema_property())
                #field_list.append(field_info.as_dict(as_json_string=False))

        #field_dict = [ ]

        block_information = OrderedDict()
        block_information['title'] = self.name
        block_information['type'] = 'object'
        block_information['properties'] = field_ordered_dict
        print json.dumps(block_information, indent=4)

        json_fname = join(JSON_SCHEMA_DIR, basename(self.fname).replace('.tsv', '.json'))
        json_schema_string = json.dumps(block_information, indent=4)
        fh = open(json_fname, 'w')
        fh.write(json_schema_string)
        fh.close()
        msg('file written: %s' % json_fname)

        return True

    def add_block_level_info(self, info_line):
        block_level_attrs = [None, 'name', 'dataverse_alias', 'display_name']
        line_items = info_line.split(DELIMITER)
        print ('info_line', info_line)
        print ('line_items', line_items)

        for idx, attr in enumerate(block_level_attrs):
            if idx == 0: continue   # skip 1st col which is empty
            print (idx, attr)
            if idx < len(line_items):
                # set a line item value if you have it
                self.__dict__[attr] = FormatHelper.format_val(line_items[idx])
            else:
                self.__dict__[attr] = None
        #self.show()
        #msgx('stop')

    def read_metadata(self):

        self.process_file()
        self.add_vocab_to_fields()

    def add_vocab_to_fields(self):
        """
        Add controlled vocabulary to the MetadataLine objects
        """
        all_field_info_objects = []
        for finfo in self.field_info_list:
            all_field_info_objects.append(finfo)
            if len(finfo.children) > 0:
                all_field_info_objects += finfo.children

        for field_info in all_field_info_objects:
            #print('field_info.name', field_info.name)
            vocab_list = self.vocab_lookup.get(field_info.name, None)
            #print (vocab_list)
            if vocab_list:
                field_info.vocabinfo_list = vocab_list

        print (self.vocab_lookup.keys())

    def process_file(self):
        """
        Iterate through the file and construct objects
        """
        metadata_block_found = False
        fields_found = False
        vocab_found = False

        info_lines = open(self.fname, 'r').readlines()
        # strip blanks
        info_lines = [x.rstrip() for x in info_lines if len(x.strip()) > 0]

        line_cnt = 0
        for info_line in info_lines:
            line_cnt += 1

            msg('(%s) %s' % (line_cnt, info_line))

            # "Ifs" 4 to 6 in reverse order to how metadata appears in the TSV
            if info_line.startswith('#metadataBlock'):
                metadata_block_found = True
                print 'FOUND metadataBlock'
            elif info_line.startswith('#datasetField'):
                fields_found = True
                print 'FOUND datasetField'
            elif info_line.startswith('#controlledVocabulary'):
                vocab_found = True
                print 'FOUND controlledVocabulary'
            elif vocab_found:       # In the vocab area
                self.add_vocab_line(info_line)
            elif fields_found:      # In the field defn area
                ml = MetadataLine(info_line)
                if ml.parent:   # this is subfield
                    self.add_child_to_existing_field(ml)
                else:
                    self.field_info_list.append(ml)
            elif metadata_block_found:  # In the block header area
                self.add_block_level_info(info_line)


    def add_child_to_existing_field(self, metadata_line):
        assert isinstance(metadata_line, MetadataLine),\
            "metadata_line must be a MetadataLine object"

        # Iterate through the existing fields to find the parent
        #
        for field_info in self.field_info_list:
            if field_info.name == metadata_line.parent:
                field_info.children.append(metadata_line)
                return

        msgx('Parent not found!  Looking for: %s' % metadata_line.parent)

if __name__ == '__main__':

    # Output all of the TSV files as JSON schemas
    tsv_dir = TSV_FILE_DIR
    fnames = [ (x, join(TSV_FILE_DIR, x)) for x in os.listdir(TSV_FILE_DIR) if x.endswith('.tsv')]
    fnames = [ x for x in fnames if isfile(x[1])]
    for tsv_fname, tsv_fullname in fnames:
        mr = MetadataReader(tsv_fullname)
        mr.read_metadata()
        mr.show()
    """
    tsv_name = 'tsv_files/citation.tsv'
    tsv_name = 'tsv_files/biomedical.tsv'
    mr = MetadataReader(tsv_name)
    mr.read_metadata()
    mr.create_schema_file()
    """
    """
    for test_line in test_lines:
        ml = MetadataLine(test_line)
        ml.as_json()
        ml.create_schema_file()
    """
