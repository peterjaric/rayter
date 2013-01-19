# File format:
# 
# [score_type lowscore|highscore]
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
#from time import strptime

class GamesParser(object):
    def __init__(self, file_obj, name):
        self.file = file_obj
        self.score_type = 'highscore'
        self.game_name = name

    def parse_type(self, line):
        type_exp = '^score_type\s+(lowscore|highscore)$'
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
        game_exp = '^game\s+([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})'
        m = re.match(game_exp, line)
        if m is not None:
            time_string = m.group(1)
#            time_format = "%Y-%m-%d %H:%M"
#            time = strptime(time_string, time_format)
            return { 
#                'time': time,
                'time': time_string,
                'scores': {}
                }
        else:
            return None

    def parse_score(self, line, game_dict):
        score_exp = '^([a-zA-Z\+]+)\s+([0-9]+)'
        m = re.match(score_exp, line)
        if m is not None:
            if game_dict is None:
                print 'Spurious score on line', self.line_no
            else:
                name = m.group(1)
                score = int(m.group(2))
                game_dict['scores'][name] = score
                return True
        else:
            return False

    def parse_file(self):
        self.games = []
        current_game = None
        self.line_no = 0

        for line in self.file:
            self.line_no += 1
 
            # Comments (TODO: refactor into method to match rest of method)
            if re.match('^\s*(#.*)?$', line) is not None:
                continue
            
            if self.parse_type(line):
                continue

            if self.parse_game_name(line):
                continue

            result = self.parse_game(line)
            if result:
                if current_game is not None:
                    self.games.append(current_game)
                current_game = result
                continue

            result = self.parse_score(line, current_game)
            if result:
                continue

            print 'Unknown format on line', self.line_no
        
        if current_game is not None:
            self.games.append(current_game)

        return self.games
