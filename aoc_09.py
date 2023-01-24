#!/usr/bin/env python3

import numpy as np
from time import sleep
"""
+––––––––––+––––––––––+
| entities | commands |    absolute positions [x,y] of H and T in grid
+––––––––––+––––––––––+    
| H: head  | R: right |    y ^
| T: tail  | U: up    |      |
|          | L: left  |      ·–––> 
|          | D: down  |          x
+––––––––––+––––––––––+    

description:
   - start with H and T at same pos (e.g.: (0,0))
   - T always follows H
   - input moves H
   - after each step, update pos of T, if H is no longer adjacent to T
   - Part 1: count up all of the positions the tail visited at least once
   - Part 2: not only H and T, but now: [H, 1, 2, 3, 4, 5, 6, 7, 8, 9] with 9==newTail
      - Rather than 2 knots, you now must simulate a rope consisting of 10 knots.
        One knot is still the H of the rope and moves according to the series of motions.
        Each knot further down the rope follows the knot in front of it using the same rules as before.
all valid configurations/states:
   with
      x_diff := H.x-T.x
      y_diff := H.y-T.y

   1  |...HT...|  –– (H.y == T.y) and (x_diff == -1)
   2  |...TH...|  –– (H.y == T.y) and (x_diff == +1)
   3  |...X...|   –– (H.y == T.y) and (H.x == T.x) // H == T

   4  |...T...|   –– (H.x == T.x) and (y_diff == -1)
      |...H...|

   5  |...H...|   –– (H.x == T.x) and (y_diff == +1)
      |...T...|

   6  |...T..|    –– (H.x != T.x) and (H.y != T.y) and (x_diff == -1) and (y_diff == -1)
      |..H...|

   7  |..T...|    –– (H.x != T.x) and (H.y != T.y) and (x_diff == +1) and (y_diff == -1)
      |...H..|

   8  |...H..|    –– (H.x != T.x) and (H.y != T.y) and (x_diff == +1) and (y_diff == +1)
      |..T...|

   9  |..H...|    –– (H.x != T.x) and (H.y != T.y) and (x_diff == -1) and (y_diff == +1)
      |...T..|

FSM (depending on current state, command requires certain action which will again result in a valid state):
   if    cmd == U => H.y += 1
      if state in [1,2,3,4,6,7]  => T stays (don't move T)
      elif state == 5   => T.y += 1
      elif state == 8   => T += ( 1, 1)
      elif state == 9   => T += (-1, 1)
   elif  cmd == R => H.x += 1
      if state in [1,3,4,5,6,9]  => T stays (don't move T)
      elif state == 2   => T.x += 1
      elif state == 7   => T += ( 1,-1)
      elif state == 8   => T += ( 1, 1)
   elif  cmd == D => H.y += -1
      if state in [1,2,3,5,8,9]  => T stays (don't move T)
      elif state == 4   => T.y += -1
      elif state == 6   => T += (-1,-1)
      elif state == 7   => T += ( 1,-1)
   elif  cmd == L => H.x += -1
      if state in [2,3,4,5,7,8]  => T stays (don't move T)
      elif state == 1   => T.x += -1
      elif state == 6   => T += (-1,-1)
      elif state == 9   => T += (-1, 1)

notes
   - TODO regarding Pos2D
      - just use np.array instead..., and use H[0] and H[1] for H.x and H.y
      - BUT: cannot add np.array to set() => **TypeError: unhashable type: 'numpy.ndarray'**
         => unhashable: np.array, list [],
         => hashable: tuple ()
   - trace out path of H and T in 2D grid
   - this is snake! go implement it!
"""

"""
TODO:
   note that the added values in exec_cmd are exactly the diff in get_state !
   so maybe exec_cmd based on distance (if abs(diff)==2 => T follows H)
   => see solve_v2
      
      ###
      |.T.H.|
         if x_diff==+2 and y_diff == 0  => T+=(+1, 0) ==(sign(x_diff),0)
      |.H.T.|
         if x_diff==-2 and y_diff == 0  => T+=(-1, 0) ==(sign(x_diff),0)
      ###
      |.H.|
      |...|
      |.T.|
         if x_diff== 0 and y_diff ==+2  => T+=( 0,+1) ==(0,sign(y_diff))
      |.T.|
      |...|
      |.H.|
         if x_diff== 0 and y_diff ==-2  => T+=( 0,-1) ==(0,sign(y_diff))
      ###
      |..H.|
      |....|
      |.T..|
         if x_diff==+1 and y_diff ==+2  => T+=(+1,+1) ==(sign(x_diff),sign(y_diff))
      |..T.|
      |....|
      |.H..|
         if x_diff==-1 and y_diff ==-2  => T+=(-1,-1) ==(sign(x_diff),sign(y_diff))
      |.H..|
      |....|
      |..T.|
         if x_diff==-1 and y_diff ==+2  => T+=(-1,+1) ==(sign(x_diff),sign(y_diff))
      |.T..|
      |....|
      |..H.|
         if x_diff==+1 and y_diff ==-2  => T+=(+1,-1) ==(sign(x_diff),sign(y_diff))
      ###
      |...H.|
      |.T...|
         if x_diff==+2 and y_diff ==+1  => T+=(+1,+1) ==(sign(x_diff),sign(y_diff))
      |...T.|
      |.H...|
         if x_diff==-2 and y_diff ==-1  => T+=(-1,-1) ==(sign(x_diff),sign(y_diff))
      |.H...|
      |...T.|
         if x_diff==-2 and y_diff ==+1  => T+=(-1,+1) ==(sign(x_diff),sign(y_diff))
      |.T...|
      |...H.|
         if x_diff==+2 and y_diff ==-1  => T+=(+1,-1) ==(sign(x_diff),sign(y_diff))

      ==>>
         if x_diff==2 or y_diff==2:
            T += (sign(x_diff),sign(y_diff))
"""

sample_input = [
"R 4\n",
"U 4\n",
"L 3\n",
"D 1\n",
"R 4\n",
"D 1\n",
"L 5\n",
"R 2\n"
]

sample_input_part2 = [
"R 5\n",
"U 8\n",
"L 8\n",
"D 3\n",
"R 17\n",
"D 10\n",
"L 25\n",
"U 20\n"
]

class Pos2D:
   def __init__(self,x,y):
      self.x = x
      self.y = y
   def __str__(self):
      return f"({self.x},{self.y})"
   def copy(self):
      return Pos2D(self.x,self.y)
   def __add__(self,other):   # T operator+(const T& lhs, const T& rhs)
      x = self.x + other.x
      y = self.y + other.y
      return Pos2D(x,y)
   def __sub__(self,other):   # T operator-(const T& lhs, const T& rhs)
      x = self.x - other.x
      y = self.y - other.y
      return Pos2D(x,y)
   def __eq__(self,other):    # bool operator==(const T& lhs, const T& rhs)
      return ((self.x==other.x) and (self.y==other.y))
   def to_tuple(self):
      return (self.x,self.y)

def get_state(H,T):
   diff = H-T
   x_diff = H.x-T.x
   y_diff = H.y-T.y
   if    (y_diff ==  0) and (x_diff == -1): return 1 # diff == Pos2D(-1, 0)
   elif  (y_diff ==  0) and (x_diff == +1): return 2 # diff == Pos2D(+1, 0)
   elif  (y_diff ==  0) and (x_diff ==  0): return 3 # diff == Pos2D( 0, 0)
   elif  (y_diff == -1) and (x_diff ==  0): return 4 # diff == Pos2D( 0,-1)
   elif  (y_diff == +1) and (x_diff ==  0): return 5 # diff == Pos2D( 0,+1)
   elif  (y_diff == -1) and (x_diff == -1): return 6 # diff == Pos2D(-1,-1)
   elif  (y_diff == -1) and (x_diff == +1): return 7 # diff == Pos2D(+1,-1)
   elif  (y_diff == +1) and (x_diff == +1): return 8 # diff == Pos2D(+1,+1)
   elif  (y_diff == +1) and (x_diff == -1): return 9 # diff == Pos2D(-1,+1)
   else: raise Exception("sth went wrong!")

def exec_cmd(H,T,cmd):
   state = get_state(H,T)
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   if    cmd == 'U':
      H.y += 1
      # if state in [1,2,3,4,6,7]: # => T stays (don't move T)
      if   state == 5: T.y += 1
      elif state == 8: T += Pos2D( 1, 1)
      elif state == 9: T += Pos2D(-1, 1)
   elif  cmd == 'R':
      H.x += 1
      #if state in [1,3,4,5,6,9]: # => T stays (don't move T)
      if   state == 2: T.x += 1
      elif state == 7: T += Pos2D( 1,-1)
      elif state == 8: T += Pos2D( 1, 1)
   elif  cmd == 'D':
      H.y += -1
      #if state in [1,2,3,5,8,9]: # => T stays (don't move T)
      if   state == 4: T.y += -1
      elif state == 6: T += Pos2D(-1,-1)
      elif state == 7: T += Pos2D( 1,-1)
   elif  cmd == 'L':
      H.x += -1
      #if state in [2,3,4,5,7,8]: # => T stays (don't move T)
      if   state == 1: T.x += -1
      elif state == 6: T += Pos2D(-1,-1)
      elif state == 9: T += Pos2D(-1, 1)
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   return H,T

def set_to_list(s):
   l = []
   l.extend(s)
   return l

def solve(data):
   #print(f"data: {data}")
   data = [l.split() for l in data]

   H,T = Pos2D(0,0),Pos2D(0,0)         # np.array([0,0]), np.array([0,0])
   tail_visited_pos = set()            # p.to_tuple(), or tuple(np_arr.data)
   tail_visited_pos.add(T.to_tuple())  # add starting position of T
   
   for cmd,n in data:
      n = int(n)
      while n:
         H,T = exec_cmd(H,T,cmd)
         tail_visited_pos.add(T.to_tuple())
         n -= 1
   
   #print(f"tail_visited_pos: {tail_visited_pos}")
   res1 = len(tail_visited_pos)
   print(f">> SOLUTION Part 1 (num visited positions by tail): {res1}")
   """l = set_to_list(tail_visited_pos)
   print(l)
   print(sorted(l))"""

##### >>> the following is only for plotting START <<<
def show(disp_arr):
   # show chararray
   [print('| '+l.tobytes().decode('UTF-8')+' |') for l in disp_arr]
   print()
def show_all_visited_by_tail(tail_visited_pos,Ny,Nx):
   arr = np.chararray((Ny,Nx))
   arr[:] = '.'
   # mark all positions the tail visited with '#'
   for px,py in tail_visited_pos:
      arr[(Ny-1)-py,px] = '#'
   arr[(Ny-1)-0,0] = 's' # mark start pos @(0,0) with 's'
   print("all visited by tail:")
   show(arr)
def show_progression(all_visited_pos,Ny,Nx,x_min,y_min):
   fw = len(str(len(all_visited_pos)-1)) # field width for printing i in loop
   arr = np.chararray((Ny,Nx))
   arr[:] = '.'
   arr[(Ny-1)-(0-y_min),(0-x_min)] = 's'
   
   print(f"\nstarting pos:")
   show(arr)
   sleep(0.3)

   # hoist 0th elem out of the loop, and start with 1st elem in loop, so I can always access previous H and T
   arr[(Ny-1)-(0-y_min),(0-x_min)] = 'H'
   print(f"i={0:{fw}}")
   show(arr)
   sleep(0.1)

   for i,(H,T) in enumerate(all_visited_pos[1:],1):
      #arr[:] = '.'
      
      (H_prev,T_prev) = all_visited_pos[i-1]
      arr[(Ny-1)-(T_prev[1]-y_min),(T_prev[0]-x_min)] = '.'
      arr[(Ny-1)-(H_prev[1]-y_min),(H_prev[0]-x_min)] = '.'
      
      #if H==T:
      #   arr[(Ny-1)-H[1],H[0]] = 'H'
      #else:
      #   arr[(Ny-1)-H[1],H[0]] = 'H'
      #   arr[(Ny-1)-T[1],T[0]] = 'T'
      
      # first T, then H, as H overwrites T if they are both on same pos – no if-else necessary
      arr[(Ny-1)-(T[1]-y_min),(T[0]-x_min)] = 'T'
      arr[(Ny-1)-(H[1]-y_min),(H[0]-x_min)] = 'H'
      
      print(f"i={i:{fw}}")
      show(arr)
      sleep(0.1)
def show_progression_10knots(all_visited_pos,Ny,Nx,x_min,y_min):
   fw = len(str(len(all_visited_pos)-1)) # field width for printing i in loop
   arr = np.chararray((Ny,Nx))
   arr[:] = '.'
   arr[(Ny-1)-(0-y_min),(0-x_min)] = 's'
   
   print(f"\nstarting pos:")
   show(arr)
   sleep(0.3)

   # hoist 0th elem out of the loop, and start with 1st elem in loop, so I can always access previous H and T
   arr[(Ny-1)-(0-y_min),(0-x_min)] = 'H'
   print(f"i={0:{fw}}")
   show(arr)
   sleep(0.1)

   for i,knots10 in enumerate(all_visited_pos[1:],1):
      # reset to '.'
      knots10_prev = all_visited_pos[i-1]
      for kx,ky in knots10_prev:
         #print("kx,ky:",kx,ky)
         arr[(Ny-1)-(ky-y_min),(kx-x_min)] = '.'
      
      """
      start with last knot '9', end with 'H', as node closer to H overwrites node closer to tail
      if they are both on same pos – no if-else necessary
      """
      # reversed knots
      knots10.reverse()
      # reversed labels: reverse(['H','1','2','3','4','5','6','7','8','9'])
      """labels = [str(i+1) for i in range(9)]
      labels.insert(0,'H')
      labels.reverse()"""
      labels = [str(i) for i in range(9,0,-1)]
      labels.append('H')
      for (kx,ky),label in zip(knots10,labels):
         arr[(Ny-1)-(ky-y_min),(kx-x_min)] = label
      
      print(f"i={i:{fw}}")
      show(arr)
      sleep(0.1)
##### >>> the following is only for plotting END <<<
def get_extend_from_input(data):
   data = [l.split() for l in data]
   x_visited = [0]
   y_visited = [0]
   for cmd,n in data:
      n = int(n)
      if   cmd == 'R': x_visited.append(x_visited[-1]+n)
      elif cmd == 'L': x_visited.append(x_visited[-1]-n)
      elif cmd == 'U': y_visited.append(y_visited[-1]+n)
      elif cmd == 'D': y_visited.append(y_visited[-1]-n)
   x_min,x_max = min(x_visited),max(x_visited)
   y_min,y_max = min(y_visited),max(y_visited)
   return (x_min,x_max),(y_min,y_max)

def solve_v2(data,visualize=False):
   #print(f"data: {data}")
   orig_data = data.copy()
   data = [l.split() for l in data]

   H,T = Pos2D(0,0),Pos2D(0,0)         # np.array([0,0]), np.array([0,0])
   tail_visited_pos = set()            # p.to_tuple(), or tuple(np_arr.data)
   tail_visited_pos.add(T.to_tuple())  # add starting position of T
   
   ##### >>> the following is only for plotting START <<<
   if visualize:
      all_visited_pos = [((0,0),(0,0))] # [(Hs,Ts),(H1,T1),(H2,T2),...]
   ##### >>> the following is only for plotting END <<<
   for cmd,n in data:
      n = int(n)
      while n:
         # move H first, then check if T needs update
         if   cmd == 'U': H.y += +1
         elif cmd == 'R': H.x += +1
         elif cmd == 'D': H.y += -1
         elif cmd == 'L': H.x += -1
         x_diff = H.x-T.x
         y_diff = H.y-T.y
         sx,sy = np.sign(x_diff),np.sign(y_diff) # sx,sy = map(lambda x: np.sign(x), [x_diff,y_diff])
         if np.abs(x_diff)==2 or np.abs(y_diff)==2:
            T += Pos2D(sx,sy)
         tail_visited_pos.add(T.to_tuple())
         n -= 1
         
         ##### >>> the following is only for plotting START <<<
         if visualize:
            all_visited_pos.append((H.to_tuple(),T.to_tuple()))
         ##### >>> the following is only for plotting END <<<

   #print(f"tail_visited_pos: {tail_visited_pos}")
   res1 = len(tail_visited_pos)
   print(f">> SOLUTION Part 1 (num visited positions by tail): {res1}")

   ##### >>> the following is only for plotting START <<<
   if visualize:
      # determine extend of grid for plotting
      (x_min,x_max),(y_min,y_max) = get_extend_from_input(orig_data)
      Nx = x_max-x_min+1
      Ny = y_max-y_min+1
      print(f"(x_min,x_max),(y_min,y_max): {(x_min,x_max)},{(y_min,y_max)} –– Nx,Ny: {Nx},{Ny}")
      
      # print all visited pos of H and T
      #[print(H,T) for H,T in all_visited_pos]

      # visualize progression
      show_progression(all_visited_pos,Ny,Nx,x_min,y_min)
      show_all_visited_by_tail(tail_visited_pos,Ny,Nx)
   ##### >>> the following is only for plotting END <<<
   #exit()

def solve_v2_Part2(data,visualize=False):
   orig_data = data.copy()
   data = [l.split() for l in data]
   #print(f"data: {data}")
   tail_visited_pos = set()
   knots = [Pos2D(0,0) for i in range(10)] # H==knots[0], T==knots[-1]
   tail_visited_pos.add(knots[-1].to_tuple())  # add starting position of T
   #[print(k,end=' ') for k in knots]; print()
   ############################################
   ##### >>> the following is only for plotting START <<<
   if visualize:
      all_visited_pos = [[(0,0)]*10] # [('H's,'1's,'2's,'3's,'4's,'5's,'6's,'7's,'8's,'9's),('H'1,'1'1,...),...]
   ##### >>> the following is only for plotting END <<<
   for cmd,n in data:
      n = int(n)
      while n:
         # move H, check all the other knots
         #H = knots[0]
         """
         [print(knot) for knot in knots]
         H = knots[0]
         knots[0] += Pos2D(11,22)
         [print(knot) for knot in knots]
         exit()
         """
         if   cmd == 'U': knots[0].y += +1
         elif cmd == 'R': knots[0].x += +1
         elif cmd == 'D': knots[0].y += -1
         elif cmd == 'L': knots[0].x += -1
         """
                 0' == updated 0 (H)
         0',1 => 1' == updated 1
         1',2 => 2' == updated 2
         2',3 => 3' == updated 3
         ...
         8',9 => 9' == updated 9
         """
         for idx in range(len(knots)-1):
            #knot_front = knots[idx  ] # this makes a copy, no reference!!!
            #knot_back  = knots[idx+1] # this makes a copy, no reference!!!

            x_diff = knots[idx].x-knots[idx+1].x
            y_diff = knots[idx].y-knots[idx+1].y

            sx,sy = np.sign(x_diff),np.sign(y_diff)
            if np.abs(x_diff)==2 or np.abs(y_diff)==2:
               knots[idx+1] += Pos2D(sx,sy)
               #print(f"changed knot_back: {knot_back}")
         #[print(knot) for knot in knots]
         tail_visited_pos.add(knots[-1].to_tuple())
         n -= 1

         ##### >>> the following is only for plotting START <<<
         if visualize:
            all_visited_pos.append([k.to_tuple() for k in knots])
         ##### >>> the following is only for plotting END <<<

   ############################################
   res2 = len(tail_visited_pos)
   #print(f"tail_visited_pos: {tail_visited_pos}")
   print(f">> SOLUTION Part 2 (num visited positions by new tail (9)): {res2}")
   
   ##### >>> the following is only for plotting START <<<
   if visualize:
      # determine extend of grid for plotting
      (x_min,x_max),(y_min,y_max) = get_extend_from_input(orig_data)
      Nx = x_max-x_min+1
      Ny = y_max-y_min+1
      print(f"(x_min,x_max),(y_min,y_max): {(x_min,x_max)},{(y_min,y_max)} –– Nx,Ny: {Nx},{Ny}")
      
      """if x_min<0 or y_min<0:
         print("x_min and/or y_min negative – not supported so far")
         return
      """

      # print all visited pos of H and T
      #[print(*knots10) for knots10 in all_visited_pos]

      # visualize progression
      show_progression_10knots(all_visited_pos,Ny,Nx,x_min,y_min)
   ##### >>> the following is only for plotting END <<<


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   #––– Part 1
   solve(sample_input)
   solve_v2(sample_input,visualize=False)
   #––– Part 2
   print("for sample input Part 2:")
   solve_v2_Part2(sample_input,visualize=False)
   solve_v2_Part2(sample_input_part2,visualize=False)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_09.txt', 'r') as f:
      file_data = f.readlines()
      # determine extend of grid for plotting
      (x_min,x_max),(y_min,y_max) = get_extend_from_input(file_data)
      print(f"(x_min,x_max),(y_min,y_max): {(x_min,x_max)},{(y_min,y_max)}")
      #––– Part 1
      solve(file_data)
      solve_v2(file_data,visualize=False)
      #––– Part 2
      print("for input file Part 2:")
      solve_v2_Part2(file_data,visualize=False)
