"""Module which forces all items to return a Model instance."""

# Source.Python
from engines.precache import Model

# Warcraft: GO
import wcgo.utilities

# Globals
models = wcgo.utilities.KeyDefaultDict(Model)
