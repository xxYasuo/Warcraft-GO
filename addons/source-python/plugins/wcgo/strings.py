"""Contains strings for all non-menu related messages."""

# Source.Python
from messages import SayText2

# Warcraft: GO
import wcgo.configs as cfg

def message(index, msg_id, cls=SayText2, use_template=True, **kwargs):
    cls(cfg.message_template.format(MESSAGES[msg_id].format(**kwargs))
        if use_template else MESSAGES[msg_id].format(**kwargs)
        ).send(index)

MESSAGES = {
    'Show XP': '\x04{hero} \x01- \x03LV {level} \x01- \x0b{xp}/{needed} XP',
    'Level Up': 'You\'ve reached \x03LV {level}\x01.',

    # HintText works with HTML codes
    'Kill': "<font color='#66FF66'>+{xp} XP for a kill.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Headshot': "<font color='#66FF66'>+{xp} XP for a headshot.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Assist': "<font color='#66FF66'>+{xp} XP for an assist.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Round Win': "<font color='#66FF66'>+{xp} XP for winning a round.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Round Loss': "<font color='#66FF66'>+{xp} XP for losing a round.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Bomb Plant': "<font color='#66FF66'>+{xp} XP for planting the bomb.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Bomb Plant Team': "<font color='#66FF66'>{xp} XP for bomb being planted.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Bomb Explode': "<font color='#66FF66'>{xp} XP for bomb XPloding.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Bomb Explode Team': "<font color='#66FF66'>{xp} XP for bomb XPloding.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Bomb Defuse': "<font color='#66FF66'>{xp} XP for defusing the bomb.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Bomb Defuse Team': "<font color='#66FF66'>{xp} XP for bomb being defused.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Hostage Pick Up': "<font color='#66FF66'>{xp} XP for picking up a hostage.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Hostage Pick Up Team': "<font color='#66FF66'>{xp} XP for a hostage being picked up.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Hostage Rescue': "<font color='#66FF66'>{xp} XP for rescuing a hostage.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
    'Hostage Rescue Team': "<font color='#66FF66'>{xp} XP for a hostage being rescued.</font>\n<center><font color='#3366FF'>{hero}: {current}/{needed} XP</font></center>",
}