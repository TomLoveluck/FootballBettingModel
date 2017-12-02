

class StateManger(object):
    """A class which manages the state used by the feature builders"""
    def __init__(self, state_id):
        self.state_id = state_id
        self.state_dict = {}

    def read_state(self, entity_id):
        """Reads state from state_dict"""
        return self.state_dict[entity_id]

    def write_state(self, entity_id, updated_state):
        """Writes state to state dict"""
        self.state_dict[entity_id] = updated_state

    def entity_state_missing(self, entity_id):
        """Returns true when entity_id missing froms state_dict"""
        return entity_id not in self.state_dict
