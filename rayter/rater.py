import math
import time

from player import Player

SCORE_TYPE_HIGH_SCORE = 'highscore'
SCORE_TYPE_LOW_SCORE = 'lowscore'
SCORE_TYPE_WINNER_TAKES_ALL = 'winnertakesall'


def to_lowscore(score, scores):
    max_score_in_game = max(scores)
    min_score_in_game = min(scores)
    return max_score_in_game - score + min_score_in_game

def to_normalized_score(score, scores):
    """
    Increases score with the absolute value of the lowest score in the game if it is negative.
    """
    min_score_in_game = min(scores)
    if min_score_in_game < 0:
        return score - min_score_in_game
    else:
        return score


def rate_single_game(scores, ratings, score_type=SCORE_TYPE_HIGH_SCORE, K=None):
    """
    Calculate the rating changes for a single game

    :param scores: List with the score for each player
    :param ratings: List of the ratings for each player
    :param score_type: Game type constant that can be one of the following constants 
                       (available under the rayter.rater python module):
                       SCORE_TYPE_HIGH_SCORE: Goal of game is to get as high score as possible
                       SCORE_TYPE_LOW_SCORE:  Goal iof game is to get as low score as possible
                       SCORE_TYPE_WINNER_TAKES_ALL: Game with a binary result (e.g. Chess). Using
                                                    this score type is effectively the same as using
                                                    SCORE_TYPE_HIGH_SCORE and seting the K parameter to 0.02.
    :param K: Override how large fraction of each players rating that is "up for grabs" in the game. 
              If not specified or set to None, K will be set automatically based on the score_type param.
    :return: List of rating change for each player
    """
    # Normalize scores if there are negative scores   
    normalized_scores = [to_normalized_score(s, scores) for s in scores]

    # Switch to lowerscore if score_type is lowscore
    if score_type == SCORE_TYPE_LOW_SCORE:
        normalized_scores = [to_lowscore(s, normalized_scores) for s in normalized_scores]

    # Calculate sums
    scores_sum = math.fsum(normalized_scores)
    ratings_sum = math.fsum(ratings)
        
    # Choose how big part of their rating each player puts in
    if K is None:
        if score_type == SCORE_TYPE_WINNER_TAKES_ALL:
            K = 0.02
        else:
            K = 0.05

    # If scores_sum is 0, it means that all scores are 0, since we've normalized 
    # scores to not contain any negative values
    if scores_sum == 0:
        scores_sum = 100.0 * len(scores)
        normalized_scores = [100.0 for s in range(len(scores))]

    rating_changes = []
    for score, old_rating in zip(normalized_scores, ratings):
        # Calculate new rating
        rating_in = K * old_rating
        rating_out = (score / scores_sum) * K * ratings_sum
        change = rating_out - rating_in
        rating_changes.append(change)

    return rating_changes



class Rater(object):
    def __init__(self, games):
        self.games = games
        self.players = {}

    def calculate_new_rating(self, score_type, player, game):
        return self.calculate_new_rating_keep_average(score_type, player, game)


    def calculate_new_rating_keep_average(self, score_type, player, game):
        """
        Calculates new rating for a player based on old rating and result in the 
        given game. The average rating will be the same before and after this 
        calculation has been called for all players.
        """
        scores = []
        ratings = []
        player_idx = None
        for i, (player_name, score) in enumerate(game['scores'].items()):
            scores.append(score)
            ratings.append(self.players[player_name].get_rating())
            if player_name == player:
                player_idx = i

        rating_changes = rate_single_game(scores, ratings, score_type=score_type)
        return ratings[player_idx] + rating_changes[player_idx]


    def cmp_rating(self, p1, p2):
        if self.players[p1].get_rating() < self.players[p2].get_rating():
            return -1
        elif self.players[p1].get_rating() > self.players[p2].get_rating():
            return 1
        else:
            return 0
        
    def rate_games(self, score_type):
        game_num = 0
        for game in self.games:
            game_num += 1
            # Add any new players to the players dict
            for player in game['scores']:
                if player not in self.players:
                    self.players[player] = Player(player)
                   
            # Calculate ratings
            new_ratings = {}
            for player in game['scores']:
                new_ratings[player] = self.calculate_new_rating(score_type, player, game)
            
           
            # Update ratings
            for player in new_ratings:
                self.players[player].set_rating(new_ratings[player], game_num)

            #rats = [self.players[p].get_rating() for p in self.players]
            #print math.fsum(rats) / len(rats)


        sorted_players = self.players.keys()
        sorted_players.sort(self.cmp_rating, reverse=True) 

        ratings = []
        for player in sorted_players:
            ratings.append((player, 
                            self.players[player].get_game_count(), 
                            round(self.players[player].get_rating()),
                            round(self.players[player].get_rating_change(game_num))))
            
        return ratings
