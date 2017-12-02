"""Feature builder classes"""

import math
from datetime import datetime
from state_manager import StateManger

class TimeDecayFeatureBuilder(object):
    """ Calculates time decayed sum and count """
    def __init__(self, state_id, decay_rate_days):
        """Instance initiated with state_id and decay_rate_days"""
        self.state_id = state_id
        self.create_state_repo()
        self.decay_rate_days = decay_rate_days

    def create_state_repo(self):
        """State location created for instance state"""
        self.sample_decay_rate = StateManger(self.state_id)

    def initialise_state(self, entity_id):
        """Sum, count and last_update state initiated as 0. and 0. and 1970-01-01"""
        initial_state = {"count": 0., "sum": 0.,
                         "last_update":datetime.strptime("1970-01-01", "%Y-%m-%d")}
        self.sample_decay_rate.write_state(entity_id, initial_state)

    def update_state(self, entity_id, amount, new_datetime):
        """Updates sum and count state"""
        # if state missing, initialise state
        if self.sample_decay_rate.entity_state_missing(entity_id):
            self.initialise_state(entity_id)
        # read state using state manager
        state = self.sample_decay_rate.read_state(entity_id)
        # edit state
        days_since_last_update = (new_datetime - state["last_update"]).days
        decay_factor = math.exp(- (days_since_last_update / self.decay_rate_days))
        state['count'] = (state['count'] * decay_factor) + 1
        state['sum'] = (state['sum'] * decay_factor) + amount
        # write state using state manager
        self.sample_decay_rate.write_state(entity_id, state)

    def get_count(self, entity_id):
        """Return count state"""
        return self.sample_decay_rate.read_state(entity_id)["count"]

    def get_sum(self, entity_id):
        """Return sum state"""
        return self.sample_decay_rate.read_state(entity_id)["sum"]

class SampleDecayFeatureBuilder(object):
    """ Calculates sample decayed sum and count """
    def __init__(self, state_id, sample_decay_rate):
        """Instance initiated with state_id and sample_decay_rate"""
        self.state_id = state_id
        self.sample_decay_rate = sample_decay_rate
        self.create_state_repo()

    def create_state_repo(self):
        """State location created for instance state"""
        self.state_manager = StateManger(self.state_id)

    def initialise_state(self, entity_id):
        """Sum and count state initiated as 0. and 0."""
        initial_state = {"count": 0., "sum": 0.}
        self.state_manager.write_state(entity_id, initial_state)

    def update_state(self, entity_id, amount):
        """Updates sum and count state"""
        # if state missing, initialise state
        if self.state_manager.entity_state_missing(entity_id):
            self.initialise_state(entity_id)
        # read state using state manager
        state = self.state_manager.read_state(entity_id)
        # edit state
        decay_factor = math.exp(- (1 / self.sample_decay_rate))
        state['count'] = (state['count'] * decay_factor) + 1
        state['sum'] = (state['sum'] * decay_factor) + amount
        # write state using state manager
        self.state_manager.write_state(entity_id, state)

    def get_count(self, entity_id):
        """Return count state"""
        return self.state_manager.read_state(entity_id)["count"]

    def get_sum(self, entity_id):
        """Return sum state"""
        return self.state_manager.read_state(entity_id)["sum"]
