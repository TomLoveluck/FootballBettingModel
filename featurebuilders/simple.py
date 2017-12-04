"""Simple feature builder classes"""

from state_manager import StateManager


class ValueLastMatchFeature(object):
    """Extract transient feature from previous event"""
    def __init__(self, field_name, entity_field, feature_name):
        self.field_name = field_name
        self.entity_field = entity_field
        self.feature_name = feature_name
        self.create_state_repo()

    def create_state_repo(self):
        """State location created for instance state"""
        self.state_manager = StateManager()

    def initialise_state(self, entity_id):
        """Sum and count state initiated as 0. and 0."""
        self.state_manager.write(entity_id, None)

    def get_feature_names(self):
        """Return feature name"""
        return [self.feature_name]

    def pre_extraction_update(self, event):
        pass

    def extract_feature_dict(self, event):
        # if state missing, initialise state
        entity_id = event[self.entity_field]
        if self.state_manager.entity_missing(entity_id):
            self.initialise_state(entity_id)
        return {self.feature_name: self.state_manager.read(entity_id)}

    def post_extraction_update(self, event):
        self.state_manager.write(event[self.entity_field], event[self.field_name])

