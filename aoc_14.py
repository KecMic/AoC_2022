#!/usr/bin/env python3

import numpy as np
from time import sleep
"""
    rock –> #  // from input
     air –> .
sand src –> +  // starts @(500,0)

   input represents horizontal/vertical lines of rock (#)
   
   sand falls (in order of preference, starting with highest)
      - straight down:  (1 D)
      - down left:      (1 D),(1 L)
      - down right:     (1 D),(1 R)
      - else:           fix
"""
sample_input = [
"498,4 -> 498,6 -> 496,6\n",
"503,4 -> 502,4 -> 502,9 -> 494,9\n"
]

def flatten_list_of_lists(ll):
   return [e for l in ll for e in l]

def get_extend_from_flat_data(flat_data):
   min_x = min(flat_data,key=lambda x: x[0])[0]
   min_y = min(flat_data,key=lambda x: x[1])[1]
   max_x = max(flat_data,key=lambda x: x[0])[0]
   max_y = max(flat_data,key=lambda x: x[1])[1]
   return (min_x,max_x), (min_y,max_y)

def show(arr,min_x,max_x,min_y,max_y):
   #show = lambda arr: [print("  ~"+l.tobytes().decode('UTF-8')+"~") for l in arr]
   sand_pos = 500-min_x
   l_pad,r_pad = "  ~ ", " ~"
   l,m,r = list(str(min_x)),list(str(500)),list(str(max_x))
   l_pos,r_pos = 0,arr[0].size-1
   header_row = list(' '*arr[0].size)
   header = []
   fw = len(str(arr.shape[0]))
   for i in range(3):
      h = header_row.copy()
      #for pos,n in zip([l_pos,sand_pos,r_pos],[l,m,r]): h[pos] = n[i]
      h[l_pos]    = l[i]
      h[sand_pos] = m[i]
      h[r_pos]    = r[i]
      header.append(f"{' ':{fw}}" + ' '*len(l_pad) + ''.join(h) + ' '*len(r_pad))
   print()
   [print(h) for h in header]
   [print( f"{i:{fw}}" + l_pad + l.tobytes().decode('UTF-8') + r_pad) for i,l in enumerate(arr)]

def pos_in_list(pos,l):
   return np.any(list(map(lambda x: pos[0]==x[0] and pos[1]==x[1],l)))

def is_within_bounds(pos,min_x,max_x,min_y,max_y):
   """ pos: np.array, bounds defined by [min_x,max_x], [min_y,max_y] """
   x,y = pos
   return x>=min_x and x<=max_x and y<=max_y

def solve(data,vis_progress=False):
   data = [[[int(num) for num in e.strip().split(",")] for e in l.strip().split("->")] for l in data]
   print(f"data: {data}")
   sand_src_pos = np.array([500,0])

   flat_data = flatten_list_of_lists(data)
   (min_x,max_x),(min_y,max_y) = get_extend_from_flat_data(flat_data)
   Nx = max_x-min_x+1
   Ny = max_y+1 # start at y=0 #max_y-min_y+1
   print(f"min_x,max_x min_y,max_y –– Ny,Nx: {min_x,max_x} {min_y,max_y} –– {Ny,Nx}")

   rocks = []
   for path in data:
      for i in range(len(path)-1):
         s = path[i]
         e = path[i+1]
         sx,sy = np.sign(np.array(e) - np.array(s))
         """
         s[0] == e[0] => vertical line
         s[1] == e[1] => horizontal line
         """
         if   s[0] == e[0]: [rocks.append((s[0],y)) for y in range(s[1],e[1],sy*1)] # e[1] +/- 1
         elif s[1] == e[1]: [rocks.append((x,s[1])) for x in range(s[0],e[0],sx*1)] # e[0] +/- 1
      # add last one
      rocks.append(path[-1])
   print(f"got {len(rocks)} rocks in total:\n{rocks}")

   # use map: x->list of y
   map_x2ys = {}
   for r in rocks:
      x,y = r
      if not x in map_x2ys:
         map_x2ys[x] = [y]
      else:
         """
         how is this possible, that y is added multiple times without if ?!?
         => some paths are appearing multiple times in input !!! so check if y is already in m[x],
            or use set instead of list: map_x2ys[x] = {y}, map_x2ys[x].add(y)
         """
         if y not in map_x2ys[x]:
            map_x2ys[x].append(y)

   print("map:")
   for k,v in map_x2ys.items():
      print(f"k–>v: {k}–>{v}")

   screen = np.chararray((Ny,Nx))
   screen[:] = '.'
   screen[0,500-min_x] = '+'
   for r in rocks: screen[r[1],r[0]-min_x] = '#'
   show(screen,min_x,max_x,min_y,max_y); print()

   occupied_pos = rocks.copy()
   occupied_by_sand = []
   print(f"got {len(occupied_pos)} occupied (rocks or sand) in total:\n{occupied_pos}")
   
   print("–"*60)
   running = True
   sand_units = 0
   while running:
      if vis_progress:
         # ASCII-print
         print(f"sand unit {sand_units}")
         for o in occupied_by_sand: screen[o[1],o[0]-min_x] = 'o'
         show(screen,min_x,max_x,min_y,max_y); print()
         #sleep(0.05)

         ### why is (500,3) shown as (500,9) in show !?!
         #if (500,3) in occupied_by_sand: exit()
         """print(f"min_y,min_x,screen.shape: {min_y},{min_x},{screen.shape}")
         [print(l.tobytes().decode('UTF-8')) for l in screen]
         for e in occupied_by_sand:
            if np.all(e==(500,3)): exit()
         """
      sand_units += 1
      if sand_units%10==0: print(f"iter {sand_units}")
      sand_pos = np.array([500,0])
      #occupied_pos.append((500,7))
      while True:
         
         # find lowest possible y for current sand_pos.x (where sand can drop to)
         ###pred = lambda occupied,sand_pos: occupied[0]==sand_pos[0] and occupied[1]>sand_pos[1]
         ###filt = filter(lambda x: pred(x,sand_pos),occupied_pos)
         ###if not filt:
         ###   running = False
         ###   break
         ###filt = sorted(filt,key=lambda x: x[1],reverse=True)[-1] #filt = sorted(filt,key=lambda x: x[1],reverse=True)[-1], filt = min(filt,key=lambda x: x[1])
         ###print(f"filt old: {filt}")


         # speed up the above: only look along y of current sand_pos.x
         pred = lambda occupied_y,sand_pos_y: occupied_y>sand_pos_y
         y_vals = map_x2ys[sand_pos[0]]
         filt_y = list(filter(lambda y: pred(y,sand_pos[1]), y_vals)) # make result of filter (generator expression) a list, so can use it multiple times, and if result is only one scalar, it will be also list, so subsequent sorted-call works

         if not filt_y:
            running = False
            break
         
         filt_y = sorted(filt_y,reverse=True)[-1]
         filt = (sand_pos[0],filt_y)


         #print(f"filt: {filt}")
         sand_pos = filt + np.array(( 0,-1))
         left     = filt + np.array((-1, 0))
         right    = filt + np.array((+1, 0))
         #print(f"sand_pos(down),diag-left,diag-right: {tuple(sand_pos)},{tuple(left)},{tuple(right)}")
         
         # try: down, diag-left, diag-right, if all 3 blocked => finished, append pos to occupied
         # finish generating sand if new position would be out-of-bounds (remember to deduct 1 of sand_units!)
         #if left not in occupied_pos and is_within_bounds(left,min_x,max_x,min_y,max_y):
         left_is_within_bounds  = is_within_bounds(left,  min_x,max_x,min_y,max_y)
         right_is_within_bounds = is_within_bounds(right, min_x,max_x,min_y,max_y)
         left_is_occupied  = (left[0]  in map_x2ys) and (left[1]  in map_x2ys[left[0] ]) #pos_in_list(left,  occupied_pos)
         right_is_occupied = (right[0] in map_x2ys) and (right[1] in map_x2ys[right[0]]) #pos_in_list(right, occupied_pos)
         #print(f"left/right within_bounds: {left_is_within_bounds,right_is_within_bounds}")
         #print(f"left/right is occupied  : {left_is_occupied,right_is_occupied}")
         if not left_is_occupied:
            if not left_is_within_bounds:
               ### Part 2 START ###
               #TODO
               sand_pos = left + (0,2)
               occupied_pos.append(sand_pos)
               occupied_by_sand.append(sand_pos) # for DEBUG
               # add sand_pos to map_x2ys
               x,y = sand_pos
               if not x in map_x2ys:
                  map_x2ys[x] = [y]
               else:
                  assert y not in map_x2ys[x], "y vals should be unique"
                  map_x2ys[x].append(y)
               ### Part 2 END ###
               running = False
               break
            else:
               # left not occupied && left within bounds
               sand_pos = left
               continue
         #if right not in occupied_pos  and is_within_bounds(right,min_x,max_x,min_y,max_y):
         if not right_is_occupied:
            if not right_is_within_bounds:
               running = False
               break
            else:
               # right not occupied && right within bounds
               sand_pos = right
               continue
         # !(!a && !b) => a || b
         #print(f"adding sand @pos: {tuple(sand_pos)}")
         occupied_pos.append(sand_pos)
         occupied_by_sand.append(sand_pos) # for DEBUG
         #++++++++++++++++++++++
         # add sand_pos to map_x2ys
         x,y = sand_pos
         if not x in map_x2ys:
            map_x2ys[x] = [y]
         else:
            assert y not in map_x2ys[x], "y vals should be unique"
            map_x2ys[x].append(y)
         #for k,v in map_x2ys.items(): print(f"k–>v: {k}–>{v}")
         #++++++++++++++++++++++
         break
   
   print("––– finally:")
   # ASCII-print
   for o in occupied_by_sand: screen[o[1],o[0]-min_x] = 'o'
   show(screen,min_x,max_x,min_y,max_y); print()

   res1 = sand_units-1
   print(f">> SOLUTION Part 1 (final num of sand units): {res1}")
   print(f">> SOLUTION Part 2 (?): ?")


if __name__ == "__main__":
   """TODO: use KD-tree to store occupied 2D-points in for faster lookup ???
   => of little/no use here, as I don't want nearest-neighbor(s), but only want scan along y-direction
   """
   """from scipy import spatial
   data = np.random.random((50,2))
   kd_tree = spatial.KDTree(data)
   print(kd_tree)
   exit()"""

   #––– sample input
   print("for sample input:")
   solve(sample_input,vis_progress=False)
   exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_14.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data,vis_progress=False)
