#!/usr/bin/env python3

"""
   commands are of the form: move <N_crates_to_move> from <src> to <dst>
   e.g.: 'move 1 from 2 to 1'  –>  ['move', '1', 'from', '2', 'to', '1']
"""
sample_input = [
"    [D]    \n",
"[N] [C]    \n",
"[Z] [M] [P]\n",
" 1   2   3 \n",
"\n",
"move 1 from 2 to 1\n",
"move 3 from 1 to 3\n",
"move 2 from 2 to 1\n",
"move 1 from 1 to 2\n"
]

def get_newline_idx_from_lines(lines):
   for i,l in enumerate(lines):
      if l == "\n":
         return i

def cmd_extract(cmd):
      l = cmd.split()
      return int(l[1]),l[3],l[5] # N_moves, src, dst
   
def exec_cmd(cmd,crate_stacks_dict):
   N_moves,src,dst = cmd_extract(cmd)
   # make sure size of stack we're about to remove elems from is big enough to remove all N elems
   N_src_crates = len(crate_stacks_dict[src])
   assert N_moves<=N_src_crates, f"want to remove N={N_moves} elems, but only have {N_src_crates}"
   
   #––– Part 1
   #while N_moves > 0:
   #   crate_stacks_dict[dst].append(crate_stacks_dict[src].pop())
   #   N_moves -= 1

   #––– Part 2
   if N_moves==1:
      crate_stacks_dict[dst].append(crate_stacks_dict[src].pop())
   else:
      assert N_moves > 1, "assumptions made are wrong!"
      ordered_crates = crate_stacks_dict[src][-N_moves:]
      crate_stacks_dict[dst].extend(ordered_crates)
      # remove elems (moved crates) from src
      crate_stacks_dict[src] = crate_stacks_dict[src][:-N_moves]

def solve(data):
   #print(f"data: {data}")
   newline_idx = get_newline_idx_from_lines(data)
   crate_stacks_init = data[:newline_idx-1]
   crate_ids = data[newline_idx-1].strip().split() # 1 2 ...
   N_stacks = len(crate_ids)
   commands = [l.strip() for l in data[newline_idx+1:]]
   print(f"crate_stacks_init:  {crate_stacks_init}")
   print(f"crate_ids:          {crate_ids}")
   #print(f"commands:           {commands}")
   
   # map: stack_id -> crates // crates[0] @bottom, crates[-1] @top
   crate_stacks_dict = {i: [] for i in crate_ids}
   print(f"crate_stacks_dict:  {crate_stacks_dict}")

   # crate labels/names' idx: 1, 1+4, 1+2*4, ...
   crate_name_indices = [1+i*4 for i in range(N_stacks)]
   print(f"crate_name_indices: {crate_name_indices}")
   for line in crate_stacks_init:
      crate_names = [line[idx] for idx in crate_name_indices]
      for i,name in enumerate(crate_names):
         if name != " ":
            crate_stacks_dict[str(i+1)].append(name)
   # reverse all, as I added them top down (could also iterate bottom up, then no subsequent reverse necessary)
   for v in crate_stacks_dict.values():
      v.reverse()
   print(f"crate_stacks_dict:  {crate_stacks_dict}")

   # here the work/moving is done
   for cmd in commands:
      exec_cmd(cmd,crate_stacks_dict)
   
   print(f"crate_stacks_dict:  {crate_stacks_dict}")
   top_crates = [v[-1] for v in crate_stacks_dict.values()]
   print(f"top_crates:         {top_crates}")
   res = ''.join(top_crates)
   print(f">> SOLUTION Part 1/2: {res}\n")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_05.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data)
