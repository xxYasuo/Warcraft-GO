"""Contains strings for all non-menu related messages."""

# Source.Python
from messages import SayText2
from messages import HintText
from translations.strings import LangStrings

# Warcraft: GO
from wcgo.info import info


EXPERIENCE_MESSAGES = LangStrings(info.basename + '/experience_strings')


def chat_message(player_index, msg_id, **kwargs):
    """Send a message to a player using SayText2."""
    SayText2(EXPERIENCE_MESSAGES[msg_id]).send(player_index, **kwargs)


def hint_message(player_index, msg_id, **kwargs):
    """Send a message to a player using HintText."""
    HintText(EXPERIENCE_MESSAGES[msg_id]).send(player_index, **kwargs)
