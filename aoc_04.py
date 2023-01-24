#!/usr/bin/env python3

"""
- 2-4 means [2,4], i.e. {2,3,4}
- PartI: find all pairs where one range fully contains the other
"""
sample_input = [
"2-4,6-8\n",
"2-3,4-5\n",
"5-7,7-9\n",
"2-8,3-7\n",
"6-6,4-6\n",
"2-6,4-8\n",
]

def is_fully_contained(r):
   """ input: of the form [[2, 4], [6, 8]] """
   r1,r2 = r
   # check if r1 is fully contained in r2
   if r1[0] >= r2[0] and r1[1] <= r2[1]: return 1
   # check if r2 is fully contained in r1
   if r2[0] >= r1[0] and r2[1] <= r1[1]: return 1
   return 0

def ranges_overlap(r):
   r1,r2 = r
   if r1[0] <= r2[0]:
      if r1[1] >= r2[0]: return 1
   else:
      if r2[1] >= r1[0]: return 1
   return 0

def solve(data):
   items = [l.strip().split(',') for l in data]
   #print(items)
   N_fully_contained_ranges = 0
   N_overlaps = 0
   for pair in items:
      ranges = [p.split('-') for p in pair]
      #print(ranges)
      #ranges = [map(lambda x: int(x), r) for r in ranges]
      ranges = [[int(r[0]),int(r[1])] for r in ranges]
      #print(ranges)
      N_fully_contained_ranges += is_fully_contained(ranges)
      #––– Part 2
      N_overlaps += ranges_overlap(ranges)
   print(f">> SOLUTION Part 1: {N_fully_contained_ranges}")
   print(f">> SOLUTION Part 2: {N_overlaps}\n")


   """ the following only works if all numbers are single digits (0-9) """
   if 1:
      import numpy as np
      #data.append("10-25,11-22\n") # to test with numbers >9
      items = [l.strip().split(',') for l in data]
      N_items = len(items)
      items = [int(n) for l in items for e in l for n in e.split('-')]
      x_max = max(items)
      print(f"x_max: {x_max}")
      if x_max>9:
         print(f"!! x_max>9, not visualizing this !!")
         return
      arr = np.chararray((N_items*3,x_max + 2*len(str(x_max))+1 + 2))
      arr[:] = '.'
      print(f"arr.shape: {arr.shape}")

      def show(disp_arr):
         [print('| '+l.tobytes().decode('UTF-8')+' |') for l in disp_arr]

      items = [l.strip().split(',') for l in data]
      for i,pair in enumerate(items):
         r1,r2 = [[int(r[0]),int(r[1])] for r in [p.split('-') for p in pair]]
         print(r1,r2)
         for v in range(r1[0],r1[1]+1): arr[i*3,v-1] = str(v)
         for v in range(x_max,x_max+2): arr[i*3,v] = ' '
         for v in range(x_max+2,arr.shape[1]): arr[i*3,v] = '#'
         arr[i*3,x_max+2] = str(r1[0])
         #arr[i*3,x_max+2:x_max+2+len(str(r1[0]))] = str(r1[0])
         arr[i*3,x_max+2+1] = '-'
         arr[i*3,x_max+2+2] = str(r1[1])

         for v in range(r2[0],r2[1]+1): arr[i*3+1,v-1] = str(v)
         for v in range(x_max,x_max+2): arr[i*3+1,v] = ' '
         for v in range(x_max+2,arr.shape[1]): arr[i*3+1,v] = '#'
         arr[i*3+1,x_max+2  ] = str(r2[0])
         arr[i*3+1,x_max+2+1] = '-'
         arr[i*3+1,x_max+2+2] = str(r2[1])

         for j in range(x_max): arr[i*3+2,j] = ' '
         for v in range(x_max,arr.shape[1]): arr[i*3+2,v] = ' '
      #print(arr)
      show(arr)


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_04.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
