#!/usr/bin/env python3

import numpy as np
from tqdm import tqdm
"""
- each sensor (S) detects exactly 1 beacon (B) closest to it (by Manhatten distance)
- no tie can occur where 2 beacons have the same distance to a sensor
=> so we know that within the Manhatten distance d(S,B) of a pair S,B
   there is only this one beacon B (but there might be other sensors)

TODO:
- generate all (valid,i.e. within bounds) positions with a certain Manhatten distance
  from any 2D-pos (use symmetry => only compute for 1 of 4 quadrants)
   e.g.: d_Manh=4

      #
      ##
      ###
      ####
      S####
- 

- Part 1 brute-force: works for easy sample data...
   y = 10 # 10 2000000
   count = 0
   for x in tqdm(range(x_min,x_max+1)):
      pos = np.array((x,y))
      for (s,b),d in zip(sensor_readings,Manhatten_distances):
         if np.all(pos == b):
            break
         if d_Manh(pos,s) <= d:
            count += 1
            break
   print(f"count: {count}")
"""
sample_input = [
"Sensor at x=2, y=18: closest beacon is at x=-2, y=15\n",
"Sensor at x=9, y=16: closest beacon is at x=10, y=16\n",
"Sensor at x=13, y=2: closest beacon is at x=15, y=3\n",
"Sensor at x=12, y=14: closest beacon is at x=10, y=16\n",
"Sensor at x=10, y=20: closest beacon is at x=10, y=16\n",
"Sensor at x=14, y=17: closest beacon is at x=10, y=16\n",
"Sensor at x=8, y=7: closest beacon is at x=2, y=10\n",
"Sensor at x=2, y=0: closest beacon is at x=2, y=10\n",
"Sensor at x=0, y=11: closest beacon is at x=2, y=10\n",
"Sensor at x=20, y=14: closest beacon is at x=25, y=17\n",
"Sensor at x=17, y=20: closest beacon is at x=21, y=22\n",
"Sensor at x=16, y=7: closest beacon is at x=15, y=3\n",
"Sensor at x=14, y=3: closest beacon is at x=15, y=3\n",
"Sensor at x=20, y=1: closest beacon is at x=15, y=3\n"
]

def show(arr,x_min,x_max,y_max):
   #show = lambda arr: [print("  ~"+l.tobytes().decode('UTF-8')+"~") for l in arr]
   l_pad,r_pad = " ", ""
   header = list(' '*arr[0].size)
   header_idx = header.copy()
   fw = len(str(y_max))
   
   for i in range(x_min,x_max+1):
      if i%5==0:
         header[i-x_min] = 'v'

   """header_idx[ 0-x_min] = '0'
   header_idx[ 5-x_min] = '5'
   header_idx[10-x_min-1:10-x_min-1+2] = '10'
   header_idx[15-x_min-1:15-x_min-1+2] = '15'"""
   for i in range(x_max+1):
      i_str = str(i)
      if   i%5==0 and len(i_str)==1:
         header_idx[i-x_min] = i_str
      elif i%5==0 and len(i_str)==2:
         header_idx[i-x_min-1:i-x_min-1+2] = i_str
   
   print()
   print(f"{' ':{fw}}" + ' '*len(l_pad) + ''.join(header_idx) + ' '*len(r_pad))
   print(f"{' ':{fw}}" + ' '*len(l_pad) + ''.join(header) + ' '*len(r_pad))
   [print(f"{i:{fw}}" + l_pad + l.tobytes().decode('UTF-8') + r_pad) for i,l in enumerate(arr)]

def show_sensor_readings(sensor_readings,x_min,x_max,y_min,y_max):
   Nx = x_max-x_min+1
   Ny = y_max-y_min+1
   if not (Ny<5000 and Nx<5000):
      print("!! matrix would be too large, not displaying this !!")
      return
   screen = np.chararray((Ny,Nx))
   screen[:] = '.'
   for s,b in sensor_readings:
      screen[s[1],s[0]-x_min] = 'S'
      screen[b[1],b[0]-x_min] = 'B'
   show(screen,x_min,x_max,y_max); print()

def show_Manhatten_distance(sensor_readings,x_min,x_max,y_min,y_max,c,d):
   """ marks all fields with d_Manh <= d from c with '#' """
   Nx = x_max-x_min+1
   Ny = y_max-y_min+1
   if not (Ny<5000 and Nx<5000):
      print("!! matrix would be too large, not displaying this !!")
      return
   screen = np.chararray((Ny,Nx))
   screen[:] = '.'
   for s,b in sensor_readings:
      screen[s[1],s[0]-x_min] = 'S'
      screen[b[1],b[0]-x_min] = 'B'

   # TODO: all quadrants of rhombus
   screen[c[1],c[0]-x_min] = '+'
   for y in range(d+1):
      if not(y_min <= y <= y_max):
         break
      for x in range(d+1-y):
         if x_min <= x <= x_max:
            screen[c[1]+y,c[0]-x_min+x] = '#'
   show(screen,x_min,x_max,y_max); print()

def d_Manh(a,b):
   """ a,b: np.array """
   return np.sum(np.abs(a-b))

def get_limits(sensor_coords,beacon_coords):
   x_min,x_max = [f(f(sensor_coords['x']),f(beacon_coords['x'])) for f in [min,max]]
   y_min,y_max = [f(f(sensor_coords['y']),f(beacon_coords['y'])) for f in [min,max]]
   return x_min,x_max,y_min,y_max

def print_sensor_readings(sensor_readings,Manhatten_distances):
   for (s,b),d in zip(sensor_readings,Manhatten_distances):
      print(f"sensor,beacon,d_Manh: {s}, {b}, {d}")

def merge_ranges(ranges_list):
   """
   ranges_list: [[b1,e1],[b2,e2],...] –– list of ranges
   
   if merged is empty (at very beginning) or if (highest e in merged) < (r.b):
      add range to list
   else:
      (highest e in merged) = max( (highest e in merged), r.e )

   CAREFUL: this is modifying input in-place!!!
   """
   ranges_list.sort(key=lambda x: x[0])
   merged = [ranges_list.pop(0)]
   ##merged = []
   ##merged.append(ranges_list.pop(0))
   for r in ranges_list:
      if merged[-1][1] < r[0]-1: # if largest_e < b'-1
         merged.append(r)
      else:
         merged[-1][1] = max(merged[-1][1],r[1])
   return merged

def parse_data(data):
   sensor_readings = []
   sensor_coords = {'x':[],'y':[]} # for easy computation of limits/extends
   beacon_coords = {'x':[],'y':[]} # for easy computation of limits/extends
   Manhatten_distances = []
   for l in data:
      # sensor, beacon
      s,b = l.split(":")
      # sensor
      xy = s.split()
      sx,sy = map(int, [xy[2].split('=')[1][:-1],xy[3].split('=')[1]])
      sensor_coords['x'].append(sx)
      sensor_coords['y'].append(sy)
      # beacon
      xy = b.split()
      bx,by = map(int, [xy[4].split('=')[1][:-1],xy[5].split('=')[1]])
      beacon_coords['x'].append(bx)
      beacon_coords['y'].append(by)
      # ((sx,sy),(bx,by))
      sensor_readings.append( ((sx,sy),(bx,by)) )
      # d_Manh(s,b) = sum(abs(s-b))
      Manhatten_distances.append( d_Manh(np.array((sx,sy)),np.array((bx,by)))  )
   return sensor_readings, sensor_coords, beacon_coords, Manhatten_distances

"""
Part 1:

count all positions (in row y=10) where a beacon cannot be, i.e.
- if pos in row is covered by sensor (d_Manh(S,pos) <= d_Manh(S,B))
- is pos is covered already by a S or a B

y=10 => 26
y=2000000 => ?

algo:
   Based on pos of sensor and difference to row y,
   I can find range [b,e] in row y that is covered by this sensor.
   Then, for each new sensor, check if its range extends the current range in row y and update.

   Given (S,B,d), with S=(sx,sy),
   covered range in row y is (deduct S's and B's in row later in one pass):
      y_diff := |y-sy|
      if y_diff<=d:
         1 + (d-y_diff)*2, centered @sx,
         i.e.: [b,e] = [(sx-(d-y_diff),sy),(sx+(d-y_diff),sy)]
      else:
         row not covered by S
"""
def find_positions_in_row(sensor_readings,Manhatten_distances,y):
   # 1) collect all ranges
   ranges = []
   N_slots_occupied = {'sensor':set(),'beacon':set()} # set, as same beacon might occur for multiple sensors
   for (s,b),d in zip(sensor_readings,Manhatten_distances):
      # check if S or B is in this row
      if s[1]==y: N_slots_occupied['sensor'].add(s)
      if b[1]==y: N_slots_occupied['beacon'].add(b)
      # range algo
      row_diff = abs(y-s[1])
      if row_diff <= d:
         dd = d-row_diff
         b,e = s[0]-dd, s[0]+dd  # [(s[0]-dd,s[1]),(s[0]+dd,s[1])]
         ranges.append([b,e])
         """
         # this only works if ranges have no 'holes'
         if not covered_x:
            covered_x = [b,e]
         else:
            if b < covered_x[0]: covered_x[0] = b
            if e > covered_x[1]: covered_x[1] = e
         """

   # 2) merge/combine all collected all ranges
   # TODO: combine ranges (see ThinkCell task)
   merged_ranges = merge_ranges(ranges.copy())
   sorted_ranges = sorted(ranges,key=lambda x: x[0])
   if 0:
      print(f"       ranges: {ranges}")
      print(f"sorted ranges: {sorted_ranges}")
      print(f"merged ranges: {merged_ranges}")
   
   # 3) still have to check for possible S/B in this row and deduct them
   N_s, N_b = len(N_slots_occupied['sensor']), len(N_slots_occupied['beacon'])
   if 0:
      print(f"N_sensors,N_beacons in row {y}: {N_s},{N_b}")
   
   covered_x_fields = [e-b+1 for b,e in merged_ranges]
   N_covered = sum(covered_x_fields) -(N_s+N_b)
   
   return merged_ranges, N_covered

def solve(data,y,y_lim_part2):
   print(f"solving for y={y}, y_lim_part2={y_lim_part2}")
   data = [l.strip() for l in data]
   print(f"data: {data}")
   
   sensor_readings, sensor_coords, beacon_coords, Manhatten_distances = parse_data(data)

   print_sensor_readings(sensor_readings,Manhatten_distances)
   x_min,x_max,y_min,y_max = get_limits(sensor_coords,beacon_coords)
   Nx = x_max-x_min+1
   Ny = y_max-y_min+1
   print(f"(x_min,x_max) (y_min,y_max): {x_min,x_max} {y_min,y_max} –– Ny,Nx: {Ny,Nx}")
   show_sensor_readings(sensor_readings,x_min,x_max,y_min,y_max)
   #show_Manhatten_distance(sensor_readings,x_min,x_max,y_min,y_max,c=(8,7),d=9)

   print("––– Part 1 –––")
   merged_ranges, N = find_positions_in_row(sensor_readings,Manhatten_distances,y)
   print(f">> Solution Part 1 (covered x ranges): {merged_ranges}, count: {N}\n")

   print("––– Part 2 –––")
   """
   ? only consider S and B within (:20,:20) ?
   => need to deal with `holes` in row => check when updating range

   TODO: current solution is brute force, y-by-y. Better solution going S-by-S ?
   """
   tuning_freq = lambda x,y: x*4000000+y
   candidates = []
   for y in tqdm(range(0,y_lim_part2+1)):
      merged_ranges, N = find_positions_in_row(sensor_readings,Manhatten_distances,y)

      ##free_fields_x = []
      ##for i in range(len(merged_ranges)-1):
      ##   r1 = merged_ranges[i]
      ##   r2 = merged_ranges[i+1]
      ##   free_fields_x.extend(list(range(r1[1]+1,r2[0])))
      ##if free_fields_x:
      ##   candidates.append((y,free_fields_x))

      # assuming only a single pos will be free, this breaks early @80%
      if len(merged_ranges)>1:
         r1 = merged_ranges[0]
         r2 = merged_ranges[1]
         candidates.append((y,list(range(r1[1]+1,r2[0]))))
         break

   assert len(candidates) == 1, "found more than 1 possible pos ?!?"
   print(f"candidates: {candidates}")
   x,y = candidates[0][1][0], candidates[0][0]
   print(f">> Solution Part 2 (x,y,tuning_freq): {x},{y},{tuning_freq(x,y)}\n")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input,y=10,y_lim_part2=20) # 26
   solve(sample_input,y=11,y_lim_part2=20) # 27 (see drawing on website)
   exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_15.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data,y=2000000,y_lim_part2=4000000)
