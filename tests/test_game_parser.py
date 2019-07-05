from StringIO import StringIO
from unittest import TestCase

from rayter.game_parser import GamesParser


class GamesParserTest(TestCase):
    def test_parse_name(self):
        data = \
"""
game_name Settlers of Catan

"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual("Settlers of Catan", parser.game_name)
        self.assertEqual(len(parser.errors), 0)

    def test_parse_score_type(self):
        data = \
"""
game_name Settlers of Catan
score_type lowscore

"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual("lowscore", parser.score_type)
        self.assertEqual(len(parser.errors), 0)
        data = \
"""
game_name Settlers of Catan
score_type winnertakesall

"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual("winnertakesall", parser.score_type)
        self.assertEqual(len(parser.errors), 0)

    def test_parse_games(self):
        data = \
"""
game_name Cool game

game 2012-01-19 15:12
Jonatan    1337
Molgan     666

game 2012-01-19 15:12
Jonatan    123
Molgan     231
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual(2, len(parser.games))
        self.assertEqual(len(parser.errors), 0)

    def test_parse_minus(self):
        data = \
"""
game_name Cool game

game 2012-01-19 15:12
Jonatan    1337
Molgan     -666
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual(parser.games[0]["scores"]["Molgan"], -666)
        self.assertEqual(len(parser.errors), 0)

    def test_parse_errors(self):
        data = \
"""
game_name Invalid date - one syntax error, two spurious scores 

game 2012-01+19 15:12
Jonatan    1337
Molgan     -666
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual(len(parser.errors), 3)

    def test_parse_comments(self):
        data = \
"""
#
# 
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual(len(parser.errors), 0)
