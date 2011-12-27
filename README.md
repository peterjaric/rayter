# Rayter

Rayter is a program for generating player ratings from a number of games, 
with the results stored in a file. 

## Installing rayter

<pre>
pip install rayter
</pre>

or

<pre>
easy_install rayter
</pre>

## Running rayter

<pre>
rayter games_file.txt
</pre>


## Rayter file format

The rayter file format is designed to be easily created by hand using a text 
editor. Here is an example for a file containing two games of Hearts:

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

**score_type lowscore** means that in this game the goal is to have as low 
score as possible. The options for **score_type** are **lowscore** and **highscore**, 
and the latter is the default (if score_typ isn't specified).

Number of whitespace characters doesn't matter.

## Rayter algorithm

Every player starts with 1000 in rating. The sum of all ratings will always be 1000 * the 
number of players in the league. So if one player gets +60 rating in a game, and all other 
players looses rating, the sum of their rating change will be -60. 

If a player with 1200 rating is playing against an opponent with 1000 rating. The first 
player is expected to get 20% more points than the second one. Therefore, if the first 
player gets 240 points, and the second player gets 200, both will get 0 rating change.

For more details see **rater.py**.
