import csv

class InputReader(object):
    """A class which reads csv data from file"""
    def __init__(self, read_filepath):
        self.read_filepath = read_filepath
        self.reader = csv.DictReader(open(self.read_filepath, 'r'))

    def __iter__(self):
        return self

    def __next__(self):
        """Returns dictionary representation of next row before
        returning a StopIteraction exception after final row"""
        yield self.reader.__next__()


class OutputWriter(object):
    """A class which writes features to a csv file"""
    def __init__(self, write_filepath, fieldnames):
        self.write_filepath = write_filepath
        self.writer = csv.DictWriter(open(self.write_filepath, 'w'), fieldnames=fieldnames)
        self.writer.writeheader()

    def write_features(self, feature_dict):
        """Writes additional rows to file"""
        self.writer.writerow(feature_dict)
