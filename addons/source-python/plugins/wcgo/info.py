"""Stores information about the plugin."""

# Source.Python
from cvars.flags import ConVarFlags
from cvars.public import PublicConVar
from plugins.info import PluginInfo

info = PluginInfo()
info.name = "Warcraft-GO"
info.author = "Warcraft-GO-Team"
info.version = ""
info.basename = "wcgo"
info.url = ""
info.convar = PublicConVar(
    info.basename + "_version", info.version, info.name + ' Version')
