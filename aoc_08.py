#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

import matplotlib
matplotlib.rcParams['figure.dpi'] = 150
"""
- count the number of trees that are visible from outside the grid when looking directly along a row or column
- input represents 2D tree-height map, 0: shortest, 9: tallest
- tree is visible if all of the other trees between it and an edge of the grid are shorter than it
- all of the trees around the edge of the grid are visible
Part 2:
- viewing_distance (find first tree that is of same height or taller (>=) than the considered tree)
"""

sample_input = [
"30373\n",
"25512\n",
"65332\n",
"33549\n",
"35390\n"
]

def get_dat_from_list(data):
   s1,s2 = len(data),len(data[0])
   dat = np.array([int(c) for l in data for c in l]).reshape((s1,s2))
   return dat
def discrete_matshow(fig, ax, data, tick_step=1):
   cmap = plt.get_cmap('jet', np.max(data)-np.min(data)+1) # 'RdBu', 'plasma', 'magma', 'oranges', 'jet'
   mat = ax.matshow(data, cmap=cmap, vmin=np.min(data)-0.5, vmax=np.max(data)+0.5)
   #cax = fig.colorbar(mat,ax=ax,ticks=np.arange(np.min(data),np.max(data)+1,tick_step))
   #cax = fig.colorbar(mat,ticks=np.arange(np.min(data),np.max(data)+1,tick_step))
   divider = make_axes_locatable(ax)
   cax = divider.append_axes('right', size='5%', pad='10%')
   fig.colorbar(mat, cax=cax, ticks=np.arange(np.min(data),np.max(data)+1, tick_step))
def discrete_matshow_with_grid(fig, ax, data, tick_step=1):
   discrete_matshow(fig, ax, data, tick_step=1)
   # grid for matshow
   ax.set_xticks(range(data.shape[1]))
   ax.set_yticks(range(data.shape[0]))
   ax.set_xticks([x-0.5 for x in ax.get_xticks()][1:], minor='true')
   ax.set_yticks([y-0.5 for y in ax.get_yticks()][1:], minor='true')
   #ax.grid(which='minor', color='k', linestyle='-', linewidth=0.4)
   ax.grid(which='minor') #TODO: grid lines are not exactly centered @ticks

   if max(data.shape)>20:
      def get_sparse_ticks(ticks):
         """
         ticks in [xticks,yticks]
         usage: get_sparse_ticks(ax.get_xticks())
         """
         mask = np.array([False]*len(ticks))
         mask[::10] = True
         mask = ~mask
         ticks = [str(e) for e in ticks]
         for i in range(len(ticks)):
            if mask[i]: ticks[i] = ''
         return ticks
      
      ax.set_xticklabels(get_sparse_ticks(ax.get_xticks()), minor=False)
      ax.set_yticklabels(get_sparse_ticks(ax.get_yticks()), minor=False)

def show_data(dat):
   fig,ax = plt.subplots(1,2)
   fig.suptitle('tree height map')

   ax[0].set_title('discrete_matshow')
   discrete_matshow_with_grid(fig,ax[0],dat)

   ax[1].set_title('imshow')
   cax = make_axes_locatable(ax[1]).append_axes('right', size='5%', pad='10%')
   im = ax[1].imshow(dat,cmap='turbo') # inferno, jet, Purples, turbo
   fig.colorbar(im,cax=cax, ticks=np.arange(np.min(dat),np.max(dat)+1,1))
   
   fig.tight_layout()
   fig.subplots_adjust(wspace=0.3)
   plt.show()


def solve(data):
   print(f"data: {data}")
   data = [l.strip() for l in data]
   dat = get_dat_from_list(data)
   print(f"dat, shape={dat.shape}, size={dat.size}:\n{dat}")
   
   show_data(dat)

   N_edge_trees = dat.shape[0]*2 + (dat.shape[1]-2)*2
   print(f"number of edge trees: {N_edge_trees}")
   dat_inner = dat[1:-1,1:-1]
   print(f"dat_inner, shape={dat_inner.shape}:\n{dat_inner}\n")
   
   #––– TODO: go row-wise on dat, then go row-wise on dat.T
   #...

   def is_visible_from_edge(dat,i,j):
      """     x
         .–––––>
         |
       y |  +–––+–––+–––+–––+–
         v  |   |   |   |   |  ...
            +–––+–––+–––+–––+–
            |   |   |   |   |  ...
            +–––+–––+–––+–––+–
            |   |   |   |   |  ...
            .  .  .  .  . 

         numpy array: column major
         i == y: [0,...,dat.shape[0]-1]
         j == x: [0,...,dat.shape[1]-1]
         dat[i,j] == dat[row,col] == dat[y,x]

         left:    y=i, x: 0,...,j-1
         right:   y=i, x: j+1,...,dat.shape[0]-1
         top:     x=j, y: 0,...,i-1
         bottom:  x=j, y: i+1,...,dat.shape[1]-1
      """
      left_x   = np.arange(0,j)
      left_y   = i*np.ones(left_x.shape,dtype=int)
      right_x  = np.arange(j+1,dat.shape[1])
      right_y  = i*np.ones(right_x.shape,dtype=int)
      top_y    = np.arange(0,i)
      top_x    = j*np.ones(top_y.shape,dtype=int)
      bottom_y = np.arange(i+1,dat.shape[0])
      bottom_x = j*np.ones(bottom_y.shape,dtype=int)

      x_indices = [left_x,right_x,top_x,bottom_x]
      y_indices = [left_y,right_y,top_y,bottom_y]

      #––– Part 1
      for x,y in zip(x_indices,y_indices):
         #print(f"i,j:{i},{j} –– y,x:{y},{x}")
         #print(f">>> dat[i,j]: {dat[i,j]}")
         #print(f"dat[y,x]: {dat[y,x]}")
         if np.all(dat[y,x] < dat[i,j]):
            return True
      return False

   def get_scene_score(dat,i,j):
      #––– Part 2: np.argwhere(dat[y,x]>=dat[i,j])[0][0]
      viewed_trees = []
      b_found = False
      val = dat[i,j]
      
      #~~~ left ~~~~~~~~~~~~~
      for idx in np.arange(j-1,-1,-1): # [j-1:0] in steps -1
         #print(f"{dat[i,idx]} ",end='')
         if dat[i,idx] >= val:
            d = j-idx
            b_found = True
            break
      if not b_found: d = j
      viewed_trees.append(d)
      b_found = False
      #print()
      #~~~~~~~~~~~~~~~~~~~~~~

      #~~~ right ~~~~~~~~~~~~
      for idx in np.arange(j+1,dat.shape[1]): # [j+1:Nx] in steps -1
         #print(f"{dat[i,idx]} ",end='')
         if dat[i,idx] >= val:
            d = idx-j
            b_found = True
            break
      if not b_found: d = dat.shape[1]-j-1
      viewed_trees.append(d)
      b_found = False
      #print()
      #~~~~~~~~~~~~~~~~~~~~~~
      
      #~~~ top ~~~~~~~~~~~~~~
      for idx in np.arange(i-1,-1,-1): # [i-1:0] in steps -1
         #print(f"{dat[idx,j]} ",end='')
         if dat[idx,j] >= val:
            d = i-idx
            b_found = True
            break
      if not b_found: d = i
      viewed_trees.append(d)
      b_found = False
      #print()
      #~~~~~~~~~~~~~~~~~~~~~~

      #~~~ bottom~~~~~~~~~~~~
      for idx in np.arange(i+1,dat.shape[0]): # [i+1:Ny] in steps -1
         #print(f"{dat[idx,j]} ",end='')
         if dat[idx,j] >= val:
            d = idx-i
            b_found = True
            break
      if not b_found: d = dat.shape[0]-i-1
      viewed_trees.append(d)
      b_found = False
      #print()
      #~~~~~~~~~~~~~~~~~~~~~~

      # SOLUTION (sample)  Part1,Part2==21,8
      # SOLUTION (file)    Part1,Part2==1690,535680
      """
      print(dat[left_y,left_x])
      res = np.argwhere(dat[left_y,left_x]>=dat[i,j])
      print(res)
      d = j if res.size==0 else j-res[0]
      viewed_trees.append(d)

      res = np.argwhere(dat[right_y,right_x]>=dat[i,j])
      d = dat.shape[1]-j-1 if res.size==0 else res[0]-j
      viewed_trees.append(d)

      res = np.argwhere(dat[top_y,top_x]>=dat[i,j])
      d = i if res.size==0 else i-res[0]
      viewed_trees.append(d)

      res = np.argwhere(dat[bottom_y,bottom_x]>=dat[i,j])
      d = dat.shape[0]-i-1 if res.size==0 else res[0]-i
      viewed_trees.append(d)
      """
      assert viewed_trees, "shouldn't be empty!"
      score = np.prod(viewed_trees,dtype=int)
      #print(f"viewed trees: {viewed_trees}, score: {score}")
      return score

   N_visible = 0
   scores = []
   for i in range(1,dat.shape[0]-1):
      for j in range(1,dat.shape[1]-1):
         #––– Part 1
         if is_visible_from_edge(dat,i,j): N_visible += 1
         #––– Part 2
         scores.append(get_scene_score(dat,i,j))
   print(f"number of visible inner trees: {N_visible}")
   print(f">> SOLUTION Part 1: {N_edge_trees+N_visible}")
   #print(f"scores: {scores}")
   print(f">> SOLUTION Part 2: {np.max(scores)}")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_08.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
