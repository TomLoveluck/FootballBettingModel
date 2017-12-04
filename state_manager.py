

class StateManager(object):
    """A class which manages the state used by the feature builders"""
    def __init__(self):
        self.state_dict = {}

    def read(self, entity_id):
        """Reads state from state_dict"""
        return self.state_dict[entity_id]

    def write(self, entity_id, updated_state):
        """Writes state to state dict"""
        self.state_dict[entity_id] = updated_state

    def entity_missing(self, entity_id):
        """Returns true when entity_id missing froms state_dict"""
        return entity_id not in self.state_dict
