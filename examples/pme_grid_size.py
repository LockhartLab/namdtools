"""
Pick a PME grid size for a NAMD simulation.

get_pme_size takes a box length and finds the smallest grid size that is at
least as large, with only small prime factors (2, 3, and 5), which is what
NAMD's PME implementation requires for an efficient FFT.
"""

from namdtools import get_pme_size

box_length = 68.0
grid_size = get_pme_size(box_length)

print(f"box length: {box_length}")
print(f"PME grid size: {grid_size}")
