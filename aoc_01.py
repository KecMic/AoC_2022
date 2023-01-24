#!/usr/bin/env python3

import numpy as np

sample_input = [
"1000\n",
"2000\n",
"3000\n",
"\n",
"4000\n",
"\n",
"5000\n",
"6000\n",
"\n",
"7000\n",
"8000\n",
"9000\n",
"\n",
"10000\n"
]

def solve_short(data):
   print("short solution:")
   total_cals_per_elf = [s.split() for s in ''.join(data).split("\n\n")]
   #all_sums = max(map(lambda l: sum([int(v) for v in l]), total_cals_per_elf))
   all_sums = max([sum([int(e) for e in l]) for l in total_cals_per_elf])
   print(f"Part 1: {all_sums}")
   max3_sum = sum(sorted([sum([int(e) for e in l]) for l in total_cals_per_elf],reverse=True)[:3])
   print(f"Part 2: {max3_sum}\n")

def solve(data):
   cals_per_elf = ''.join(data).split("\n\n")
   total_cals_per_elf = [s.split() for s in cals_per_elf]
   print(f"data:               {data}")
   print(f"cals_per_elf:       {cals_per_elf}")
   print(f"total_cals_per_elf: {total_cals_per_elf}")
   all_sums = []
   for l in total_cals_per_elf:
      cals_sum = np.sum([int(e) for e in l])
      all_sums.append(cals_sum)
   print(f"all_sums:           {all_sums}")
   max_idx = np.argmax(all_sums)
   max_cals = all_sums[max_idx]
   print(f"elf {max_idx+1} carrying most calories: {max_cals} calories")
   print(f">> SOLUTION Part 1: {max_cals}")

   #––– Part 2
   """
   not using first/last 3 indices of sorted values:
      https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array
   """
   max3indices = np.argpartition(all_sums,-3)[-3:] # get indices of top 3
   print(f"max3indices: {max3indices}")
   max3_cals = np.array(all_sums)[max3indices]
   max3_sum = np.sum(max3_cals)
   print(f"max3_cals:   {max3_cals}")
   print(f"max3_sum:    {max3_sum}")
   print(f">> SOLUTION Part 2: {max3_sum}\n")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)
   solve_short(sample_input)

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_01.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
      solve_short(file_data)
