#!/usr/bin/env python3

"""
- split string exactly in middle in 2 halves (is length always divisible by 2 without remainder ?!?)
- prios
   a-z –> 1-26    => lower case: char_val-'a'+1
   A-Z –> 27-52   => upper case: char_val-'A'+27
"""
sample_input = [
"vJrwpWtwJgWrhcsFMMfFFhFp\n",
"jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\n",
"PmmdzqPrVvPwwTWBwg\n",
"wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\n",
"ttgJtRGJQctTZtZT\n",
"CrZsJsPPZsGzwwsLwLmpwMDw\n"
]

#prios =      {chr(k):v for k,v in zip( range(ord('a'),ord('z')+1), range( 1,26+1) )}
#prios.update({chr(k):v for k,v in zip( range(ord('A'),ord('Z')+1), range(27,52+1) )})

prios =      {chr(i): i-ord('a')+ 1  for i in range(ord('a'),ord('z')+1)}
prios.update({chr(i): i-ord('A')+27  for i in range(ord('A'),ord('Z')+1)})

def solve(data):
   items = [l.strip() for l in data]
   for i in items:
      assert len(i)%2==0, "cannot divide in 2 halves of equal size!"
   print(items)
   compartments_content = [(i[:len(i)//2], i[len(i)//2:]) for i in items]
   print(compartments_content)
   d =      {chr(i):0 for i in range(ord('a'),ord('z')+1)}  # 'a':0,...,'z':0
   d.update({chr(i):0 for i in range(ord('A'),ord('Z')+1)}) # 'A':0,...,'Z':0
   #print(f"initial dict: {d}")
   d1 = d.copy()
   d2 = d.copy()
   shared_items = []
   for half1, half2 in compartments_content:
      #print(half1,"–",half2)
      for c in half1: d1[c] += 1 # dict of char-counts in string s:  d = {s[i]:s.count(s[i]) for i in range(len(s))}
      for c in half2: d2[c] += 1
      for k,v1,v2 in zip(d1.keys(),d1.values(),d2.values()):
         if v1>0 and v2>0:
            shared_items.append(k)
            break # break, as I know only 1 char will be shared per line
      # reset dicts' values
      d1 = {k:0 for k in d1.keys()}
      d2 = {k:0 for k in d2.keys()}
   all_prios = [prios[i] for i in shared_items]
   print(f"all shared items: {shared_items}")
   print(f"all prios:        {all_prios}")
   sol = sum(all_prios)
   print(f">> SOLUTION Part 1: {sol}\n")

def solve_Part2(data):
   items = [l.strip() for l in data]
   assert len(items)%3==0, "one group incomplete!"
   badges = []
   # instead of while: for i in range(0,len(items),3):
   i = 0
   #while i < len(items):
   while i <= len(items)-2:
      l1 = items[i]
      l2 = items[i+1]
      l3 = items[i+2]
      #print(l1,l2,l3)
      d =      {chr(i):0 for i in range(ord('a'),ord('z')+1)}  # 'a':0, ..., 'z':0
      d.update({chr(i):0 for i in range(ord('A'),ord('Z')+1)}) # 'A':0, ..., 'Z':0
      d1,d2,d3 = d.copy(),d.copy(),d.copy()
      
      for c in l1: d1[c] += 1
      for c in l2: d2[c] += 1
      for c in l3: d3[c] += 1
      #for l,d in zip([l1,l2,l3],[d1,d2,d3]):
      #   for c in l: d[c] += 1

      for k,v1,v2,v3 in zip(d1.keys(),d1.values(),d2.values(),d3.values()):
         if v1>0 and v2>0 and v3>0:
            badges.append(k)
            break
      # reset dicts' values
      d1 = {k:0 for k in d1.keys()}
      d2 = {k:0 for k in d2.keys()}
      d3 = {k:0 for k in d3.keys()}
      i+=3
   
   print(f"all {len(badges)} badges ({len(items)} items in total): {badges}")
   sol = sum([prios[i] for i in badges])
   print(f">> SOLUTION Part 2: {sol}\n")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)
   solve_Part2(sample_input)

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_03.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
      solve_Part2(file_data)
