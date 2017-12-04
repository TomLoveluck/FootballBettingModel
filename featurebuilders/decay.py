"""Sample and time decay feature builder classes"""

import math
from datetime import datetime
from state_manager import StateManager
from tools.numeric import safe_division


class DecayFeature(object):

    def __init__(self, feature_name, entity_field, sum_value_field, incl_count, incl_sum, incl_mean, decay_rate):
        """Instance initiated with state_id and sample_decay_rate"""
        self.feature_name = feature_name
        self.entity_field = entity_field
        self.sum_value_field = sum_value_field
        self.incl_count = incl_count
        self.incl_sum = incl_sum
        self.incl_mean = incl_mean
        self.decay_rate = decay_rate
        self.create_state_repo()

    def create_state_repo(self):
        """State location created for instance state"""
        self.state_manager = StateManager()

    def initialise_state(self, entity_id):
        raise Exception("Implementation missing")

    def get_feature_names(self):
        feature_names = []
        if self.incl_count: feature_names.append(self.feature_name + "_count")
        if self.incl_sum: feature_names.append(self.feature_name + "_sum")
        if self.incl_mean: feature_names.append(self.feature_name + "_mean")
        return feature_names

    def pre_extraction_update(self, event):
        raise Exception("Implementation missing")

    def extract_feature_dict(self, event):
        """Return feature dict state"""
        # read state using state manager
        state = self.state_manager.read(event[self.entity_field])
        feature_dict = {}
        if self.incl_count: feature_dict[self.feature_name + "_count"] = state['count']
        if self.incl_sum: feature_dict[self.feature_name + "_sum"] = state['sum']
        if self.incl_mean: feature_dict[self.feature_name + "_mean"] = safe_division(state['sum'], state['count'], 1.)
        return feature_dict


class SampleDecayFeature(DecayFeature):

    def initialise_state(self, entity_id):
        """Sum and count state initiated as 0. and 0."""
        initial_state = {"count": 0., "sum": 0.}
        self.state_manager.write(entity_id, initial_state)

    def pre_extraction_update(self, event):
        """Decay sum and count state"""
        # if state missing, initialise state
        entity_id = event[self.entity_field]
        if self.state_manager.entity_missing(entity_id):
            self.initialise_state(entity_id)
        # read state using state manager
        state = self.state_manager.read(entity_id)
        # decay state
        decay_factor = math.exp(- (1 / self.decay_rate))
        state['count'] = (state['count'] * decay_factor)
        state['sum'] = (state['sum'] * decay_factor)
        # write state using state manager
        self.state_manager.write(entity_id, state)

    def post_extraction_update(self, event):
        """Add to sum and count state"""
        # read state using state manager
        entity_id = event[self.entity_field]
        state = self.state_manager.read(entity_id)
        # add to state
        state['count'] += 1.
        state['sum'] += float(event[self.sum_value_field])
        # write state using state manager
        self.state_manager.write(entity_id, state)

    def extract_feature_dict(self, event):
        """Return feature dict state"""
        # read state using state manager
        state = self.state_manager.read(event[self.entity_field])
        feature_dict = {}
        if self.incl_count:
            feature_dict[self.feature_name + "_count"] = state['count']
        if self.incl_sum:
            feature_dict[self.feature_name + "_sum"] = state['sum']
        if self.incl_mean:
            feature_dict[self.feature_name + "_mean"] = safe_division(state['sum'], state['count'], 1.)
        return feature_dict


class TimeDecayFeature(DecayFeature):
    """ Calculates sample decayed sum, count and means"""

    def initialise_state(self, entity_id):
        """Sum and count state initiated as 0. and 0."""
        initial_state = {"count": 0., "sum": 0.,
                         "last_update": datetime.strptime("1970-01-01", "%Y-%m-%d")}
        self.state_manager.write(entity_id, initial_state)


    def pre_extraction_update(self, event):
        """Decay sum and count state"""
        # if state missing, initialise state
        entity_id = event[self.entity_field]
        if self.state_manager.entity_missing(entity_id):
            self.initialise_state(entity_id)
        # read state using state manager
        state = self.state_manager.read(entity_id)
        # decay state
        curr_date = datetime.strptime(event['Date'], "%d/%m/%y")
        days_since_last_update = (curr_date - state["last_update"]).days
        decay_factor = math.exp(- (days_since_last_update / self.decay_rate))
        state['count'] = (state['count'] * decay_factor)
        state['sum'] = (state['sum'] * decay_factor)
        # write state using state manager
        self.state_manager.write(entity_id, state)

    def post_extraction_update(self, event):
        """Add to sum and count state"""
        # read state using state manager
        entity_id = event[self.entity_field]
        state = self.state_manager.read(entity_id)
        # add to state
        state["count"] += 1.
        state["sum"] += float(event[self.sum_value_field])
        state["last_update"] = datetime.strptime(event['Date'], "%d/%m/%y")
        # write state using state manager
        self.state_manager.write(entity_id, state)