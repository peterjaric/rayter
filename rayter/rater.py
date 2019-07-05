import math
import time

from player import Player

#def to_lowscore(score, scores):
#    max_score_in_game = max(scores)
#    return max_score_in_game - score

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
        
        old_rating = self.players[player].get_rating()

        # Normalize scores if there are negative scores
        raw_scores = game['scores'].values()
        score = to_normalized_score(game['scores'][player], raw_scores)    
        scores = [to_normalized_score(s, raw_scores) for s in raw_scores]

        # Switch to lowe scores if score_type is lowscore
        if score_type == 'lowscore':
            score = to_lowscore(score, scores)
            scores = [to_lowscore(s, scores) for s in scores]

        # Calculate sums
        scores_sum = math.fsum(max(s, 0) for s in scores)
        old_ratings_sum = math.fsum(self.players[p].get_rating() for p in game['scores'].keys())
            
        # Choose how big part of their rating each player puts in
        if score_type == 'winnertakesall':
            K = 0.02
        else:
            K = 0.05

        # Calculate new rating
        rating_in = K * old_rating
        rating_out = (score / scores_sum) * K * old_ratings_sum
        change = rating_out - rating_in
        new_rating = old_rating + change

        return new_rating


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
