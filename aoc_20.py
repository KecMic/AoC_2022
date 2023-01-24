#!/usr/bin/env python3

import numpy as np
from tqdm import tqdm
"""
                        when to move which number (at its current pos)

  ._____________________ 1.––.       8.  15.
  |  .__________________ 2.<–´–.     9.   .
  |  |  ._______________ 3.<–––´–.  10.   .
  |  |  |  .____________ 4.<–––––´   .    .
  |  |  |  |  ._________ 5.          .    
  |  |  |  |  |  .______ 6.          .    
  |  |  |  |  |  |  .___ 7.         14.   
  |  |  |  |  |  |  |
  1  2 -3  3 -2  0  4

  1  2 -3  3 -2  0  4
  `>>+´
  
  2  1 -3  3 -2  0  4
  `>>.>>+´
  
  1 -3  2  3 -2  0  4
  #<<´       `+<<.<<.
  1  2  3 -2 -3  0  4

       1 -3  2  3 -2  0  4
       1  2  3 -2  0  4 -3   # 1 <
       1  2  3 -2  0 -3  4   # 2 <
       1  2  3 -2 -3  0  4   # 3 <
  
  1  2  3 -2 -3  0  4
        `>>.>>.>>+´
  1  2 -2 -3  0  3  4
  #<<.<<´          `+
  1  2 -3  0  3  4 -2
           *
  1  2 -3  0  3  4 -2
  .>>.>>.>>.>>+´  `>>#
       
       1  2 -3  0  3  4 -2
       4  1  2 -3  0  3 -2   # 1 >
       1  4  2 -3  0  3 -2   # 2 >
       1  2  4 -3  0  3 -2   # 3 >
       1  2 -3  4  0  3 -2   # 4 >


 2 % 7 => 5
-1 % 7 => 6

check out if there is only one single '0' in the input and at which line:
   ~$ grep "^0" -n input_20.txt
"""

sample_input = [
"1\n",
"2\n",
"-3\n",
"3\n",
"-2\n",
"0\n",
"4\n"
]

def get_new_idx(arr,old_idx):
   N = len(arr)
   n = arr[old_idx]
   new_idx = None
   if n > 0:
      new_idx = (n+old_idx) % (N-1)
      if old_idx==N-1 and new_idx==0: new_idx = N-1
   else:
      new_idx = (n-(N-1-old_idx)) % (N-1)
      if old_idx!=0 and new_idx==0: new_idx = N-1
   return new_idx

def shift_all_left_by_1_cyclic(arr,old_idx,new_idx):
   """
   - shift all elems in [old_idx,new_idx] left by 1, cyclically
   - old_idx and new_idx are valid indices in arr
   """
   assert old_idx < new_idx, "precondition violated!"
   tmp = arr[old_idx]
   for i in range(old_idx,new_idx,+1):
      arr[i] = arr[i+1]
   arr[new_idx] = tmp
   """# return a map of the changed indices: old_idx –> new_idx
   map_old2new = {i: i-1 for i in range(old_idx+1,new_idx+1)}
   map_old2new[old_idx] = new_idx
   return map_old2new"""

def shift_all_right_by_1_cyclic(arr,old_idx,new_idx):
   """
   - shift all elems in [old_idx,new_idx] right by 1, cyclically
   - old_idx and new_idx are valid indices in arr
   """
   assert old_idx > new_idx, "precondition violated!"
   tmp = arr[old_idx]
   for i in range(old_idx,new_idx,-1):
      arr[i] = arr[i-1]
   arr[new_idx] = tmp
   """# return a map of the changed indices: old_idx –> new_idx
   map_old2new = {i: i+1 for i in range(new_idx,old_idx)}
   map_old2new[old_idx] = new_idx
   return map_old2new"""

def print_before_and_after(old_idx,new_idx,arr_before,arr_after):
   print(f"  old_idx,new_idx:   {old_idx},{new_idx}")
   print(f"  initially:         {arr_before}")
   
   fw = np.max( list(map(lambda x: len(str(x)), [np.min(arr_after),np.max(arr_after)])) )
   s,e = (old_idx,new_idx) if old_idx < new_idx else (new_idx,old_idx)
   r = range(s,e+1)
   arr_str = ""
   for i,v in enumerate(arr_after):
      if i in r:
         arr_str += f"\033[1;33m{v:{fw}}\033[0;0m "
      else:
         arr_str += f"{v:{fw}} "
   
   #print(f"  after shift:       {arr_after}")
   print(f"  after shift:       [{arr_str}\b]")

def testing_nums(orig_arr,nums_kind="negative"):
   #if nums_kind != "negative" and nums_kind != "positive":
   if not (nums_kind == "negative" or nums_kind == "positive"):
      raise Exception("only support 'negative' and 'positive'")
   
   N = len(orig_arr)
   for old_idx in range(N):
      for n in range(1,N+(N-1)*1):
         if nums_kind == "negative": n = -n
         print(f"testing n={n} @idx {old_idx}:")
         arr = orig_arr.copy()
         arr[old_idx] = n
         arr_before_shift = arr.copy()
         new_idx = get_new_idx(arr,old_idx)
         if new_idx==old_idx:
            print(f"  new==old, nothing to do for\n  {arr_before_shift}")
            continue
         elif new_idx > old_idx:
            shift_all_left_by_1_cyclic(arr, old_idx, new_idx)
            print_before_and_after(old_idx, new_idx, arr_before_shift, arr)
         else: #new_idx < old_idx
            shift_all_right_by_1_cyclic(arr, old_idx, new_idx)
            print_before_and_after(old_idx, new_idx, arr_before_shift, arr)
      print("–"*5)

def test_shifting(N_entries=5):
   print("testing cyclic shifting:")
   xi = [f"x{i}" for i in range(N_entries)]
   orig = np.array(xi,dtype=object) # dtype=object, so I can mix int with strings
   print("–"*50)
   testing_nums(orig,nums_kind="positive")
   print("–"*50)
   testing_nums(orig,nums_kind="negative")
   print("–"*50)

def get_old_idx(nums_indices,list_idx):
   for j,v in enumerate(nums_indices):
      if v == list_idx:
         return j
   raise Exception("shouldn't get here!")

""" 
TODO: no separate nums_indices and arr, but zip them in array of pairs (idx,num)
pairs = [(idx,num) for (idx,num) in zip(range(N),data)] #np.array(data.copy())
print(f"pairs: {pairs}")
print(f"indices: {[p[0] for p in pairs]}")
print(f"numbers: {[p[1] for p in pairs]}")
TODO: only shift indices, ans use map_idx2num
"""
def mix_arr(data,arr,nums_indices):
   N = len(data)
   for i in tqdm(range(N)):
      list_idx = i % N
      #if list_idx==0: print("–––")
      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      n = data[list_idx]
      arr_before_shift = arr.copy()
      #old_idx = nums_indices[list_idx]
      old_idx = get_old_idx(nums_indices,list_idx)
      new_idx = get_new_idx(arr,old_idx)
      #print(f"idx % N: {list_idx} –– num: old_idx –> new_idx: {n:2}: {old_idx}–>{new_idx}")

      if new_idx==old_idx:
         #print(f"  new==old, nothing to do for\n  {arr_before_shift}")
         continue
      elif new_idx > old_idx:
         # update arr
         shift_all_left_by_1_cyclic(arr, old_idx, new_idx)
         # update nums_indices
         shift_all_left_by_1_cyclic(nums_indices, old_idx, new_idx)
         """print(f"  nums_indices after [shift L]: {nums_indices}")
         print_before_and_after(old_idx, new_idx, arr_before_shift, arr)"""
      else: #new_idx < old_idx
         # update arr
         shift_all_right_by_1_cyclic(arr, old_idx, new_idx)
         # update nums_indices
         shift_all_right_by_1_cyclic(nums_indices, old_idx, new_idx)
         """print(f"  nums_indices after [shift R]: {nums_indices}")
         print_before_and_after(old_idx, new_idx, arr_before_shift, arr)"""
      
      #print(f"  from nums_indices: {np.array([data[i] for i in nums_indices])}")
      #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      #if i==7-1: break
   """print(f"after round {i_round+1}, arr:")
   [print(e) for e in arr]"""

def solve(data,whichPart="Part1"):
   data = [int(l.strip()) for l in data]
   N = len(data)
   arr = np.array(data.copy())
   #print(f"data: {data}")
   print(f"have \033[1;31m{len(arr)-len(np.unique(arr))}\033[0;0m non-unique vals")

   nums_indices = [i for i in range(N)]
   #print(f"nums_indices initially: {nums_indices}")
   
   #––– Part 1
   if whichPart=="Part1":
      mix_arr(data,arr,nums_indices)

   #––– Part 2
   if whichPart=="Part2":
      arr *= 811589153
      for i_round in tqdm(range(10)):
         mix_arr(data,arr,nums_indices)


   print(f"arr:               {arr}")
   print(f"from nums_indices: {np.array([data[i] for i in nums_indices])}")
   zero_idx = np.where(arr==0)[0][0]
   print(f"0 @idx {zero_idx} –– N elems left of 0: {arr.size-1-zero_idx}")
   # get 1000th, 2000th, and 3000th number after 0 (wrap around)
   req_indices = [(zero_idx+offset)%N for offset in np.array([1000,2000,3000])]
   print(f"idxs of 1000th,2000th,3000th num after zero_idx: {req_indices}")
   print(f"nums of 1000th,2000th,3000th num after zero_idx: {arr[req_indices]}")
   print(f">> SOLUTION Part 1/2 (sum of these 3 nums): {sum(arr[req_indices])}")


if __name__ == "__main__":
   #––– testing cyclic shifting
   #test_shifting()
   #exit()

   #––– sample input
   print("for sample input:")
   solve(sample_input,whichPart="Part1")
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_20.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data,whichPart="Part1")


"""
##note:
##   np.roll(a, 1) == right_shift(a,1)
##   np.roll(a,-1) == left_shift(a,1)
##shift positive:
##   2  1 -3  3 -2  0  4
##   `>>.>>´
##         2  1 -3  3 -2  0  4
##         `>>´
##         1  2 -3  3 -2  0  4
##            `>>´
##         1 -3  2  3 -2  0  4
##shift negative:
##   2  1 -3  3 -2  0  4
##         `<<.<<´
##         2  1 -3  3 -2  0  4
##                  `<<´
##         2  1 -3 -2  3  0  4
##               `<<´
##         2  1 -2 -3  3  0  4
##
def shift_positive(a,old_idx,new_idx):
   # number n > 0
   # => shift n to right by n
   #    and all @idx
   #       index_of(n)+n, index_of(n)+(n-1), ..., index_of(n)+1
   #    to the left
   tmp = a[old_idx]
   for i in range(old_idx+1,new_idx+1,+1):
      a[i-1] = a[i]
   a[new_idx] = tmp

def shift_negative(a,old_idx,new_idx):
   # number n < 0
   # => shift n to left by n
   #    and all @idx
   #       index_of(n)-|n|, index_of(n)-(|n|-1), ..., index_of(n)-1
   #    to the right
   tmp = a[old_idx]
   for i in range(old_idx-1,new_idx-1,-1):
      a[i+1] = a[i]
   a[new_idx] = tmp

a = np.array((2,  1, -3,  3, -2,  0,  4))
print(f"a before: {a}")
shift_positive(a,0,2)
print(f"a after:  {a}")
print("–––")
a = np.array((2,  1, -3,  3, -2,  0,  4))
print(f"a before: {a}")
shift_negative(a,4,2)
print(f"a after:  {a}")
"""