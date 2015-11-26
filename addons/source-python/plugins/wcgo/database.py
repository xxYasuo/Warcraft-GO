"""Module for dealing with Warcraft: GO database."""

# Python 3
import sqlite3

# Warcraft: GO
import wcgo.entities


class Database:
    """OOP implementation around sqlite3 databases for Warcraft: Go."""

    def __init__(self, path=':memory:'):
        """Initialize a new database connection."""
        self._path = path
        self.connection = sqlite3.connect(path)
        self.connection.execute('''CREATE TABLE IF NOT EXISTS players (
            steamid TEXT PRIMARY KEY,
            gold INTEGER,
            hero_clsid TEXT
        )''')
        self.connection.execute('''CREATE TABLE IF NOT EXISTS heroes (
            steamid TEXT,
            clsid TEXT,
            level INTEGER,
            xp INTEGER,
            PRIMARY KEY (steamid, clsid)
        )''')
        self.connection.execute('''CREATE TABLE IF NOT EXISTS skills (
            steamid TEXT,
            hero_clsid TEXT,
            clsid TEXT,
            level INTEGER,
            PRIMARY KEY (steamid, hero_clsid, clsid)
        )''')

    def close(self, commit=True):
        """Close the database connection."""
        if commit is True:
            self.connection.commit()
        self.connection.close()
        self.connection = None

    def save_player(self, player):
        """Save player's data into the database."""
        if player.steamid == 'BOT':
            steamid = 'BOT_' + player.name
        else:
            steamid = player.steamid
        self.connection.execute(
            'INSERT OR REPLACE INTO players VALUES (?, ?, ?)',
            (steamid, player.gold, player.hero.clsid))
        self.save_hero(steamid, player.hero)

    def save_hero(self, steamid, hero):
        """Save hero's data into the database."""
        self.connection.execute(
            'INSERT OR REPLACE INTO heroes VALUES (?, ?, ?, ?)',
            (steamid, hero.clsid, hero.level, hero.xp))
        for skill in hero.skills:
            self.connection.execute(
                'INSERT OR REPLACE INTO skills VALUES (?, ?, ?, ?)',
                (steamid, hero.clsid, skill.clsid, skill.level))
        self.connection.commit()

    def load_player(self, player):
        """Load player's data from the database."""
        hero_classes = wcgo.entities.Hero.get_classes()
        if player.steamid == 'BOT':
            steamid = 'BOT_' + player.name
        else:
            steamid = player.steamid
        player.gold, active_hero_clsid = self._get_player_data(steamid)
        for clsid, level, xp in self._get_heroes_data(steamid):
            if clsid not in hero_classes:
                continue
            hero = hero_classes[clsid](player, level, xp)
            self._load_skills(steamid, hero)
            player.heroes[clsid] = hero
            if clsid == active_hero_clsid:
                player.hero = hero

    def _load_skills(self, steamid, hero):
        """Load hero's data from the database."""
        cursor = self.connection.cursor()
        for skill in hero.skills:
            cursor.execute(
                'SELECT level FROM skills WHERE steamid=? AND hero_clsid=? AND clsid=?',
                (steamid, hero.clsid, skill.clsid))
            data = cursor.fetchone()
            if data:
                skill.level = data[0]

    def _get_player_data(self, steamid):
        """Get player's data from the database."""
        cursor = self.connection.execute(
            'SELECT gold, hero_clsid FROM players WHERE steamid=?', (steamid,))
        data = cursor.fetchone()
        if data is None:
            return (0, None)
        return data

    def _get_heroes_data(self, steamid):
        """Get a list of heroes' data for a given steamid."""
        return self.connection.execute(
            "SELECT clsid, level, xp FROM heroes WHERE steamid=?", (steamid,))
