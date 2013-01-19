START_RATING = 1000

class Player(object):
    def __init__(self, name):
        self.rating_history = {}
#        self.set_rating(START_RATING, 0)
        self.name = name

    def get_rating_change(self, game):
        if self.get_game_count() > 0 and game in self.rating_history:
            return self.get_rating(game) - self.get_rating(game - 1)
        else:
            return 0

    def has_played(self, game):
        return game in self.rating_history

    def get_rating(self, game = None):
        if self.get_game_count() is 0:
            game = 0
        elif game is None:
            game = self.last_game
        elif game < 0:
            game = 0

        if not self.has_played(game):
            if game is not 0:
                return self.get_rating(game - 1)
            else:
                return START_RATING
        else:
            return self.rating_history[game]
    
    def set_rating(self, rating, game_num):
        self.rating_history[game_num] = rating
        self.last_game = game_num

    def get_game_count(self):
        return len(self.rating_history)

    def get_first_game(self):
        if self.get_game_count() > 0:
            return sorted(self.rating_history.keys())[0]
        else:
            return None
