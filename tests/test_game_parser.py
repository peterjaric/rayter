from io import StringIO
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
        self.assertEqual(parser.games[0].scores["Molgan"], -666)
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
        self.assertEqual("Syntax error on line 4: game 2012-01+19 15:12\n", parser.errors[0])

    def test_parse_comments(self):
        data = \
"""
#
#
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual(len(parser.errors), 0)

    def test_hiscore_winner(self):
        data = \
"""
game_name Cool game

game 2012-01-19 15:12
Jonatan    1337
Molgan     666
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual("Jonatan", parser.games[0].winners[0])
        self.assertEqual(len(parser.errors), 0)

    def test_lowscore_winner(self):
        data = \
"""
game_name Cool game
score_type lowscore
game 2012-01-19 15:12
Jonatan    1337
Molgan     666
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual("Molgan", parser.games[0].winners[0])
        self.assertEqual(len(parser.errors), 0)

    def test_multiple_winners(self):
        data = \
"""
game_name Cool game

game 2012-01-19 15:12
Jonatan    1337
Peter      1337
Molgan     666
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual(2, len(parser.games[0].winners))
        self.assertTrue("Jonatan" in parser.games[0].winners)
        self.assertTrue("Peter" in parser.games[0].winners)
        self.assertEqual(len(parser.errors), 0)

    def test_parse_international_names(self):
        data = \
"""
game_name Name game

game 2012-01-19 15:12
Álvaro      1
Zoë         2
Søren       3
Łukasz      4
Çağla       5
Björn       6
François    7
Dvořák      8
Saša        9
İpek        10
Márta       11
Máximo      12
Jürgen      13
Faïza       14
Renée       15
Ngô         16
Hàníf       17
Sáng-hōng   18
Māori       19
Chidiébére  20
Dhanésh     21
C++         22
"""
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        self.assertEqual(0, len(parser.errors))

