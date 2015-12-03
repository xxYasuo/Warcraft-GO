"""Module which forces all items to return a Model instance."""

from engines.precache import Model

##
## PRECACHE MODELS
##

class _models(dict):
	def __missing__(self, item):
		self[item] = Model(item)
		return self[item]
models = _models()