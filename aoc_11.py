#!/usr/bin/env python3

import numpy as np

sample_input = [
"Monkey 0:\n",
"  Starting items: 79, 98\n",
"  Operation: new = old * 19\n",
"  Test: divisible by 23\n",
"    If true: throw to monkey 2\n",
"    If false: throw to monkey 3\n",
"\n",
"Monkey 1:\n",
"  Starting items: 54, 65, 75, 74\n",
"  Operation: new = old + 6\n",
"  Test: divisible by 19\n",
"    If true: throw to monkey 2\n",
"    If false: throw to monkey 0\n",
"\n",
"Monkey 2:\n",
"  Starting items: 79, 60, 97\n",
"  Operation: new = old * old\n",
"  Test: divisible by 13\n",
"    If true: throw to monkey 1\n",
"    If false: throw to monkey 3\n",
"\n",
"Monkey 3:\n",
"  Starting items: 74\n",
"  Operation: new = old + 3\n",
"  Test: divisible by 17\n",
"    If true: throw to monkey 0\n",
"    If false: throw to monkey 1\n"
]

######################################################
all_params = {
   # N_rounds: Part 1: 20, Part 2: 10000
   'Part1': {'N_rounds': 20},
   'Part2': {'N_rounds': 10000}
}
##########################################
# set `whichPart` to 'Part1' or 'Part2' !!
whichPart = 'Part1'
##########################################
params = all_params[whichPart]
######################################################

def adapt_worry_level(old_val,operator,operand):
   #print(f"eval string: |{old_val + operator + operand}|")
   new_wl = eval(old_val + operator + operand)
   #print(f"old_wl,new_wl:  {old_val,new_wl}")
   if whichPart == 'Part1': new_wl = str(int(new_wl/3)) #wl = int(wl/3) -- Part 1
   if whichPart == 'Part2': new_wl = str(new_wl) # –– Part 2
   #print(f"updated new_wl: {new_wl}\n")
   return new_wl

class Monkey:
   def __init__(self):
      self.id = -1
      self.wl = []
      self.if_false = str()
      self.if_true  = str()
      self.operator = str()
      self.operand = str()
      self.test = str()
      self.n_items_inspected = 0
   def calc_new_wl(self):
      if self.operand=="old": func_change_wl = lambda x: adapt_worry_level(x,self.operator,x)
      else:                   func_change_wl = lambda x: adapt_worry_level(x,self.operator,self.operand)
      return np.array(list(map(func_change_wl,self.wl)))
   def calc_test_is_divisible(self,new_wl):
      func_test = lambda x: int(x)%int(self.test)==0
      return np.array(list(map(func_test,new_wl)))
   def __str__(self):
      return \
         f"id: {self.id}\n" +\
         f"  worry levels:      {self.wl}\n" +\
         f"  operator:          {self.operator}\n" +\
         f"  operand:           {self.operand}\n" +\
         f"  test:              {self.test}\n" +\
         f"  if_true:           {self.if_true}\n" +\
         f"  if_false:          {self.if_false}\n" +\
         f"  n_items_inspected: {self.n_items_inspected}\n"
   def act(self,monkeys,common_divisor=1):
      # 1) calc new worry level
      new_wl = self.calc_new_wl()
      self.n_items_inspected += len(new_wl)
      
      # 2) test on new worry level
      test_is_divisible = self.calc_test_is_divisible(new_wl)
      passed_wl = new_wl[test_is_divisible==True]
      failed_wl = new_wl[test_is_divisible==False]
      for e in passed_wl: assert str(int(e)%int(self.test))=="0"
      
      #print()
      #print(f"passed test: {passed_wl}")
      #print(f"failed test: {failed_wl}")
      
      # 3) throw all worry levels that failed test to monkey with id if_false, all that passed to if_true
      #print(f"sending failed to {self.if_false} and passed to {self.if_true}")
      
      #–– Part 1
      if whichPart == 'Part1':
         monkeys[self.if_false].wl.extend(failed_wl) #[monkeys[self.if_false].wl.append(e) for e in failed_wl]
         monkeys[self.if_true ].wl.extend(passed_wl) #[monkeys[self.if_true ].wl.append(e) for e in passed_wl]
      
      #–– Part 2 (take rem of mod by test-val of target => test result will still be same, but smaller nums)
      #print([e for e in failed_wl])
      #print([e for e in passed_wl])
      # ————————————— why is this working for round 20, but not for 1000 ?!?
      """f = lambda e,test: str(int(e)%int(test))
      g = lambda e,test,o: str((int(e)%int(o))%int(test))
      if len(passed_wl)>0:
         if monkeys[self.if_true].operator == '*':# and monkeys[self.if_true].operand == "old":
            [monkeys[self.if_true].wl.append( f(e,monkeys[self.if_true].test) ) for e in passed_wl]
         ### if next cmd will be 'old*old', don't send 'old' but 'old % target_monkey_test'
         ##if monkeys[self.if_true].operator == '*' and monkeys[self.if_true].operand == "old":
         ##   [monkeys[self.if_true].wl.append( f(e,monkeys[self.if_true].test) ) for e in passed_wl]
         else:
            monkeys[self.if_true].wl.extend(passed_wl)
      if len(failed_wl)>0:
         monkeys[self.if_false].wl.extend(failed_wl)
      """
      #–– Part 2
      if whichPart == 'Part2':
         f = lambda e,d: str(int(e)%d)
         [monkeys[self.if_false].wl.append( f(e,common_divisor) ) for e in failed_wl]
         [monkeys[self.if_true ].wl.append( f(e,common_divisor) ) for e in passed_wl]


      #print(f"{self.id} throwing these to {self.if_false}: {failed_wl}")
      #print(f"{self.id} throwing these to {self.if_true}:  {passed_wl}\n")
      
      #print(f"old wl: {self.wl}")
      #print(f"new wl: {new_wl}")
      #print(f"test:   {test_is_divisible}")

      # 4) empty current monkey's list after it has thrown all worry levels
      self.wl.clear()

def print_heading_str(h):
   n = 50
   print('~'*n + f"\n––– {h} –––\n" + '~'*n)

def solve(data):
   data = ''.join(data).split("\n\n")
   print(f"data: {data}")
   print(f"N monkeys: {len(data)}")

   print_heading_str("parse monkeys from file")
   monkeys = {} # {str(i):Monkey() for i in range(len(data))}
   for turn in data:
      #print(turn)
      lines = turn.split("\n")
      #print(lines)
      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      # parse from file
      monkey_id          = lines[0].split()[1].split(":")[0]
      worry_level        = [e.strip() for e in lines[1].split(":")[1].split(",")]
      _,operator,operand = lines[2].split("=")[1].split()
      test               = lines[3].split("by")[1].strip()
      if_true            = lines[4].split(":")[1][-1]
      if_false           = lines[5].split(":")[1][-1]
      print(f"monkey_id:        |{monkey_id}|")
      print(f"worry_level:      |{worry_level}|")
      print(f"operator,operand: |{operator},{operand}|")
      print(f"test              |{test}|")
      print(f"if_true           |{if_true}|")
      print(f"if_false          |{if_false}|")
      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      # build up monkeys
      monkeys[monkey_id]          = Monkey()
      monkeys[monkey_id].id       = monkey_id
      monkeys[monkey_id].wl       = worry_level
      monkeys[monkey_id].operator = operator
      monkeys[monkey_id].operand  = operand
      monkeys[monkey_id].test     = test
      monkeys[monkey_id].if_false = if_false
      monkeys[monkey_id].if_true  = if_true
      #print(f"monkey: {monkeys[monkey_id]}")
      print()
      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   # with help of https://www.reddit.com/r/adventofcode/comments/zifqmh/2022_day_11_solutions/ => Chinese Theorem
   print_heading_str("monkeys common denominator for Part 2")
   common_divisor = np.prod([int(m.test) for m in monkeys.values()])
   print(f"common_divisor: {common_divisor}\n")

   print_heading_str("monkeys initially")
   [print(f"{k} –> {m}") for k,m in monkeys.items()]
   #print(monkeys['0'].calc_new_wl())
   #exit()
   print_heading_str("rounds start here")
   N_rounds = params['N_rounds'] # Part 1: 20, Part 2: 10000
   # go for `N_rounds` rounds, each round all monkeys take turns
   inspected_items = []
   for i in range(N_rounds):
      #print(f"round {i+1}")
      #if i == 1: break
      #for monkey in monkeys.values(): monkey.act(monkeys) # Part 1
      for monkey in monkeys.values(): monkey.act(monkeys,common_divisor) # Part 2
      if (i+1)%100==0: print(f"after round {i+1}:")
      ####[print(f"{m}") for k,m in monkeys.items()]
      ###[print(f"{m.id}: {m.n_items_inspected},{m.wl}") for k,m in monkeys.items()]
      inspected_items.append([m.n_items_inspected for m in monkeys.values()])
   
   #print(inspected_items)
   #for i in range(len(monkeys)):
   #   print(f"monkey {i}: {np.diff([e[i] for e in inspected_items])}")

   #print(list(zip(inspected_items))[1])
   #exit()

   print()
   print_heading_str(f"2 most active monkeys after {N_rounds} rounds")
   #print(f"n_inspected: {[monkey.n_items_inspected for monkey in monkeys.values()]}")
   n_inspected = sorted([monkey.n_items_inspected for monkey in monkeys.values()])
   print(f"n_inspected: {n_inspected}")
   top2 = n_inspected[-2:]
   print(f">> SOLUTION Part 1/2: level of monkey business = {np.prod(top2)}\n")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)
   exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_11.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
