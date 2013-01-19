from StringIO import StringIO
from unittest import TestCase

from rayter.game_parser import GamesParser

class GamesParserTest(TestCase):
    def test_parse_name(self):
        data = \
"""
game_name Settlers of Catan

"""
        parser = GamesParser(StringIO(data))
        parser.parse_file()
        self.assertEqual("Settlers of Catan", parser.game_name)
    
    def test_parse_score_type(self):
        data = \
"""
game_name Settlers of Catan
score_type lowscore

"""
        parser = GamesParser(StringIO(data))
        parser.parse_file()
        self.assertEqual("lowscore", parser.score_type)
    
    def test_parse_games(self):
        data = \
"""
game_name Cool game

game 2012-01-19 15:12:00
Jonatan    1337
Molgan     666

game 2012-01-19 15:12:20
Jonatan    123
Molgan     231
"""
        parser = GamesParser(StringIO(data))
        parser.parse_file()
        self.assertEqual(2, len(parser.games))
    
