from featurebuilders.decay import SampleDecayFeatureBuilder, TimeDecayFeatureBuilder
from featurebuilders.simple import ValueLastMatchFeatureBuilder

class FeatureManger(object):

    def __init__(self):
        self.initialise_feature_builders()

    def initialise_feature_builders(self):
        """Initialises feature builders"""

        # home goals sample decay feature
        home_goals_sd = SampleDecayFeatureBuilder(
            feature_name="home_goals_sd",
            entity_field="HomeTeam",
            sum_value_field="FTHG",
            incl_count=False, incl_sum=False, incl_mean=True,
            decay_rate=3)

        home_goals_td = TimeDecayFeatureBuilder(
            feature_name="home_goals_td",
            entity_field="HomeTeam",
            sum_value_field="FTHG",
            incl_count=False, incl_sum=False, incl_mean=True,
            decay_rate=30)

        # away goals sample decay feature
        away_goals_sd = SampleDecayFeatureBuilder(
            feature_name="away_goals_sd",
            entity_field="AwayTeam",
            sum_value_field="FTAG",
            incl_count=False, incl_sum=False, incl_mean=True,
            decay_rate=3)

        away_goals_td = TimeDecayFeatureBuilder(
            feature_name="away_goals_td",
            entity_field="AwayTeam",
            sum_value_field="FTAG",
            incl_count=False, incl_sum=False, incl_mean=True,
            decay_rate=30)

        home_team_last_home_score = ValueLastMatchFeatureBuilder(
            field_name="FTHG", entity_field="HomeTeam",
            feature_name="home_team_last_home_score")

        home_team_last_away_score = ValueLastMatchFeatureBuilder(
            field_name="FTAG", entity_field="HomeTeam",
            feature_name="home_team_last_away_score")

        away_team_last_home_score = ValueLastMatchFeatureBuilder(
            field_name="FTHG", entity_field="AwayTeam",
            feature_name="away_team_last_home_score")

        away_team_last_away_score = ValueLastMatchFeatureBuilder(
            field_name="FTAG", entity_field="AwayTeam",
            feature_name="away_team_last_away_score")

        self.feature_builders = [home_goals_td,
                                 home_goals_sd,
                                 away_goals_td,
                                 away_goals_sd,
                                 home_team_last_home_score,
                                 home_team_last_away_score,
                                 away_team_last_home_score,
                                 away_team_last_away_score]

    def get_all_feature_names(self):
        """Get complete list of feature names"""
        feature_names = []
        for feature_builder in self.feature_builders:
            feature_names.extend(feature_builder.get_feature_names())
        return feature_names

    def pre_extraction_updates(self, event):
        """pre_extraction_updates"""
        for feature_builder in self.feature_builders:
            feature_builder.pre_extraction_update(event)

    def extract_feature_dict(self, event):
        """extract_feature_dict"""
        output_features = dict()
        for feature_builder in self.feature_builders:
            output_features.update(feature_builder.extract_feature_dict(event))
        return output_features

    def post_extraction_updates(self, event):
        """post_extraction_updates"""
        for feature_builder in self.feature_builders:
            feature_builder.post_extraction_update(event)
