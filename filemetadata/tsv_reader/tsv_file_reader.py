"""
Read in Dataverse TSV files
    Examples: https://github.com/IQSS/dataverse/tree/develop/scripts/api/data/metadatablocks
"""
import sys
from os.path import isfile, isdir, join
import os
from tsv_field_info import MetadataLine
import json
from collections import OrderedDict

def msg(m): print m
def dashes(): msg('-' * 40)
def msgt(m): dashes(); msg(m); dashes()
def msgx(m): msgt(m); sys.exit(0)


DELIMITER = '\t'

VOCAB_FIELD_NAMES = 'field value identifier display_order'.split()
class VocabInfo(object):

    def __init__(self, vocab_line):
        self.init_fields(vocab_line)

    def init_fields(self, line):

        line_items = line.split(DELIMITER)

        # Iterate through fields
        for idx, field_name in enumerate([None] + VOCAB_FIELD_NAMES):
            if idx == 0: continue   # skip 1st col which is empty
            if idx < len(line_items):
                # set a line item value if you have it
                val = MetadataLine.format_val(line_items[idx])
            else:
                # default to None
                val = None
            self.__dict__[field_name] = val

    def as_dict(self):
        d = {}
        for field_name in VOCAB_FIELD_NAMES[1:]:
            d[field_name] = self.__dict__.get(field_name, None)
        return d

    def as_json(self):
        print json.dumps(self.__dict__, indent=4)

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


    def show(self, as_json_schema=True):

        # Gather field info
        #
        field_ordered_dict = OrderedDict()
        for field_info in self.field_info_list:
            if 1:#field_info.name == 'subject':
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

        json_fname = 'json_schemas/%s.json' % self.name
        json_schema_string = json.dumps(block_information, indent=4)
        open(json_fname, 'w').write(json_schema_string)
        msg('file written: %s' % json_fname)

        #block_information['name'] = self.name
        #block_information['dataverse_alias'] = self.dataverse_alias
        #block_information['display_name'] = self.display_name

        """
        block_dict = dict(block_information=block_information,\
                title=self.name,\
                type='object',\
                properties=field_list\
                )

        block_dict_ordered = OrderedDict(sorted(block_dict.items(), key=lambda t: t[0]))

        print json.dumps(block_dict_ordered, indent=4)
        """

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
                self.__dict__[attr] = MetadataLine.format_val(line_items[idx])
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
        for field_info in self.field_info_list:
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
                self.field_info_list.append(ml)
            elif metadata_block_found:  # In the block header area
                self.add_block_level_info(info_line)


if __name__ == '__main__':
    test_lines = """#metadataBlock	name	dataverseAlias	displayName
	citation		Citation Metadata""".split('\n')
    """
    allowControlledVocabulary	allowmultiples	facetable	showabovefold	required	parent	metadatablock_id
	title	Title	Full title by which the Dataset is known.	Enter title...	text	0		TRUE	FALSE	FALSE	FALSE	TRUE	TRUE		citation
	subtitle	Subtitle	A secondary title used to amplify or state certain limitations on the main title.		text	1		FALSE	FALSE	FALSE	FALSE	FALSE	FALSE		citation
	alternativeTitle	Alternative Title	A title by which the work is commonly referred, or an abbreviation of the title.		text	2		FALSE	FALSE	FALSE	FALSE	FALSE	FALSE		citation
	otherId	Other ID	Another unique identifier that identifies this Dataset (e.g., producer's or another repository's number).		none	3	:	FALSE	FALSE	TRUE	FALSE	FALSE	FALSE		citation
	otherIdAgency	Agency	Name of agency which generated this identifier.		text	4	#VALUE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	otherId	citation
	otherIdValue	Identifier	Other identifier that corresponds to this Dataset.		text	5	#VALUE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	otherId	citation
	author	Author	The person(s), corporate body(ies), or agency(ies) responsible for creating the work.		none	6		FALSE	FALSE	TRUE	FALSE	TRUE	FALSE		citation""".split('\n')

    tsv_dir = 'tsv_files'
    fnames = [ (x, join(tsv_dir, x)) for x in os.listdir(tsv_dir) if x.endswith('.tsv')]
    fnames = [ x for x in fnames if isfile(x[1])]
    for tsv_fname, tsv_fullname in fnames:
        mr = MetadataReader(tsv_fullname)
        mr.read_metadata()
        mr.show()

    #tsv_name = 'tsv_files/citation.tsv'
    #tsv_name = 'tsv_files/biomedical.tsv'


    #mr = MetadataReader(tsv_name)
    #mr.read_metadata()
    #mr.show()
    """
    for test_line in test_lines:
        ml = MetadataLine(test_line)
        ml.as_json()
        ml.show()
    """
