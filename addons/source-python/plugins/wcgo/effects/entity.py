"""Effects sub module to extend Source.Python's Entity class."""

# Source.Python
import entities


class Entity(entities.entity.Entity):
    """Entity with safe methods to make sure the entity exists."""
    
    def __init__(self, index):
        """Initialize a new entity and store his ehandle."""
        super().__init__(index)
        self._ehandle = self.get_ref_ehandle()

    def is_valid(self):
        """Use the ehandle to see if the entity is still valid."""
        return self._ehandle.is_valid()

    def add_output_safe(self, statement):
        """Safely add an output to the entity."""
        if self.is_valid():
            self.add_output(statement)

    def call_input_safe(self, statement):
        """Safely call an input on the entity."""
        if self.is_valid():
            self.call_input(statement)
