#!/usr/bin/env python3

import numpy as np
"""
start-of-packet marker:    sequence of  4 chars that are all different
start-of-message marker:   sequence of 14 chars that are all different
"""
sample_input = [
"mjqjpqmgbljsphdztnvjfqwrcgsmlb\n",
"bvwbjplbgvbhsrlpgdmjqwftvncz\n",
"nppdvjthqldpwncqszvftbrmjlhg\n",
"nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg\n",
"zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw\n"
]

def find_packet_start_pos(s,n_diff_chars=4):
   assert (len(s)-n_diff_chars) > 0, "length ERROR!"
   for i in range(len(s)-n_diff_chars):
      sub_str = s[i:i+n_diff_chars]
      #if np.unique(list(sub_str)).size == n_diff_chars:
      if len(set(sub_str)) == n_diff_chars:
         print(f"found marker of len {n_diff_chars}: {sub_str} @pos {i}")
         return i
   raise Exception("precondition violated!")

def solve(data):
   input_str = data.strip()
   print(f"input_str: {input_str}")
   n_diff_chars = 14 # 4,14
   marker_start_pos = find_packet_start_pos(input_str,n_diff_chars)
   res = marker_start_pos + n_diff_chars    # N chars from beginning to end of marker
   print(f">> SOLUTION Part 1/2 with n_diff_chars={n_diff_chars}: {res}\n")


if __name__ == "__main__":
   #––– sample input
   for s in sample_input:
      print("for sample input:")
      solve(s)

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_06.txt', 'r') as f:
      file_data = f.readlines()[0]
      solve(file_data)
