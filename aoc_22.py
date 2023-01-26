#!/usr/bin/env python3

import numpy as np
"""
- You begin the path in the leftmost open tile of the top row of tiles.
  Initially, you are facing to the right (from the perspective of how the map is drawn).
- Rows start from 1 at the top and count downward;
- Cols start from 1 at the left and count rightward. 
- Facing is
   0 for right (>)
   1 for down  (v)
   2 for left  (<)
   3 for up    (^)

idea: maybe preprocess map and store
   all positions of '#' => store: (sorted) map[line_idx] –> list of y_idx
   extent_data: [0,Nx-1] => only store: Nx-1
   leftmost_valid_map_idx (board_map[leftmost_valid_map_idx] in ['.','#']
      => in general, this would be a list of ranges [(b1,e1),(b2,e2),...]
         in our case: [(b1,e1)] == [(leftmost_valid_map_idx,Nx-1)] => only store: leftmost_valid_map_idx
idea: use 2D-array as board_map, as I will need to search along both x and y

TODO:
   handle < and > (horizontal movement) together somehow...
         >:  find
         >: rfind
   handle ^ and v (vertical movement) together somehow...
"""
sample_input = [
"        ...#\n",
"        .#..\n",
"        #...\n",
"        ....\n",
"...#.......#\n",
"........#...\n",
"..#....#....\n",
"..........#.\n",
"        ...#....\n",
"        .....#..\n",
"        .#......\n",
"        ......#.\n",
"\n",
"10R5L5R10L4R5L5\n"
]

def commands_from_path(path):
   commands = []
   start_idx = 0
   for i in range(len(path)):
      if path[i] in ['L','R']:
         # assume that L and R is always followed by a number, otherwise n would be empty string
         num = path[start_idx:i]
         assert num, "precondition [L and R always followed by a number] violated"
         commands.append(num)       # num
         commands.append(path[i])   # L/R
         start_idx = i+1
   commands.append(path[start_idx:]) # append last one
   return commands

def get_next_heading(current_heading,turn_cmd):
   """ turn_cmd in ['L','R'], current_heading in ['^','>','v','<'] """
   all_headings = "^>v<" # stored in cyclic order ;)
   N = len(all_headings)
   step = {'R': +1, 'L': -1}
   assert turn_cmd in ['L','R'], "precondition violated!"
   idx = (all_headings.find(current_heading) + step[turn_cmd]) % N
   return all_headings[idx]

def test__get_next_heading():
   """
   current state contains
      current 2D-position in map
         (y,x)
      current heading
         left/west   L/W   <
         right/east  R/E   >
         up/north    U/N   ^
         down/south  D/S   v
   """
   state = {
      'pos': (1,2),
      'heading': '>'
   }

   print("–– test__get_next_heading ––")
   print(f"initial state: {state}")
   for turn_cmd in ['L','R']:
      print(f"turn_cmd: {turn_cmd}")
      for i in range(5):
         next_heading = get_next_heading(state['heading'],turn_cmd)
         print(f"  heading (current|next): {state['heading']}|{next_heading}")
         state['heading'] = next_heading
   print()

def show(disp_arr):
   print()
   [print('|'+l.tobytes().decode('UTF-8')+'|') for l in disp_arr]
   print()

# simulate: found_pos = board_map[:,x].find('#',y)
def fing_along_y(board_map,x,y_range_start,y_range_end,c='#',reverse=False):
   found_pos = -1
   if reverse: r = range(y_range_end,y_range_start-1,-1)
   else:       r = range(y_range_start,y_range_end) # for iy in range(y+1,Nx):
   for iy in r:
      if board_map[iy][x] == c:
         found_pos = iy
         break
   
   return found_pos

def find_next_pos(board_map,current_state,n_moves,disp_map):
   pos = current_state['pos']
   current_heading = current_state['heading']
   y,x = pos
   Ny,Nx = len(board_map),len(board_map[y])


   if current_heading == '^':
      pass
   
   if current_heading == '>':
      # >: THIS SEEMS TO WORK => prototype for all others
      found_pos = board_map[y].find('#',x+1)
      print(f"found_pos: {found_pos}")
      if found_pos == -1:
         # Starting at (y,x), did't find '#' anywhere along x-dir. Check whether we we have to wrap around.
         num_max_steps_x = Nx-1-x
         print(f"num_max_steps_x: {num_max_steps_x}")
         if n_moves <= num_max_steps_x:
            # we can move there
            pos = (y,x+n_moves)
         else:
            # wrap around (potentially multiple times ?!?)
            n_over = n_moves - num_max_steps_x
            found_pos = board_map[y].find('#',0,n_over-1) # str.find(what,start,end) // [start,end], both incl.
            if found_pos == 0 or board_map[y][found_pos-1] == ' ':
               # '#' at leftmost beginning => move to rightmost end of field
               rightmost_x = board_map[y].rfind('.')
               assert rightmost_x == Nx
               pos = (y,rightmost_x) #pos = (pos[0],board_map[y][rightmost_x])
            elif found_pos == -1:
               # didn't find any '#'
               if n_over >= Nx:
                  print(f"WRAP AROUND {n_over//Nx} TIMES!")
                  # wrap around multiple times
                  pos = (y,(n_over%Nx)-1)
               else:
                  print(f"WRAP AROUND 1 TIME!")
                  pos = (y,n_over-1)
            else:
               # move one before '#'
               pos = (y,found_pos-1)

      else:
         # found '#', so move for n_moves steps, or right before '#'
         new_pos_x = x+n_moves
         if new_pos_x < Nx:
            # we can move there
            pos = (y,new_pos_x)
         else:
            # move one before '#'
            pos = (y,found_pos-1)
   
   if current_heading == 'v':
      found_pos = fing_along_y(board_map,x,y+1,Nx,'#')
      print(f"found_pos: {found_pos}")
      if found_pos == -1:
         # Starting at (y,x), did't find '#' anywhere along y-dir. Check whether we we have to wrap around.
         last_valid_y_idx = fing_along_y(board_map,x,0,Ny-1,'.',reverse=True)
         num_max_steps_y = last_valid_y_idx-y
         print(f"num_max_steps_y: {num_max_steps_y}")
         if n_moves <= num_max_steps_y:
            # we can move there
            pos = (y+n_moves,x)
         else:
            # wrap around (potentially multiple times ?!?)
            n_over = n_moves - num_max_steps_y
            topmost_y = fing_along_y(board_map,x,0,Ny-1,'.')
            found_pos = fing_along_y(board_map,x,topmost_y,topmost_y+n_over-1,'#')

            if found_pos == 0 or board_map[found_pos-1][x] == ' ':
               # '#' at topmost beginning => move to downmost end of field
               downmost_y = fing_along_y(board_map,x,0,Ny-1,'.',reverse=True) # TODO: topmost_y instead of 0
               pos = (downmost_y,x)
            elif found_pos == -1:
               # didn't find any '#'
               if n_over-1 > last_valid_y_idx:
                  print(f"WRAP AROUND {n_over//Ny} TIMES!")
                  # wrap around multiple times
                  pos = ((n_over%Ny)-1,x)
               else:
                  print(f"WRAP AROUND 1 TIME!")
                  pos = (n_over-1,x)
            else:
               # move one before '#'
               pos = (found_pos-1,x)
      else:
         # found '#', so move for n_moves steps, or right before '#'
         new_pos_y = y+n_moves
         if new_pos_y < Ny:
            # we can move there
            pos = (new_pos_y,pos[1])
         else:
            # move one before '#'
            pos = (found_pos-1,pos[1])
   
   if current_heading == '<':
      pass

   disp_map[pos] = 'x'; show(disp_map)
   return pos

def solve(data):
   print('~'*50,''.join(data),'~'*50,sep='\n')
   #data = [l.strip() for l in data]
   #print(f"data: {data}")
   
   # split into board_map and path
   board_map,path = ''.join(data).split("\n\n")
   """print(f"board_map:\n{board_map}")
   print(f"path:\n{[path]}")"""
   # path
   path = path[:-1]
   """print(f"path: {path}")"""
   commands = commands_from_path(path)
   """print(f"commands: {commands}")"""
   # boardmap
   N_chars = len(board_map)
   N_walls = board_map.count('#')
   print(f"map contains {N_chars} chars in total")
   print(f"map contains {N_walls} walls, thats {(N_walls/N_chars*100):.2f} %")
   board_map = board_map.split("\n")
   """print(f"board_map: {board_map}")"""
   x_max = max(map(len,board_map))
   """print(f"x_max: {x_max}")"""
   disp_map = np.chararray((len(board_map),x_max)) # H,W –– Ny,Nx
   disp_map[:] = ' '
   for i,line in enumerate(board_map):
      #print(f"line of length {len(line):2}: |{line}|")
      #disp_map[i,:len(line)] = '.'
      for j in range(len(line)):
         disp_map[i,j] = line[j]
   #print(disp_map)

   show(disp_map)

   print('–'*50)
   # find starting position at leftmost open tile ('.') of top row
   start_pos = (0,board_map[0].find('.'))
   print(f"start_pos (y,x): {start_pos}")
   
   state = {
      'pos': start_pos,
      'heading': '>'
   }
   print(f"initial state: {state}")
   disp_map[state['pos']] = 'x'; show(disp_map)
   
   cmd_idx = 0
   all_positions = [(state['pos'],state['heading'])]
   while cmd_idx < len(commands):
      current_cmd = commands[cmd_idx]
      print(f"–– current cmd,heading: {current_cmd},{state['heading']}")
      if current_cmd in ['L','R']:
         # turn in-place
         state['heading'] = get_next_heading(state['heading'],current_cmd)
      else:
         # advance in direction of current heading, if possible
         n_moves = int(current_cmd)
         print(f"n_moves: {n_moves}")
         next_pos = find_next_pos(board_map,state,n_moves,disp_map)
         all_positions.append((next_pos,state['heading']))
         print(f"next_pos: {next_pos}")
         state['pos'] = next_pos
      cmd_idx += 1

   print(f"all_positions: {all_positions}")
   for i,(p,h) in enumerate(all_positions):
      disp_map[p] = str(i)
      show(disp_map)

   # show path
   show_path(board_map,all_positions,x_max)
   print(f">> SOLUTION Part 1/2: ?")

def show_path(board_map,all_positions,x_max):
   # show as "ASCII-art" on terminal
   Ny = len(board_map)
   disp = np.chararray((Ny,x_max)) # H,W –– Ny,Nx
   disp[:] = ' '
   for i,line in enumerate(board_map):
      for j in range(len(line)):
         disp[i,j] = line[j]

   print("initially:")
   show(disp)
   disp_initial = disp.copy()

   path = [p for (p,h) in all_positions]

   for i in range(len(path)-1):
      cur = path[i]
      nxt = path[i+1]
      h = all_positions[i+1][1]
      #print(f"cur,nxt,h: {cur},{nxt},{h}")


      if nxt[0]==cur[0] and nxt[1]==cur[1]:
         disp[cur[0],cur[1]] = h
         continue
      if nxt[0]==cur[0]:
         Nx = len(board_map[cur[0]])
         # >>> or <<<
         if nxt[1]>cur[1]:
            if h == '>':
               # >>>
               #for x in range(cur[1],nxt[1]): disp[cur[0],x] = '>'
               r = range(cur[1],nxt[1])
               disp[cur[0],r] = '>'
            else:
               # <<<
               r = list(range(cur[1],-1,-1)) + list(range(Nx-1,nxt[1],-1))
               disp[cur[0],r] = '<'
         else:
            #for x in range(cur[1],nxt[1],-1): disp[cur[0],x] = '<'
            if h == '<':
               # <<<
               r = range(cur[1],nxt[1],-1)
               disp[cur[0],r] = '<'
            else:
               # >>>
               #print(cur[0],cur[1],Nx)
               r = list(range(cur[1],Nx)) + list(range(0,nxt[1]))
               disp[cur[0],r] = '>'
      if nxt[1]==cur[1]:
         # vvv or ^^^
         if nxt[0]>cur[0]:
            if h == 'v':
               # vvv
               r = range(cur[0],nxt[0])
               disp[r,cur[1]] = 'v'
            else:
               # ^^^
               topmost_y = fing_along_y(board_map,x,0,Ny-1,'.')
               r = range(cur[0],topmost_y-1,-1)
               disp[r,cur[1],] = '^'
               #last_valid_y_idx = len(board_map[cur[0]])-1 #TODO: not right
               last_valid_y_idx = fing_along_y(board_map,cur[1],0,Ny-1,'.',reverse=True)
               r = range(last_valid_y_idx,nxt[0],-1)
               disp[r,cur[1]] = '^'
         else:
            if h == '^':
               # <<<
               r = range(cur[0],nxt[0],-1)
               disp[r,cur[0]] = '^'
            else:
               # >>>
               downmost_y = fing_along_y(board_map,cur[1],0,Ny-1,'.',reverse=True)
               topmost_y = fing_along_y(board_map,cur[1],0,Ny-1,'.')
               r = list(range(cur[0],downmost_y+1)) + list(range(topmost_y,nxt[0]))
               disp[r,cur[1]] = 'v'

      
      #show(disp)

   print("path taken:")
   show(disp)
   show(disp_initial)

   bridge = "  '  "
   disp_side_by_side = np.chararray((Ny,x_max*2+len(bridge)))
   disp_side_by_side[:] = ' '
   disp_side_by_side[:,:x_max] = disp_initial
   disp_side_by_side[:,x_max:x_max+len(bridge)] = list(bridge)
   disp_side_by_side[:,x_max+len(bridge):] = disp
   fw = x_max+len(bridge)//2
   print(f"|{'initially':{fw}}|{'path taken':{fw}}|")
   print('`'+'–'*fw+'+'+'–'*fw+'´') #print('–'*(disp_side_by_side.shape[1]+2))
   show(disp_side_by_side)


if __name__ == "__main__":
   #––– tests
   #test__get_next_heading()
   #––– sample input
   print("for sample input:")
   solve(sample_input)
   exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_22.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
