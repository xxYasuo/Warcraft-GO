"""This module contains cooldown decorators."""

# Python 3
import time

# Source.Python
from messages import SayText2


class UnboundCooldownMethod:
    """Decorator for the unbound methods of classes."""

    def __init__(self, func, cdkey, message, bound_type=None):
        """Initialize a new unbound cooldown method."""
        self._func = func
        self._cdkey = cdkey  # `duration` or `cd_func` based on `bound_type`
        if isinstance(message, str):
            message = SayText2(message)
        self.message = message
        self._bound_type = bound_type
        self._bindings = {}

    def __get__(self, obj, objtype=None):
        """Bind the object to a bound cooldown method."""
        if obj is None:
            return self
        bound_method = self._bindings.get(id(obj), None)
        if bound_method is None:
            bound_method = self._bindings[id(obj)] = self._bound_type(obj, self)
        return bound_method


class _BoundCooldownMethod:
    """Base class for all bound cooldown methods."""

    def __init__(self, skill, unbound):
        """Initialize a new bound cooldown method."""
        self._skill = skill
        self._unbound = unbound
        self._last_cooldown = 0
        self._start_time = 0

    def __del__(self):
        """Delete the reference from the unbound method."""
        if id(self) in self._unbound._bindings:
            del self._unbound._bindings[id(self)]

    def __getattr__(self, attr):
        """Attempt to get the unbound method's attribute."""
        return self._unbound.__getattribute__(attr)

    def _get_new_cd(self, **eargs):
        """Get the new cooldown for the method."""
        raise NotImplementedError(
            "CooldownMethod classes must implement a way of getting cooldown")

    @property
    def cooldown(self):
        """Get the maximum cooldown of the method."""
        return self._last_cooldown if self._last_cooldown > 0 else 0

    @property
    def remaining_cooldown(self):
        """Get the reaminign cooldown of the method."""
        remaining = self.cooldown - (time.time() - self._start_time)
        return remaining if remaining > 0 else 0

    @remaining_cooldown.setter
    def remaining_cooldown(self, value):
        """Set the remaining cooldown of the method."""
        self._start_time = time.time() - (self.cooldown - value)

    def __call__(self, **eargs):
        """Call the method. Sends a message if still on cooldown."""
        if self.remaining_cooldown == 0:
            new_cd = self._get_new_cd(**eargs)
            self.remaining_cooldown = self._last_cooldown = new_cd
            return self._func(self._skill, **eargs)
        else:
            self._send_message(eargs['player'].index)

    def _send_message(self, player_index):
        """Send the message to a player."""
        if self.message is not None:
            self.message.send(
                player_index, 
                skill_name=self._skill.name,
                remaining_cd=self.remaining_cooldown,
                maximum_cd=self.cooldown)


class StaticCooldownMethod(_BoundCooldownMethod):
    """CooldownMethod with an integer as cooldown."""

    def _get_new_cd(self, **eargs):
        """Get the static cooldown as an integer."""
        return self._cdkey

    @_BoundCooldownMethod.cooldown.setter
    def cooldown(self, value):
        """Set the cooldown to something else."""
        self._cdkey = value


class DynamicCooldownMethod(_BoundCooldownMethod):
    """CooldownMethod with a function for getting the cooldown."""

    def _get_new_cd(self, **eargs):
        """Get the cooldown by calling the cooldown function."""
        return self._cdkey(self._skill, **eargs)


def cooldownf(cd_func, message=None):
    """Decorate a function so it can only be called after a cooldown.
    
    Uses a function to dynamically get the cooldown on every call.
    """
    def decorator(func):
        return UnboundCooldownMethod(
            func, cd_func, message, DynamicCooldownMethod)
    return decorator


def cooldown(duration, message=None):
    """Decorate a function so it can only be called after a cooldown.
    
    Uses a static duration as the cooldown.
    """
    def decorator(func):
        return UnboundCooldownMethod(
            func, duration, message, StaticCooldownMethod)
    return decorator