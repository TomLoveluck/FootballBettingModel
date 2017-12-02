import csv

class InputReader(object):
    """A class which reads csv data from file"""
    def __init__(self, read_filepath):
        self.read_filepath = read_filepath
        self.reader = self._create_reader()

    def _create_reader(self):
        """Creates DictReader object"""
        csvfile = open(self.read_filepath, 'r')
        return csv.DictReader(csvfile)

    def get_next_event(self):
        """Returns dictionary representation of next row before
        returning a StopIteraction exception after final row"""
        return self.reader.__next__()
