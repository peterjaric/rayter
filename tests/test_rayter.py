from io import StringIO
from datetime import datetime
from unittest import TestCase
from pprint import pprint
from textwrap import dedent

from rayter.rater import Rater, rate_single_game, SCORE_TYPE_HIGH_SCORE
from rayter.player import Player
from rayter.game_parser import GamesParser

class RaterTest(TestCase):
    def test_rate_game_with_negative_score(self):
        data = dedent("""
            game_name Negative score 

            game 2012-01-19 15:12
            Jonatan    1337
            Hugo 0
            Molgan     -666
        """)
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        rater = Rater(parser.games)
        rater.rate_games(parser.score_type)
        self.assertNotEqual(
            rater.players['Hugo'].get_rating(),
            rater.players['Molgan'].get_rating(),
        )
    
    def test_rate_game_with_all_negative_scores(self):
        data = dedent("""
            game_name Negative score 

            game 2012-01-19 15:12
            Hugo -100
            Molgan     -120
        """)
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        rater = Rater(parser.games)
        rater.rate_games(parser.score_type)
        self.assertGreater(
            rater.players['Hugo'].get_rating(),
            rater.players['Molgan'].get_rating(),
        )

    def test_rate_game_with_all_same_negative_scores(self):
        data = dedent("""
            game_name Negative score 

            game 2012-01-19 15:12
            Hugo -666
            Molgan     -666
        """)
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        rater = Rater(parser.games)
        rater.rate_games(parser.score_type)
        self.assertEqual(1000, rater.players['Hugo'].get_rating())
        self.assertEqual(1000, rater.players['Molgan'].get_rating())
    
    def test_rate_game_with_all_zero_scores(self):
        data = dedent("""
            game_name Zero scores

            game 2012-01-19 15:12
            Hugo    0
            Molgan  0
        """)
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        rater = Rater(parser.games)
        rater.rate_games(parser.score_type)
        self.assertEqual(1000, rater.players['Hugo'].get_rating())
        self.assertEqual(1000, rater.players['Molgan'].get_rating())

    def test_rate_winnertakesall_game(self):
        data = dedent("""
            game_name Winner Takes All
            score_type winnertakesall

            game 2019-07-05 15:12
            Jonatan 0
            Hugo 0
            Molgan 1
        """)
        parser = GamesParser(StringIO(data), "test")
        parser.parse_file()
        rater = Rater(parser.games)
        rater.rate_games(parser.score_type)
        self.assertEqual(rater.players['Hugo'].get_rating(),
                         rater.players['Jonatan'].get_rating())
        self.assertGreater(rater.players['Molgan'].get_rating(),
                           rater.players['Hugo'].get_rating())
        self.assertNotEqual(
            rater.players['Molgan'].get_rating() -
            rater.players['Hugo'].get_rating(), 150)
    
    def test_rate_one_game(self):
        rating_changes = rate_single_game([100, 100], [1200, 1000], score_type=SCORE_TYPE_HIGH_SCORE)
        self.assertEqual([-5, 5], rating_changes)
    
    def test_rate_one_game_custom_K(self):
        rating_changes = rate_single_game([100, 100], [1200, 1000], score_type=SCORE_TYPE_HIGH_SCORE, K=0.1)
        self.assertEqual([-10, 10], rating_changes)
