from featurebuilders.decay import SampleDecayFeature, TimeDecayFeature
from featurebuilders.simple import ValueLastMatchFeature

class FeatureManger(object):

    def __init__(self):
        self.initialise_feature_builders()

    def initialise_feature_builders(self):
        """Initialises feature builders"""

        # home and away team goals scored and conceded sd features
        decay_rate = 10
        home_team_goals_scored_sd = SampleDecayFeature(
            feature_name="home_team_goals_scored_sd",
            entity_field="HomeTeam",
            sum_value_field="FTHG",
            incl_count=False, incl_sum=False, incl_mean=True,
            decay_rate=decay_rate)

        home_team_goals_conceded_sd = SampleDecayFeature(
            feature_name="home_goals_conceded_sd",
            entity_field="HomeTeam",
            sum_value_field="FTAG",
            incl_count=False, incl_sum=False, incl_mean=True,
            decay_rate=decay_rate)

        away_team_goals_scored_sd = SampleDecayFeature(
            feature_name="away_team_goals_scored_sd",
            entity_field="AwayTeam",
            sum_value_field="FTAG",
            incl_count=False, incl_sum=False, incl_mean=True,
            decay_rate=decay_rate)

        away_team_goals_conceded_sd = SampleDecayFeature(
            feature_name="away_team_goals_conceded_sd",
            entity_field="AwayTeam",
            sum_value_field="FTHG",
            incl_count=False, incl_sum=False, incl_mean=True,
            decay_rate=decay_rate)


        # last match scores
        home_team_last_home_score = ValueLastMatchFeature(
            field_name="FTHG", entity_field="HomeTeam",
            feature_name="home_team_last_home_score")

        home_team_last_away_score = ValueLastMatchFeature(
            field_name="FTAG", entity_field="HomeTeam",
            feature_name="home_team_last_away_score")

        away_team_last_home_score = ValueLastMatchFeature(
            field_name="FTHG", entity_field="AwayTeam",
            feature_name="away_team_last_home_score")

        away_team_last_away_score = ValueLastMatchFeature(
            field_name="FTAG", entity_field="AwayTeam",
            feature_name="away_team_last_away_score")

        self.feature_builders = [home_team_goals_scored_sd,
                                 home_team_goals_conceded_sd,
                                 away_team_goals_scored_sd,
                                 away_team_goals_conceded_sd,
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
