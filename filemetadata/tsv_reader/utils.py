

class FormatHelper(object):

    @staticmethod
    def format_val(val):
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
