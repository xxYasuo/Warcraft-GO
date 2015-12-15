"""Contains strings for all non-menu related messages."""

# Source.Python
from messages import SayText2
from messages import HintText
from translations.strings import LangStrings

# Warcraft: GO
from wcgo.info import info


def _get_messages(translation_file, message_cls):
    """Get a dict of messages from a translation file."""
    lang_strings = LangStrings(info.basename + '/' + translation_file)
    return {key: message_cls(value) for key, value in lang_strings.items()}

# Globals
misc_messages = _get_messages('misc_messages', SayText2)
xp_messages = _get_messages('xp_messages', HintText)
menu_messages = _get_messages('menu_messages', SayText2)
menu_options = LangStrings(info.basename + '/menu_options')
