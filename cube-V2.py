import numpy as np

class Cube:
# We will represent the cube as a numpy array where we can access each
# individual cubie by cube[x,y,z]. This will return us a colour vector [cx,cy,cz]
# which tells us the colour in the x,y,z directions (numbered
# 1-6, and 0 for no colour, as in the cx colour on the upper face)
# A minus sign for colour means that it is facing in the negative i direction
# The cube is sitting with the [0,0,0] cube at the origin in the xyz positive octant

# Only issue so far is it's unclear how this corresponds to a solved/unsolved cube
# it's not clear to see. Maybe we can just have a mapping to our old way of showing this
    def __init__(self):
        self.cubie_colour = [0,0,0] # this will be the colour vector at each cubie point, start it off empty (as zeros)
        self.line = [self.cubie_colour,self.cubie_colour,self.cubie_colour]
        self.face = [self.line,self.line,self.line] 
        self.empty_cube = [self.face,self.face,self.face] # build up the cube

        self.cube = np.array(self.empty_cube) # np array is easier to navigate

# next we need to set the colour vectors
        for x in range(0,3):
            for y in range(0,3):
                for z in range(0,3):

                    if x == 0:
                        self.cube[x,y,z,0] = -1
                    elif x == 1:
                        self.cube[x,y,z,0] = 0
                    elif x == 2:
                        self.cube[x,y,z,0] = 6

                    if y == 0:
                        self.cube[x,y,z,1] = -2
                    elif y == 1:
                        self.cube[x,y,z,1] = 0
                    elif y == 2:
                        self.cube[x,y,z,1] = 5

                    if z == 0:
                        self.cube[x,y,z,2] = -3
                    elif z == 1:
                        self.cube[x,y,z,2] = 0
                    elif z == 2:
                        self.cube[x,y,z,2] = 4

# TODO - write some kind of method to print the cube in a 

# Next, we need to implement rotations of the cube, where we don't
# perform any twist, just a rotation in space

    def rotate_cube(self,clockwise,axis):

        if clockwise != 0 and clockwise != 1:
            raise("first argument must be 1 or 0 (clockwise or anticlockwise rotation)")

        tmp_cube = np.array(self.empty_cube)

        for i in range(0,3):
            for j in range(0,3):
                for k in range(0,3):

                    x = i - 1 # centre the cube at 0,0,0
                    y = j - 1 # so we can rotate about z axis
                    z = k - 1

                    x_clockwise = [ [1,0,0], [0,0,1], [0,-1,0] ]
                    x_anticlockwise = [ [1,0,0], [0,0,-1], [0,1,0] ]
                    y_clockwise = [ [0,0,-1], [0,1,0], [1,0,0] ]
                    y_anticlockwise = [ [0,0,1], [0,1,0], [-1,0,0] ]
                    z_clockwise = [ [0,1,0], [-1,0,0], [0,0,1] ]
                    z_anticlockwise = [ [0,-1,0], [1,0,0], [0,0,1] ]

                    rotation_matrices = [x_clockwise,x_anticlockwise,y_clockwise,y_anticlockwise,z_clockwise,z_anticlockwise]

                    if axis == "X":
                        if clockwise == 1:
                            matrix = rotation_matrices[0]
                        else:
                            matrix = rotation_matrices[1]
                    elif axis == "Y":
                        if clockwise == 1:
                            matrix = rotation_matrices[2]
                        else:
                            matrix = rotation_matrices[3]
                    elif axis == "Z":
                        if clockwise == 1:
                            matrix = rotation_matrices[4]
                        else:
                            matrix = rotation_matrices[5]
                    else:
                        raise("can only rotate about X,Y, or Z axes, invalid input")

                    [x1,y1,z1] = np.dot(matrix,[x,y,z]) # new coordinates after rotating

                    i1 = x1 + 1 # translate back to
                    j1 = y1 + 1 # out original frame
                    k1 = z1 + 1

                    tmp = self.cube[i,j,k] # rotate the cubies, but keep their original orientation
                    tmp_cube[i1,j1,k1] = np.dot(matrix,tmp) # now rotate their orientation

        self.cube = tmp_cube



c = Cube()
print(c.cube[2,0,0])
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
c.rotate_cube(1,"Z")
# c.rotate_z()
# print()
print(c.cube[2,0,0])
# print(c.cube[0,0])
