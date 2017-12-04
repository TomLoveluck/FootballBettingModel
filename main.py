"""
main.py loads in data using the InputReader class,
calculates the features using the FeatureManager classs and
writes the output to file using the OutputWriter class
"""
from datetime import datetime

from feature_manager import FeatureManger
from input_output import InputReader, OutputWriter


# CONSTANTS
READ_FILEPATH = "data/Football_data.csv"
OUTPUT_FILEPATH = "data/Features.csv"

# Initialise important classes
input_reader = InputReader(READ_FILEPATH)
feature_manager = FeatureManger()

output_features = feature_manager.get_all_feature_names() + ['Date','HomeResult','AwayResult','HomeTeam','AwayTeam']
output_writer = OutputWriter(OUTPUT_FILEPATH, output_features)

# read data from file using iterable interface of InputReader class
for event in input_reader:

        # pre features extraction state updates
        feature_manager.pre_extraction_updates(event)

        # use FeatureManager to extract feature values before match
        feature_dict = feature_manager.extract_feature_dict(event)

        # post features extraction state updates
        feature_manager.post_extraction_updates(event)

        # addition of extra fields to output
        feature_dict['Date'] = datetime.strptime(event['Date'], "%d/%m/%y")
        feature_dict['HomeResult'] = event['FTHG']
        feature_dict['AwayResult'] = event['FTAG']
        feature_dict['HomeTeam'] = event['HomeTeam']
        feature_dict['AwayTeam'] = event['AwayTeam']

        # write output to file
        output_writer.write_features(feature_dict)

