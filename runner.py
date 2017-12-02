"""
runner.py loads in data using the InputReader class,
calculates the features using the FeatureManager classs and
writes the output to file using the OutputWriter class
"""

from input_reader import InputReader
from feature_manager import FeatureManger
from output_writer import OutputWriter

# CONSTANTS
READ_FILEPATH = "data/Data.csv"
OUTPUT_FILEPATH = "data/Features.csv"
FEATURES = ['home_team', 'home_goals_sum', 'away_team', 'away_goals_sum']

# Initialise important classes
IR = InputReader(READ_FILEPATH)
FM = FeatureManger()
OW = OutputWriter(OUTPUT_FILEPATH, FEATURES)

# read data from file using InputReader class
try:
    while True:
        # read event from file
        event = IR.get_next_event()

        # use FeatureManager class to update state and extract feature dict
        FM.update_state(event)
        feature_dict = FM.extract_feature_dict(event)

        # write output to file
        OW.write_features(feature_dict)

except StopIteration:
    pass
