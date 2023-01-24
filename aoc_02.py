#!/usr/bin/env python3

"""
A  rock
B  paper
C  scissors

A vs. C -> A wins
B vs. C -> C wins
A vs. B -> B wins
x vs. x -> draw

input: strategy guide
   (c1,c2)
   1st col: opponent's pick
   2nd col: response to play (strategy guide)
      X  rock
      Y  paper
      Z  scissors

total score = sum(single_round_scores)
single_round_score =
   (score for selected shape) + (score of outcome of round)
   –––––––––––––––––––––––––––+––––––––––––––––––––––––––––
                    X -> 1    |    loss -> 0
                    Y -> 2    |    draw -> 3
                    Z -> 3    |    win  -> 6

Part 2: 2nd column means
X  need to lose
Y  need round to end in draw
Z  need to win

"""
sample_input = [
"A Y\n",
"B X\n",
"C Z\n",
]

shape_score   = {'X': 1, 'Y': 2, 'Z': 3}
shape2XYZ     = {'A': 'X', 'B': 'Y', 'C': 'Z'}
losing_shape  = {'A': 'C', 'B': 'A', 'C': 'B'}  # 'A': 'C' –> C loses against A
winning_shape = {'A': 'B', 'B': 'C', 'C': 'A'}  # 'A': 'B' –> B wins against A

def calc_score(p):
   """ p: pair of selected shaped, e.g.: ('A','Y') """

   """ short version:
   if   p[1] == shape2XYZ[p[0]]: return 3
   elif p[1] == shape2XYZ[winning_shape[p[0]]]: return 6
   elif p[1] == shape2XYZ[losing_shape[p[0]]]: return 0
   """
   if p[0] == 'A':
      if   p[1] == 'X': return 3
      elif p[1] == 'Y': return 6
      elif p[1] == 'Z': return 0
   elif p[0] == 'B':
      if   p[1] == 'Y': return 3
      elif p[1] == 'X': return 0
      elif p[1] == 'Z': return 6
   elif p[0] == 'C':
      if   p[1] == 'Z': return 3
      elif p[1] == 'X': return 6
      elif p[1] == 'Y': return 0
   else:
      print("invalid input!")
      exit(-1)

def get_shape(p):
   if   p[1] == 'X': return losing_shape[p[0]]
   elif p[1] == 'Y': return p[0]
   elif p[1] == 'Z': return winning_shape[p[0]]
   
def solve(data):
   pairs = [l.strip().split() for l in data]
   #print(pairs)
   scores_per_round = [shape_score[p[1]] + calc_score(p) for p in pairs]
   total_score = sum(scores_per_round)
   print(f">> SOLUTION Part 1: {total_score}")
   #––– Part 2
   scores_per_round = [shape_score[shape2XYZ[get_shape(p)]] + calc_score((p[0],shape2XYZ[get_shape(p)])) for p in pairs]
   print(f">> SOLUTION Part 2: {sum(scores_per_round)}\n")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_02.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
