# I want to write some code that will be able to solve a
# rubik's cube, and eventually make a gui where we can scramble
# and solve. Would also like to be able to implement different
# algorithms. The stages we will need are
# 1. Figure out a set of notation so we can save/load a cube
# 2. Implement the moves, so we can scramble a solved one
# 3. Solve a scrambled one manually
# 4. Implement an algorith to solve it automatically

# I think the biggest issue will be figuring out how
# to represent the cube

# Maybe as a tuple (cx, cy, cz) which has contains
# the colours in the x y z direction i.e.
# a red centre facing in the x direction would be (R,0,0)
# whereas a red,blue white corner would be (R,B,W)