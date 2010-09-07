#!/usr/bin/python

import sys
from parser import GamesParser
from rater import Rater           

def random_color():
    pass

if (len(sys.argv) == 1):
    print "Usage:", sys.argv[0], "<filename>"
    exit(1)

try:
    filename = sys.argv[1]
    parser = GamesParser(filename)
    games = parser.parse_file()
    rater = Rater(games)
    ratings = rater.rate_games(parser.score_type)

    if (len(sys.argv) > 2):
        if sys.argv[2] == "gnuplot":
            commands = 'set key left\n'
            plot_command = 'plot "%s" with lines lw 2 title "%s"\n'

            for name in rater.players:
                player = rater.players[name]
                if player.get_game_count() > 0:
                    player_file_name = "plot_rating_%s.data" % player.name
                    commands += plot_command % (player_file_name, player.name)
                    if plot_command.startswith('plot'):
                        plot_command = 're' + plot_command
                    player_file = open(player_file_name, "w")  
                    for game_num in range(player.get_first_game() - 1, len(games) + 1):
                        rating = player.get_rating(game_num)
                        print >> player_file, "%d %d" % (game_num, rating)

            commands += 'pause mouse\n'
            command_file_name = "plot_commands.gnuplot"
            command_file = open(command_file_name, "w")
            print >> command_file, commands
            print "Run 'gnuplot %s' to plot all ratings." % command_file_name 
        elif sys.argv[2] == "html":
            categories = ''
            game_nums = range(0, len(games) + 1)
            for game_num in game_nums:
                categories += "<category name='%d'/>\n" % game_num

            datasets = ''

            for name in rater.players:
                player = rater.players[name]
                if player.get_game_count() > 0:
                    dataset = "<dataset seriesName='%s'>\n" % name
                    for game_num in game_nums:
                        if player.has_played(game_num):
                            rating = player.get_rating(game_num)
                            dataset += "<set value='%d'/>\n" % rating
                        else:
                            dataset += "<set/>\n"
                    dataset += "</dataset>\n"
                    datasets += dataset
                
            template_file = open('ratingGraph.template')
            xml = template_file.read()
            xml = xml.replace('$GAMENAME$', parser.game_name)
            xml = xml.replace('$CATEGORIES$', categories)
            xml = xml.replace('$DATASETS$', datasets)
            graph_file = open('html/graph_%s.xml' % parser.game_name, "w")
            print >> graph_file, xml
        else:
            name = sys.argv[2]
            player = rater.players[name]
            if player:
                for game_num in sorted(player.rating_history.keys()):
                    rating = player.rating_history[game_num]
                    print "%d %d" % (game_num, rating)
    else:
        print "Spel: %s" % parser.game_name
        print "Totalt antal matcher: %s" % len(games)
        hformat = "%-15s%-10s%-10s%-10s"
        rformat = "%-15s%7d%9d%9d"
        print hformat % ("Namn", "Matcher", "Rating", "Delta")
        for rating in ratings:
            print rformat % rating
        
except IOError:
    print "File", filename, "not found."
