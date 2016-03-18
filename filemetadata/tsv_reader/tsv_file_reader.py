"""
Read in Dataverse TSV files
    Examples: https://github.com/IQSS/dataverse/tree/develop/scripts/api/data/metadatablocks
"""
import csv
from os.path import isfile, isdir, join
import csv
import json

def msg(m): print m
def dashes(): msg('-' * 40)
def msgt(m): dashes(); msg(m); dashes()

FIELD_NAMES = """datasetField name title description watermark  fieldType displayOrder displayFormat advancedSearchField allowControlledVocabulary allowmultiples facetable showabovefold required parent metadatablock_id""".split()

class MetadataLine(object):

    def __init__(self, line):

        line_items = line.split('\t')
        self.init_fields(line)

    def init_fields(self, line):
        line_items = line.split('\t')

        for idx, field_name in enumerate(FIELD_NAMES):

            if idx < len(line_items):
                val = self.format_val(line_items[idx])
            else:
                val = None
            self.__dict__[field_name] = val

    def format_val(self, val):
        if val is None:
            return None

        val = val.strip()
        if len(val) == 0:
            return None

        if val == "FALSE":
            return False

        if val == "TRUE":
            return True

        return val

    def show(self):

        msgt('field vals')
        for idx, field_name in enumerate(FIELD_NAMES):
            msg('%s: %s' % (field_name, self.__dict__[field_name]))

    def as_json(self):
        print json.dumps(self.__dict__, indent=4)

class MetadataReader(object):

    def __init__(self, fname):
        assert isfile(fname), "File not found: %s" % fname

        self.fname = fname

if __name__ == '__main__':
    test_lines = """#datasetField	title	Title	Full title by which the Dataset is known.	Enter title...	text	0
#datasetField	subtitle	Subtitle	A secondary title used to amplify or state certain limitations on the main title.		text	1
#datasetField	alternativeTitle	Alternative Title	A title by which the work is commonly referred, or an abbreviation of the title.		text	2
#datasetField	otherId	Other ID	Another unique identifier that identifies this Dataset (e.g., producer's or another repository's number).		none	3	:
#datasetField	otherIdAgency	Agency	Name of agency which generated this identifier.		text	4	#VALUE
#datasetField	otherIdValue	Identifier	Other identifier that corresponds to this Dataset.		text	5	#VALUE
#datasetField	author	Author	The person(s), corporate body(ies), or agency(ies) responsible for creating the work.		none	6
#datasetField	authorName	Name	The author's Family Name, Given Name or the name of the organization responsible for this Dataset.	FamilyName, GivenName or Organization	text	7	#VALUE
#datasetField	authorAffiliation	Affiliation	The organization with which the author is affiliated.		text	8	(#VALUE)
#datasetField	authorIdentifierScheme	Identifier Scheme	Name of the identifier scheme (ORCID, ISNI).		text	9	- #VALUE:
#datasetField	authorIdentifier	Identifier	Uniquely identifies an individual author or organization, according to various schemes.		text	10	#VALUE
#datasetField	datasetContact	Contact	The contact(s) for this Dataset.		none	11
#datasetField	datasetContactName	Name	The contact's Family Name, Given Name or the name of the organization.	FamilyName, GivenName or Organization	text	12	#VALUE
#datasetField	datasetContactAffiliation	Affiliation	The organization with which the contact is affiliated.		text	13	(#VALUE)
#datasetField	datasetContactEmail	E-mail	The e-mail address(es) of the contact(s) for the Dataset. This will not be displayed.		email	14	#EMAIL""".split('\n')

    for test_line in test_lines:
        ml = MetadataLine(test_line)
        ml.as_json()
        ml.show()
