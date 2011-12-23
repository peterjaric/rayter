
#!/usr/bin/python

import sys
import json
from game_parser import GamesParser
from rater import Rater
from optparse import OptionParser


opt_parser = OptionParser(usage = "usage: %prog [options] <game file>")
opt_parser.add_option("-m", "--mode", dest="mode", default="text",
                  help="output mode (text, html, gnuplot, json)")
opt_parser.add_option("-p", "--player", dest="player",
                  help="player name")

(options, args) = opt_parser.parse_args()

if len(args) < 1:
    print >> sys.stderr, "Error: No game file specified. Try", sys.argv[0], "-h."
    exit(1)


try:
    filename = args[0]
    parser = GamesParser(filename)
    games = parser.parse_file()
    rater = Rater(games)
    ratings = rater.rate_games(parser.score_type)

    if options.mode == "gnuplot":
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
    elif options.mode == "html":
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
    elif options.mode == "json":
        rating_dict = {}
        for rating in ratings:
            r = {"name":rating[0], "matches":rating[1], "rating":rating[2], "delta":rating[3]}
            rating_dict[rating[0]] = r
        print simplejson.dumps(rating_dict)
    elif not options.player is None:
        name = options.player
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
        
except IOError as ioe:
    print ioe
