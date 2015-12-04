"""Contains strings for all non-menu related messages."""

# Source.Python
from messages import SayText2
from messages import HintText

# Warcraft: GO
import wcgo.configs as cfg


def chat_message(player_index, msg_id, kwargs):
    """Send a message to a player using SayText2."""
    msg = MESSAGES[msg_id].format(**kwargs)
    msg = cfg.message_template.format(msg)
    SayText2(msg).send(player_index)


def hint_message(player_index, msg_id, kwargs):
    """Send a message to a player using HintText."""
    msg = MESSAGES[msg_id].format(**kwargs)
    HintText(msg).send(player_index)


MESSAGES = {
    'Show XP': '\x04{hero.name} \x01- \x03Level {hero.level} \x01- \x0b{hero.xp}/{hero.required_xp} XP',
    'Level Up': 'You\'ve reached \x03level {level}\x01.',

    # HintText works with HTML codes
    'Kill': "<font color='#66FF66'>+{xp} XP for a kill.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Headshot': "<font color='#66FF66'>+{xp} XP for a headshot.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Assist': "<font color='#66FF66'>+{xp} XP for an assist.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Round Win': "<font color='#66FF66'>+{xp} XP for winning a round.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Round Loss': "<font color='#66FF66'>+{xp} XP for losing a round.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Bomb Plant': "<font color='#66FF66'>+{xp} XP for planting the bomb.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Bomb Plant Team': "<font color='#66FF66'>{xp} XP for bomb being planted.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Bomb Explode': "<font color='#66FF66'>{xp} XP for bomb XPloding.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Bomb Explode Team': "<font color='#66FF66'>{xp} XP for bomb XPloding.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Bomb Defuse': "<font color='#66FF66'>{xp} XP for defusing the bomb.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Bomb Defuse Team': "<font color='#66FF66'>{xp} XP for bomb being defused.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Hostage Pick Up': "<font color='#66FF66'>{xp} XP for picking up a hostage.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Hostage Pick Up Team': "<font color='#66FF66'>{xp} XP for a hostage being picked up.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Hostage Rescue': "<font color='#66FF66'>{xp} XP for rescuing a hostage.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
    'Hostage Rescue Team': "<font color='#66FF66'>{xp} XP for a hostage being rescued.</font>\n<center><font color='#3366FF'>{hero.name}: {hero.xp}/{hero.required_xp} XP</font></center>",
}