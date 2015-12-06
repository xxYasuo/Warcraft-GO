"""Contains strings for all non-menu related messages."""

# Source.Python
from messages import SayText2
from messages import HintText
from translations.strings import LangStrings

# Warcraft: GO
import wcgo.configs as cfg
from wcgo.info import info


MESSAGES = LangStrings(info.basename)


def chat_message(player_index, msg_id, kwargs):
    """Send a message to a player using SayText2."""
    msg = MESSAGES[msg_id].format(**kwargs)
    msg = cfg.message_template.format(msg)
    SayText2(msg).send(player_index)


def hint_message(player_index, msg_id, kwargs):
    """Send a message to a player using HintText."""
    msg = MESSAGES[msg_id].format(**kwargs)
    HintText(msg).send(player_index)
