from static_values import VOCAB_FIELD_NAMES, DELIMITER
from utils import FormatHelper

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
                val = FormatHelper.format_val(line_items[idx])
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
