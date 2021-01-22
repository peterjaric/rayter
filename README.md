# Rayter

![tests](https://github.com/peterjaric/rayter/workflows/.github/workflows/tests.yml/badge.svg)

Rayter is a program for generating player ratings from a number of games, 
with the results stored in a file. 

It can be used in the form as a command line program, or as a Python library.

## Installing Rayter

<pre>
pip install rayter
</pre>


## Running Rayter Command Line Tool

<pre>
rayter games_file.txt
</pre>


## Using Rayter as a library

Rayter can be used as a python library

```python
>>> from rayter.rater import rate_single_game, SCORE_TYPE_HIGH_SCORE
>>> scores = [100, 93, 74]
>>> ratings = [1889, 1400, 1662]
>>> rating_changes = rate_single_game(scores, ratings, score_type=SCORE_TYPE_HIGH_SCORE)
>>> rating_changes
[-1.7346441947565552, 16.22528089887642, -14.49063670411985]
```

## Rayter file format

The rayter file format expected by the Rayter Command Line Tool is designed 
to be easily created by hand using a text editor. Here is an example for a 
file containing two games of Hearts:

<pre>
score_type lowscore

game 2011-12-24 22:00
Jessica     95
Hugo        77
Jonatan     89
Jakob       103

game 2011-12-24 23:19
Hugo        107
Jonatan     96
Peter       65
Jakob       70
</pre>

**score_type lowscore** means that in this game the goal is to have as
low score as possible. The options for `score_type` are `lowscore`, 
`highscore` (the default, if score_type is not specified), and 
`winner_takes_all` (used for games with binary results, e.g. Chess).

Number of whitespace characters doesn't matter.

The format of the timestamp is year-month-day hour:minute, where hour
is from 0 to 23. The timestamp is currently not used more than as an
identifier of the game.

## Rayter Algorithm

Every player starts with a rating of 1000. The sum of all ratings will
always be 1000 * the number of players in the league. So if one player
gets +60 rating in a game, and all other players lose rating, the sum
of their rating change will be -60.

If a player with a rating of 1200 is playing against an opponent with
a rating of 1000, the first player is expected to get 20% more points
than the second one. That means that if the first player scores 240
points in the game, and the second player scores 200, the rating
change of both players will be 0, since 240 divided by 200 equals 1200
divided by 1000.

Example:

Here are some results in a made-up card game:

<pre>
game 2011-12-24 23:19
Dahlia        27
John          15
Ahmed         14
Lei           10

game 2011-12-25 21:12
John          23
Dahlia        10
Lei           4
Ahmed         4
</pre>

After the first game, the ratings will look like this:

<pre>
Name             Games   Rating    Delta
Dahlia               1     1032       32
John                 1      995       -5
Ahmed                1      992       -8
Lei                  1      980      -20
</pre>

When the second game was played, the ratings changed to this:

<pre>
Name             Games   Rating    Delta
John                 2     1058       62
Dahlia               2     1029       -3
Ahmed                2      962      -30
Lei                  2      951      -30
</pre>

For the full details see the `rate_single_game()` function in `rater.py`.
