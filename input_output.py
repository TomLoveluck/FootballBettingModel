import csv


class InputReader(object):
    """A class which reads csv data from file"""
    def __init__(self, read_file_path):
        self.read_file_path = read_file_path
        self.reader = csv.DictReader(open(self.read_file_path, 'r'))

    def __iter__(self):
        return self.reader

    def __next__(self):
        """Returns dictionary representation of next row before
        returning a StopIteration exception after final row"""
        yield self.reader.__next__()


class OutputWriter(object):
    """A class which writes features to a csv file"""
    def __init__(self, write_file_path, fieldnames):
        self.write_file_path = write_file_path
        self.writer = csv.DictWriter(open(self.write_file_path, 'w'), fieldnames=fieldnames)
        self.writer.writeheader()

    def write_features(self, feature_dict):
        """Writes additional rows to file"""
        self.writer.writerow(feature_dict)
