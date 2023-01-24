#!/usr/bin/env python3

import numpy as np
from time import sleep
"""
- CPU has single register X that starts with value 1
- 2 instructions
      addx V   -- takes 2 cycles
         reg X = [1]
         after having executed 'addx V'   => reg X = [1,1,1+V] # after 2nd cycle
      noop     -- takes 1 cycle
         reg X = [1]
         after having executed 'noop'     => reg X = [1,1]     # after 1st cycle
- @start of 1st cycle, the 1st instruction begins execution
   => value DURING i-th cycle is in X[i-1]
- Part 2
   - sprite 3 pixels wide, X marks middle of it –x–
   - screen 40x6
      .–––> x
      |
      v y

      - draw top to bottom row, left to right in each row
      - in each row: leftmost pixel: [0], rightmost pixel: [39]
      - draw one pixel during each cycle
      - lit: '#', dark: '.'

      If sprite is positioned such that one of its 3 pixels is the pixel currently being drawn,
      the screen produces a lit pixel (#); otherwise, the screen leaves the pixel dark (.).
         current pixel == disp_arr[row,col]
         sprite pos:
            mid == register_vals[i]
            mid-1,mid,mid+1
"""
sample_input = [
"noop\n",
"addx 3\n",
"addx -5\n"
]

def signal_strength(cycle_num,reg_value):
   return cycle_num*reg_value

def solve(data,visualize=False):
   data = [l.strip().split() for l in data]
   print(f"data: {data}")
   print(f"total of {len(data)} instructions")

   register_vals = [1]
   #  want value of register DURING 20th, 60th, 100th, 140th, 180th, 220th cycles
   nth_cycles = np.array([20+i*40-1 for i in range(6)]) # np.arange(20,220+1,40)-1
   print(f"nth_cycles (indices):    {nth_cycles}")

   for cmd in data:
      if len(cmd)==1:
         assert cmd[0]=="noop", "check preconditions"
         register_vals.append(register_vals[-1])
      elif len(cmd)==2:
         assert cmd[0]=="addx", "check preconditions"
         register_vals.extend([register_vals[-1],register_vals[-1]+int(cmd[1])])

   N_total_cycles = len(register_vals)-1
   vals = np.array(register_vals)[nth_cycles]
   signal_strengths = signal_strength(nth_cycles+1,vals)
   sss = sum(signal_strengths)
   print(f"final register value:    {register_vals[-1]}, after {N_total_cycles} cycles")
   print(f"vals:                    {vals}")
   print(f"signal strengths:        {signal_strengths}")
   print(f">> SOLUTION Part 1 (sum of signal strengths): {sss}")

   #––– Part 2
   disp_arr = np.chararray((6,40)) # H,W -- Ny,Nx
   disp_arr[:] = '.'

   #show_lambda = lambda arr: [print(l.tobytes().decode('UTF-8')) for l in arr]
   def show(disp_arr):
      [print('   '+l.tobytes().decode('UTF-8')) for l in disp_arr]
      print()
   
   print(f"disp_arr of shape Ny,Nx={disp_arr.shape}:")
   #disp_arr[0,1] = '#'
   show(disp_arr)
   #print(register_vals[:10])

   for i,reg_val in enumerate(register_vals[:-1]): # only works as last instruction is noop; in general: register_vals[:-len_last_instruction]
      sprite_pos = [reg_val-1,reg_val,reg_val+1]
      
      s = list('–'*(40+2*2)) # - - 0 1 2 .. 39 - - ### or: ['–']*(40+2*2)
      for p in sprite_pos:
         s[2+p] = '+'
      
      row,col = divmod(i,40) # n,rem
      #print(f"sprite_pos,i: {sprite_pos},{i}",end='')
      if col in sprite_pos:
         disp_arr[row,col] = '#'
         #print(" => draw #")
      else:
         disp_arr[row,col] = '-'
         #print(" => draw .")

      if visualize:
         print(f" {''.join(s)} {sprite_pos}")
         show(disp_arr)
         sleep(0.01)
      """cur_cycle_during = i+1
      print(f"\ncur_cycle,row_idx: {cur_cycle_during:3},{row}")
      # draw/don't draw pixel disp_arr[n,rem] = '#'
      print(f"row,col: {row,col}")
      disp_arr[row,col] = '+'
      show(disp_arr)
      sleep(0.01)"""

   print("final result:")
   show(disp_arr)

if __name__ == "__main__":
   #––– sample input
   ##print("for sample input:")
   ##solve(sample_input)
   print("for large sample input file:")
   with open('input_10_largeSample.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data,visualize=False)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_10.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data,visualize=False)
