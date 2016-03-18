"""
Read in Dataverse TSV files
    Examples: https://github.com/IQSS/dataverse/tree/develop/scripts/api/data/metadatablocks
"""
import csv
from os.path import isfile, isdir, join
import csv

def msg(m): print m
def dashes(): msg('-' * 40)
def msgt(m): dashes(); msg(m); dashes()

FIELD_NAMES = """datasetField name title description watermark  fieldType displayOrder displayFormat advancedSearchField allowControlledVocabulary allowmultiples facetable showabovefold required parent metadatablock_id""".split()

class MetadataLine(object):

    def __init__(self, line):
        self.line_items = line.split('\t')
        for idx, field_name in enumerate(FIELD_NAMES):

            if idx < len(self.line_items):
                val = self.line_items[idx]
            else:
                val = None
            self.__dict__[field_name] = val

    def show(self):

        msgt('field vals')
        for idx, field_name in enumerate(FIELD_NAMES):
            msg('%s: %s' % (field_name, self.__dict__[field_name]))

class MetadataReader(object):

    def __init__(self, fname):
        assert isfile(fname), "File not found: %s" % fname

        self.fname = fname

if __name__ == '__main__':
    test_lines = """	title	Title	Full title by which the Dataset is known.	Enter title...	text	0		TRUE	FALSE	FALSE	FALSE	TRUE	TRUE		citation
	subtitle	Subtitle	A secondary title used to amplify or state certain limitations on the main title.		text	1		FALSE	FALSE	FALSE	FALSE	FALSE	FALSE		citation
	alternativeTitle	Alternative Title	A title by which the work is commonly referred, or an abbreviation of the title.		text	2		FALSE	FALSE	FALSE	FALSE	FALSE	FALSE		citation
	otherId	Other ID	Another unique identifier that identifies this Dataset (e.g., producer's or another repository's number).		none	3	:	FALSE	FALSE	TRUE	FALSE	FALSE	FALSE		citation
	otherIdAgency	Agency	Name of agency which generated this identifier.		text	4	#VALUE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	otherId	citation""".split('\n')

    for test_line in test_lines:
        ml = MetadataLine(test_line)
        ml.show()
