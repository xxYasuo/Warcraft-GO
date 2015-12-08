"""Effects sub module to extend Source.Python's Entity class."""

# Source.Python
import entities


class Entity(entities.entity.Entity):
    '''Subclassing Entity to ensure input and outputs
    are never called when entity doesn't exist.'''
    def __init__(self, index):
        super().__init__(index)
        self._ehandle = self.get_ref_ehandle()

    def is_valid(self):
        return self._ehandle.is_valid()

    def add_output_safe(self, statement):
        if self.is_valid():
            self.add_output(statement)

    def call_input_safe(self, statement):
        if self.is_valid():
            self.call_input(statement)