from feature_builder import SampleDecayFeatureBuilder

class FeatureManger(object):

    def __init__(self):
        self.initialise_feature_builders()

    def initialise_feature_builders(self):
        """Initialises feature builders"""
        self.home_goals_td = SampleDecayFeatureBuilder("state1", 2)
        self.away_goals_td = SampleDecayFeatureBuilder("state2", 2)

    def update_state(self, event):
        """Updates feature builder state"""
        # extract useful information from event
        home_team = event['HomeTeam']
        away_team = event['AwayTeam']
        home_goals = float(event['FTHG'])
        away_goals = float(event['FTAG'])

        # update state
        self.home_goals_td.update_state(home_team, home_goals)
        self.away_goals_td.update_state(away_team, away_goals)

    def extract_feature_dict(self, event):
        """Extracts feature values"""
        # extract useful information from event
        home_team = event['HomeTeam']
        away_team = event['AwayTeam']

        output_dict = dict()

        output_dict['home_team'] = home_team
        output_dict['home_goals_sum'] = self.home_goals_td.get_sum(home_team)

        output_dict['away_team'] = away_team
        output_dict['away_goals_sum'] = self.away_goals_td.get_sum(away_team)

        return output_dict
