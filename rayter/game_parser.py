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
# After parsing we have a list of dicts that look like this:
# { 'time': String, 'scores': dict }
# The scores dict is a mapping between player names and their scores
# in that game.

import re
import sys
import math


class UnexpectedStatementError(Exception): pass


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
            return { 
                'time': time_string,
                'scores': {}
                }
        else:
            return None

    def parse_score(self, line, game_dict):
        score_exp = '^([a-zA-Z\+]+)\s+(-?[0-9]+)\s*$'
        m = re.match(score_exp, line)
        if m is not None:
            if game_dict is None:
                raise UnexpectedStatementError('Spurious score (no current game) on line %i' % self.line_no)
            else:
                name = m.group(1)
                score = int(m.group(2))
                game_dict['scores'][name] = score
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
                self.errors.append(e.message)
        
        if current_game is not None:
            self.games.append(current_game)

        return self.games
