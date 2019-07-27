from logbook import ERROR, WARNING, INFO
from logbook.more import ColorizedStderrHandler as _ColorizedStderrHandler


class ColorizedStderrHandler(_ColorizedStderrHandler):
    def get_color(self, record):
        """Returns the color for this record."""
        if record.level >= ERROR:
            return 'darkred'
        elif record.level >= WARNING:
            return 'darkyellow'
        elif record.level >= INFO:
            return 'darkgreen'
        return 'lightgray'
