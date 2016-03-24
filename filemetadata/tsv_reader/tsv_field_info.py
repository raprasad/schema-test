"""
Store Info on a Metadata line based on a Dataverse TSV files
    Examples: https://github.com/IQSS/dataverse/tree/develop/scripts/api/data/metadatablocks
"""
import sys
from os.path import isfile, isdir, join
import csv
import json
from collections import OrderedDict
from static_values import FIELD_NAMES, DELIMITER
from utils import FormatHelper

def msg(m): print m
def dashes(): msg('-' * 40)
def msgt(m): dashes(); msg(m); dashes()
def msgx(m): msgt(m); sys.exit(0)


class MetadataLine(object):

    def __init__(self, line):

        self.init_fields(line)
        self.vocabinfo_list = None # [VocabInfo, VocabInfo, VocabInfo]
        self.children = []  # map be a parent

    def get_vocab_values_only(self):
        if not self.vocabinfo_list or\
            len(self.vocabinfo_list) == 0:
            return None

        # Iterate through VocabInfo objects
        vocab_values = [x.value for x in self.vocabinfo_list]
        return vocab_values


    def get_vocab_values(self, as_list=False):
        if not self.vocabinfo_list or\
            len(self.vocabinfo_list) == 0:
            return None

        if as_list:
            return [v.as_dict() for v in self.vocabinfo_list]

        # Iterate through VocabInfo objects
        vocab_values = [x.value for x in self.vocabinfo_list]
        return vocab_values


    def init_fields(self, line):
        line_items = line.split('\t')

        for idx, field_name in enumerate(FIELD_NAMES):

            if idx < len(line_items):
                val = FormatHelper.format_val(line_items[idx])
            else:
                val = None
            self.__dict__[field_name] = val

    def show(self):

        msgt('field vals')
        controlled_vocab = self.get_vocab_values()
        msgx('controlled_vocab: %s' %  controlled_vocab)
        show_list = FIELD_NAMES
        for idx, field_name in enumerate(show_list):
            msg('%s: %s' % (field_name, self.__dict__[field_name]))

        if controlled_vocab:
            msg('controlled_vocab: %s' % controlled_vocab)

    """
allowmultiples
"pets": {
      "type": "array",
      "format": "table",
      "title": "Pets",
      "uniqueItems": true,
      "items": {
        "type": "object",
        "title": "Pet",
        "properties": {
          "type": {
            "type": "string",
            "enum": [
              "cat",
              "dog",
              "bird",
              "reptile",
              "other"
            ],
            "default": "dog"
          },
          "name": {
            "type": "string"
          }
        }
      },
    """

    def as_basic_json_schema_property(self):
        """
        Definition of single field as a Python dict
        that matches the JSON schema
        """

        # basic params for a single field or subfield
        prop_dict = dict(title=self.title,\
                        description=self.description,\
                        propertyOrder=self.displayOrder,\
                        required=self.required,\
                        display_format=self.displayFormat\
                        )
        vocab_enum = self.get_vocab_values_only()
        if vocab_enum:
            prop_dict['enum'] = vocab_enum

        prop_type = self.get_json_schema_type()
        if prop_type:
            prop_dict.update(prop_type)

        return prop_dict

    def as_json_schema_property(self, as_json_string=False):

        val_dict = self.__dict__.copy()
        val_dict.pop('vocabinfo_list')
        val_dict['controlled_vocabulary'] =  self.get_vocab_values(as_list=True)

        if self.allowmultiples and len(self.children) > 0:
            # prepared individual fields "items"
            properties = OrderedDict()
            for child_info in self.children:
                msg('child info: %s' % child_info.name)
                properties[child_info.name] = child_info.as_basic_json_schema_property()

            prop_dict = OrderedDict(title=self.title,\
                        format="table",\
                        type="array",\
                        uniqueItems=True,\
                        description=self.description,\
                        items=OrderedDict(
                            type="object",\
                            title=self.title,\
                            properties=properties)
                        )
            return prop_dict
        else:
            return self.as_basic_json_schema_property()
        """
        elif self.allowmultiples:
            prop_dict = OrderedDict(title=self.title,\
                        format="table",\
                        type="array",\
                        uniqueItems=True,\
                        description=self.description,\
                        items=OrderedDict(
                            type="object",\
                            title=self.title,
                                properties=OrderedDict(type=OrderedDict(title=self.title,\
                                    #description=self.description,\
                                    propertyOrder=self.displayOrder,\
                                    required=self.required),\
                                )
                            #display_format=self.displayFormat\
                        ))
            vocab_enum = self.get_vocab_values_only()
            if vocab_enum:
                prop_dict['items']['properties']['type']['enum'] = vocab_enum

            prop_type = self.get_json_schema_type()
            if prop_type:
                prop_dict['items']['properties']['type'].update(prop_type)
            '''
            "type": "array",
            "format": "table",
            "title": "Pets",
            "uniqueItems": true,
            "items": {
              "type": "object",
              "title": "Pet",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "cat",
                    "dog",
                    "bird",
                    "reptile",
                    "other"
                  ],
                  "default": "dog"
                },
                "name": {
                  "type": "string"
                }
              }'''

        else:
            # basic params for a single field or subfield
            prop_dict = dict(title=self.title,\
                            description=self.description,\
                            propertyOrder=self.displayOrder,\
                            required=self.required,\
                            #display_format=self.displayFormat\
                            )
            vocab_enum = self.get_vocab_values_only()
            if vocab_enum:
                prop_dict['enum'] = vocab_enum

            prop_type = self.get_json_schema_type()
            if prop_type:
                prop_dict.update(prop_type)

        return prop_dict
        """
    def get_json_schema_type(self):

        type_string = dict(type='string')

        MAPPING_DICT = { 'text' : type_string,\
                    'int' : dict(type='integer'),\
                    'url' : dict(type='string', pattern=u'some pattern'),\
                    'date': dict(type='string',\
                        pattern=r'^(19|20)\d\d[\-\/.](0[1-9]|1[012])[\-\/.](0[1-9]|[12][0-9]|3[01])$'),\
                    'textbox' : type_string,\
                    'number' : dict(type='number'),\
                    }

        return MAPPING_DICT.get(self.fieldType, type_string)


    def as_dict(self, as_json_string=False):
        msgt('as_json')


        val_dict = self.__dict__.copy()
        val_dict.pop('vocabinfo_list')
        val_dict['controlled_vocabulary'] =  self.get_vocab_values(as_list=True)

        if as_json_string:
            return json.dumps(val_dict, indent=4)
        return val_dict
"""
{
  "title": "Person",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "First and Last name",
      "minLength": 4,
      "default": "Jeremy Dorn"
    },
    "age": {
      "type": "integer",
      "default": 25,
      "minimum": 18,
      "maximum": 99
    },
    "favorite_color": {
      "type": "string",
      "format": "color",
      "title": "favorite color",
      "default": "#ffa500"
    },
    "gender": {
      "type": "string",
      "enum": [
        "male",
        "female"
      ]
    },
    "location": {
      "type": "object",
      "title": "Location",
      "properties": {
        "city": {
          "type": "string",
          "default": "San Francisco"
        },
        "state": {
          "type": "string",
          "default": "CA"
        },
        "citystate": {
          "type": "string",
          "description": "This is generated automatically from the previous two fields",
          "template": ", ",
          "watch": {
            "city": "location.city",
            "state": "location.state"
          }
        }
      }
    },
    "pets": {
      "type": "array",
      "format": "table",
      "title": "Pets",
      "uniqueItems": true,
      "items": {
        "type": "object",
        "title": "Pet",
        "properties": {
      "type": {
            "type": "string",
            "enum": [
              "cat",
              "dog",
              "bird",
              "reptile",
              "other"
            ],
            "default": "dog"
          },
          "name": {
            "type": "string"
          }
        }
      },
      "default": [
        {
          "type": "dog",
          "name": "Walter"
        }
      ]
    }
  }
}"""
