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
and the latter is the default (if not type is specified).

Number of whitespace characters doesn't matter.

## Rayter algorithm

The rating algorithm that is used is a variant of the algorithm used by Swedish 
Scrabble website Betapet (http://betapet.com). Here is a description, in Swedish,
of the algorithm: http://betapet.com/rating

TODO: Describe the rayter algorithm.
