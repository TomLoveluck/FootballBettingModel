"""
main.py loads in data using the InputReader class,
calculates the features using the FeatureManager classs and
writes the output to file using the OutputWriter class
"""
from datetime import datetime

from input_output import InputReader, OutputWriter
from feature_manager import FeatureManger

# CONSTANTS
READ_FILEPATH = "data/Data.csv"
OUTPUT_FILEPATH = "data/Features.csv"

# Initialise important classes
IR = InputReader(READ_FILEPATH)
FM = FeatureManger()

output_features = FM.get_all_feature_names() + ['Date','HomeResult','AwayResult']
OW = OutputWriter(OUTPUT_FILEPATH, output_features)

# read data from file using InputReader class
try:
    while True:
        # read event from file
        event = IR.get_next_event()

        # pre features extraction state updates
        FM.pre_extraction_updates(event)

        # use FeatureManager to extract feature values before match
        feature_dict = FM.extract_feature_dict(event)

        # post features extraction state updates
        FM.post_extraction_updates(event)

        # addition of extra fields to output
        feature_dict['Date'] = datetime.strptime(event['Date'], "%d/%m/%y")
        feature_dict['HomeResult'] = event['FTHG']
        feature_dict['AwayResult'] = event['FTAG']

        # write output to file
        OW.write_features(feature_dict)

except StopIteration:
    pass
