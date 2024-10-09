# File format:
#
# [score_type lowscore|highscore|winnertakesall]
# [game_name <name>]
#
# game <time>
# <player> <score>
# <player> <score>
# <empty line>
#
# <etc>
# Hash comments are OK
#
# Example:
#
# game 2010-08-02 20:12
# Peter      100
# Jonatan    210
# Axel       134
#
#
# After parsing we have a list of matches with a scores dict for each match.
# The scores dict is a mapping between player names and their scores
# in that game.

import re

class UnexpectedStatementError(Exception): pass

class Game(object):
    def __init__(self, time_string, type):
        self.time_string = time_string
        self.scores = {}
        self.type = type

    def add_score(self, name, score):
        self.scores[name] = score

    @property
    def winners(self):
    # Find winner, taking score type into account
        winners = []
        winner_score = None

        winner_score = None
        for name, score in self.scores.items():
            if self.type == 'lowscore':
                if winner_score is None or score < winner_score:
                    winner_score = score
                    winners = [name]
                elif score == winner_score:
                    winners.append(name)
            else:
                if winner_score is None or score > winner_score:
                    winner_score = score
                    winners = [name]
                elif score == winner_score:
                    winners.append(name)
        return winners

    def set_score_type(self, type):
        self.type = type


class GamesParser(object):
    def __init__(self, file_obj, name=None):
        self.file = file_obj
        self.score_type = 'highscore'
        self.game_name = name
        self.errors = []

    def parse_type(self, line):
        type_exp = '^score_type\s+(lowscore|highscore|winnertakesall)$'
        m = re.match(type_exp, line)
        if m is not None:
            self.score_type = m.group(1)
            return True
        else:
            return False

    def parse_game_name(self, line):
        name_exp = '^game_name\s+(.+)$'
        m = re.match(name_exp, line)
        if (m is not None):
            self.game_name = m.group(1)
            return True
        else:
            return False

    def parse_game(self, line):
        game_exp = '^game\s+([0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}[:.][0-9]{2})\s*$'
        m = re.match(game_exp, line)
        if m is not None:
            time_string = m.group(1)
            return Game(time_string, self.score_type)
        else:
            return None

    def parse_score(self, line, current_game):
        score_exp = '^([\w+-]+)\s+(-?[0-9]+)\s*$'
        m = re.match(score_exp, line)
        if m is not None:
            if current_game is None:
                raise UnexpectedStatementError('Spurious score (no current game) on line %i' % self.line_no)
            else:
                # Add score to current game
                name = m.group(1)
                score = int(m.group(2))
                current_game.add_score(name, score)
                return True
        else:
            return False

    def parse_comment(self, line):
        return re.match('^#.*$', line) is not None

    def parse_empty_line(self, line):
        return re.match('^\s*$', line) is not None

    def parse_file(self):
        self.games = []
        current_game = None
        self.line_no = 0

        # For each line in the file, try to parse it as a comment, empty line,
        # type, game name, score or game.
        # If the line marks the beginning of a new game, add the current game
        # to the list of games and start a new game.
        for line in self.file:
            self.line_no += 1
            try:
                if self.parse_comment(line) or self.parse_empty_line(line):
                    continue

                if self.parse_type(line):
                    continue

                if self.parse_game_name(line):
                    continue

                if self.parse_score(line, current_game):
                    continue

                new_game = self.parse_game(line)
                if new_game:
                    if current_game is not None:
                        self.games.append(current_game)
                    current_game = new_game
                    continue

                raise UnexpectedStatementError('Syntax error on line %i: %s' % (self.line_no, line))
            except UnexpectedStatementError as e:
                self.errors.append(e.args[0])

        # Add the last game
        if current_game is not None:
            self.games.append(current_game)

        return self.games
