#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import os
"""
- heightmap
   'a' –> lowest elevation
   'z' –> highest elevation
   'S': current pos   (has elevation 'a')
   'E': goal pos      (has elevation 'z')
- Part 1: go from 'S' to 'E' in as few steps as possible (shortest path)
   - each step, can move 1 up, down, left or right –– and <=1 higher
"""
sample_input = [
"Sabqponm\n",
"abcryxxl\n",
"accszExk\n",
"acctuvwj\n",
"abdefghi\n"
]

def show(arr):
   [print('|' + l.tobytes().decode('UTF-8') + '|') for l in arr]
   print('`' + '~'*len(arr[0]) + '´')
def get_dat_from_list(data):
   s1,s2 = len(data),len(data[0])
   dat = np.array([ord(c) for l in data for c in l]).reshape((s1,s2))
   return dat
def plot_dat(fig,ax,dat,show_nums=False):
   ax.matshow(dat,cmap=plt.cm.Blues)
   if show_nums:
      for (i,j),v in np.ndenumerate(dat):
         ax.text(j,i,v,
            ha='center',va='center',
            bbox=dict(boxstyle='round',facecolor='black',alpha=1.0),
            fontweight='bold',fontsize=10,fontfamily='monospace',
            color='orange')

def find_neighbors(u,mat):
   # 4-neighbors
   Ny,Nx = mat.shape
   neighbors = []
   if u[1]!=0:    neighbors.append((u[0]  ,u[1]-1))  # L
   if u[1]!=Nx-1: neighbors.append((u[0]  ,u[1]+1))  # R
   if u[0]!=0:    neighbors.append((u[0]-1,u[1]  ))  # U
   if u[0]!=Ny-1: neighbors.append((u[0]+1,u[1]  ))  # D
   return neighbors
def Dijkstra(mat,src_idx):
   #print(f"–– Dijkstra ––\nsrc_idx: {src_idx}, mat:\n{mat}")
   print(f"–– Dijkstra ––\nsrc_idx: {src_idx}")
   # distances to src
   dist = np.ones(mat.shape,dtype=int)
   dist[:] = np.prod(mat.shape)*100 # np.inf
   dist[src_idx[0],src_idx[1]] = 0
   # previous node of mat[j,i] as (i,j)
   prev = np.ones(mat.shape,dtype=object)
   prev[:] = -1
   # queue
   #Q = [((i,j),v) for (i,j),v in np.ndenumerate(dist)]
   Q = [(src_idx,0)]

   while Q:
      #print(f"dist:\n{dist}\nprev:\n{prev}")
      Q = [((i,j),dist[i,j]) for (i,j),v in Q] # recompute dist-vals, as Q works with indices, but we update dist
      Q = sorted(Q,reverse=True,key=lambda x: x[1]) # imitate prio-Q: sort so that smallest dist[i,j] is at back of list
      #print(f"Q:\n{Q}")
      u,val = Q.pop()
      #if u == (2,5): return dist,prev
      #print(f"current u: {u} with dist[u]={dist[u[0],u[1]]}")
      neighbors = find_neighbors(u,mat)
      valid_neighbors = [n for n in neighbors if (mat[n[0],n[1]]-mat[u[0],u[1]] <= 1)]
      #print(f"  all 4-neighbors of {u} – {mat[u[0],u[1]]:3}: {neighbors}")
      #print(f"valid 4-neighbors of {u} – {mat[u[0],u[1]]:3}: {valid_neighbors}")

      for n in valid_neighbors:
         #d_height = mat[n[0],n[1]] - mat[u[0],u[1]]
         #print(f"d_height: {d_height}")
         #d_Manh = np.sum(np.abs(np.array(n)-np.array(u))) # this is always 1 in a 4-neighborhood
         alternative = dist[u[0],u[1]] + 1 # +d_height
         #cond = (d_height != -1 and np.abs(d_height) <= 1)
         #cond = (d_height==0 or d_height==1)
         if alternative < dist[n[0],n[1]]:# and cond:
            #print(f"setting dist[n[0],n[1]]={dist[n[0],n[1]]} to alt={alternative}")
            dist[n[0],n[1]] = alternative
            prev[n[0],n[1]] = u
            if n in [q[0] for q in Q]:
               # if n already in Q => decrease_prio (as my Q contains indices, no need to change element of Q directly)
               pass
            else:
               # if n not already in Q => add_with_prio
               #print(f"appending {n} to Q")
               Q.append((n,-1)) # -1 doesn't matter, as we update at beginning of loop
   return dist,prev
def shortestPathFromDijkstra(prev,endpos,startpos):
   path = [endpos]
   u = endpos
   while prev[u[0],u[1]] != -1: #prev[u[0],u[1]] != startpos:
      u = prev[u[0],u[1]]
      #print(f"prev of u={u} is {prev[u[0],u[1]]}")
      path.append(u)
   #path.append(startpos)
   path.reverse()
   return path
def UCS(mat,src_idx):
   print(f"–– uniform-cost search ––: mat,src_idx:\n{mat}\n{src_idx}")
   # TODO
def GreedyNext(mat,src_idx,endpos):
   # works for sample, but not for real input...
   print(f"–– GreedyNext ––\nsrc_idx: {src_idx}, mat:\n{mat}")
   # distances to src
   dist = np.ones(mat.shape,dtype=int)
   dist[:] = np.prod(mat.shape)*100 # np.inf
   dist[src_idx[0],src_idx[1]] = 0
   # previous node of mat[j,i] as (i,j)
   prev = np.ones(mat.shape,dtype=object)
   prev[:] = -1
   # visited
   pos = src_idx
   visited = np.zeros(mat.shape,dtype=bool)
   visited = [pos]
   i = 1
   while pos != endpos:
      #u_idx = np.argmin([dist[i,j] for (i,j) in Q])
      #u = Q[u_idx] #Q.pop()
      #visited.append(u)
      #visited.append(pos)
      #if u == (2,5): return dist,prev
      neighbors = find_neighbors(pos,mat)
      height_diffs = np.array([mat[n[0],n[1]]-mat[pos[0],pos[1]] for n in neighbors])
      #valid_heights_idx = np.where(np.logical_or(height_diffs==0,height_diffs==1))[0]
      #print(f"height_diffs:      {height_diffs}")
      #print(f"valid_heights_idx: {valid_heights_idx}")
      # prefer distance 1 over distance 0
      candidates = np.hstack((np.where(height_diffs==1)[0],np.where(height_diffs==0)[0]))
      candidates = [c for c in candidates if neighbors[c] not in visited]
      goal_dist = [np.sum( np.array(neighbors[c]) - np.array(endpos) ) for c in candidates]
      rem_dist  = [np.abs(e) for e in goal_dist]
      min_dist_idx = np.argmin(rem_dist) # only works if rem_dist is never empty!!
      #print(f"goal_dist:    {goal_dist}")
      #print(f"min_dist_idx: {min_dist_idx}")
      #print(f"goal_dist: {[np.sum(e) for e in goal_dist]}")
      #print(f"candidates stacked: {candidates}")
      for i,candidate in enumerate(candidates):
         if i==min_dist_idx:
            n = neighbors[candidate]
            #print(f"neighbor:{n}")
            dist[n[0],n[1]] = dist[pos[0],pos[1]] + 1
            prev[n[0],n[1]] = pos
            pos = n
            break
      # add only current pos (not neighbors) to visited
      visited.append(pos)
      #print(f"–– dist,prev:\n{dist}\n{prev}")

   return dist,prev

def show_path(dat,path,S,E):
   # show as "ASCII-art" on terminal
   disp = np.chararray(dat.shape)
   disp[:] = '.'
   disp[S] = 'S'
   disp[E] = 'E'
   print()
   show(disp); print()
   for i in range(len(path)-1):
      cur = path[i]
      nxt = path[i+1]
      if   nxt[0]-cur[0]== 1 and nxt[1]-cur[1]== 0: disp[cur[0],cur[1]] = 'v'
      elif nxt[0]-cur[0]==-1 and nxt[1]-cur[1]== 0: disp[cur[0],cur[1]] = '^'
      elif nxt[0]-cur[0]== 0 and nxt[1]-cur[1]== 1: disp[cur[0],cur[1]] = '>'
      elif nxt[0]-cur[0]== 0 and nxt[1]-cur[1]==-1: disp[cur[0],cur[1]] = '<'
      else: raise Exception("sth went wrong!")
   show(disp); print()

def solve(data):
   data = [l.strip() for l in data]
   dat = get_dat_from_list(data)
   print(f"data: {data}\n")
   [print(f"  {l}") for l in data]
   print(f"\ndat:\n{dat}")

   S = np.where(dat==ord('S')) #np.array(list(map(int,np.where(dat==ord('S')))))
   E = np.where(dat==ord('E')) #np.array(list(map(int,np.where(dat==ord('E')))))
   #d = E-S # get preferred direction from d
   Ny,Nx = dat.shape
   print(f"S,E: {S},{E} –– Ny,Nx: {Ny,Nx}")

   pos    = tuple(map(int,S))
   endpos = tuple(map(int,E))
   print(f"starting @pos {pos} –– desired endpos: {endpos}")
   dat[S] = ord('a')
   dat[E] = ord('z')

   # in terminal: $ PLOT=1 python aoc_12.py
   if os.environ.get('PLOT')=='1':
      fig,ax = plt.subplots(figsize=(12,8))
      plot_dat(fig,ax,dat,show_nums=False)
      plt.show()

   dist,prev = Dijkstra(dat,pos)
   path = shortestPathFromDijkstra(prev,endpos,pos)
   print(f"Dijkstra result –– dist,prev:\n{dist}\n{prev}")
   print(f"prev,endpos,pos: {endpos,pos}")
   #print(f"shortest path from src to dst: {path}")
   shortest_path_len = len(path)-1
   print(f"length of shortest path:       {shortest_path_len}")
   show_path(dat,path,S,E)

   #–– Part 2
   # brute force...
   all_starting_pos = np.where(dat==ord('a'))
   all_paths = []
   all_path_lengths = []
   all_pos = []
   #for pos in zip(all_starting_pos[0],all_starting_pos[1]):
   for pos in zip(*all_starting_pos):
      dist,prev = Dijkstra(dat,pos)
      path = shortestPathFromDijkstra(prev,endpos,pos)
      path_len = len(path)-1
      if path_len > 0:
         all_paths.append(path)
         all_path_lengths.append(path_len)
         all_pos.append(pos)
   for pl in all_path_lengths:
      print(f"length of this shortest path: {pl}")

   min_path_idx = np.argmin(all_path_lengths)
   min_path = all_paths[min_path_idx]
   min_path_S = all_pos[min_path_idx] #list(zip(*all_starting_pos))[min_path_idx]
   assert np.min(all_path_lengths) == all_path_lengths[min_path_idx], "sth is wrong!"
   min_path_len = np.min(all_path_lengths)
   print(f"starting from an arbitrary 'a', shortest path is of len {min_path_len}, starting @{min_path_S}:")
   show_path(dat,min_path,min_path_S,E)

   """dist,prev = GreedyNext(dat,pos,endpos)
   print(f"GreedyNext result –– dist,prev:\n{dist}\n{prev}")
   path = shortestPathFromDijkstra(prev,endpos)
   #print(f"shortest path from src to dst: {path}")
   print(f"length of shortest path:       {len(path)-1}")"""

   ##"""
   ##preferred movement starting with most desirable: [move up, stay]
   ##pick next pos among neighbors as the one with shortest (Manhatten) distance to end
   ##"""
   ##neighbor_distances = [np.sum(np.array(endpos)-np.array(n)) if n != None else -1 for n in neighbors]
   ##max_dist_idx = np.argmax(neighbor_distances)
   ##sorted_dist_and_idx = sorted(zip(neighbor_distances,range(len(neighbor_distances))),reverse=True)
   ##sorted_neighbor_indices = [e[1] for e in sorted_dist_and_idx]
   ##
   ##print(f"current pos {pos}")
   ##print(f"neighbors (L,R,U,D) (i,j): {neighbors}")
   ##print(f"neighbor_distances: {neighbor_distances}")
   ##print(f"max_dist_idx: {max_dist_idx}")
   ##print(f"sorted_dist_and_idx: {sorted_dist_and_idx}")
   ##print(f"sorted_neighbor_indices: {sorted_neighbor_indices}")
   print(f">> SOLUTION Part 1: {shortest_path_len}")
   print(f">> SOLUTION Part 2: {min_path_len}\n")

if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)
   exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_12.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
