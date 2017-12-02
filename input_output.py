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


class OutputWriter(object):
    """A class which writes features to a csv file"""
    def __init__(self, write_filepath, fieldnames):
        self.write_filepath = write_filepath
        self.writer = self._create_writer(fieldnames)
        self.writer.writeheader()

    def _create_writer(self, fieldnames):
        """Creates DictWriter object"""
        csvfile = open(self.write_filepath, 'w')
        return csv.DictWriter(csvfile, fieldnames=fieldnames)

    def write_features(self, feature_dict):
        """Writes additional rows to file"""
        self.writer.writerow(feature_dict)
