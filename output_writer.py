import csv

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
