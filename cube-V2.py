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

    def print_cube(self):
# want something that can output the cube to screen
# will define how we unfold the cube. As we look at it (down from positive x)
# the face facing us (X=2) is F
# F:X=2, L:Y=0, R:Y=2, B:X=0, U:Z=2, D:Z=0
# multiply the negative faces by -1 to only print out positive numbers
        self.front = self.cube[2,:,:][:,:,0][::-1] # the first indexer gets us the X=2 plane, and the second indexer gets us all the cx from that
        self.back = self.cube[0,:,:][:,:,0][::-1]*-1 # same, but for X=0 plane
        self.left = self.cube[:,0,:][:,:,1][::-1]*-1 # all cy in Y=0 plane
        self.right = self.cube[:,2,:][:,:,1][::-1] # smae for Y=2
        self.upper = self.cube[:,:,2][:,:,2][::-1] # cz for Z=2
        self.down = self.cube[:,:,0][:,:,2][::-1]*-1 # cz for Z=0
        print("         ",self.upper[0])
        print("         ",self.upper[1])
        print("         ",self.upper[2])
        print("")
        print(self.left[0]," ",self.front[0]," ",self.right[0]," ",self.back[0])
        print(self.left[1]," ",self.front[1]," ",self.right[1]," ",self.back[1])
        print(self.left[2]," ",self.front[2]," ",self.right[2]," ",self.back[2])
        print("")
        print("         ",self.down[0])
        print("         ",self.down[1])
        print("         ",self.down[2])

    def print_cube2(self):
# redoing the printing stage "manually" like
#[["U1","U2","U3"],["U8","U0","U4"],["U7","U6","U5"]]
#[["L1","L2","L3"],["L8","L0","L4"],["L7","L6","L5"]]
#[["F1","F2","F3"],["F8","F0","F4"],["F7","F6","F5"]] i.e. each face numbers go
#[["R1","R2","R3"],["R8","R0","R4"],["R7","R6","R5"]] 1 2 3
#[["B1","B2","B3"],["B8","B0","B4"],["B7","B6","B5"]] 8 0 4
#[["D1","D2","D3"],["D8","D0","D4"],["D7","D6","D5"]] 7 6 5
        # f0 = self.cube[1,0,1][1]
        f1 = -self.cube[0,0,2][1]
        f2 = -self.cube[1,0,2][1]
        f3 = -self.cube[2,0,2][1]
        f4 = -self.cube[2,0,1][1]
        f5 = -self.cube[2,0,0][1]
        f6 = -self.cube[1,0,0][1]
        f7 = -self.cube[0,0,0][1]
        f8 = -self.cube[0,0,1][1]
        f0 = -self.cube[1,0,1][1]

        L1 = -self.cube[0,2,2][0]
        L2 = -self.cube[0,1,2][0]
        L3 = -self.cube[0,0,2][0]
        L4 = -self.cube[0,0,1][0]
        L5 = -self.cube[0,0,0][0]
        L6 = -self.cube[0,1,0][0]
        L7 = -self.cube[0,2,0][0]
        L8 = -self.cube[0,2,1][0]
        L0 = -self.cube[0,1,1][0]

        R1 = self.cube[2,0,2][0]
        R2 = self.cube[2,1,2][0]
        R3 = self.cube[2,2,2][0]
        R4 = self.cube[2,2,1][0]
        R5 = self.cube[2,2,0][0]
        R6 = self.cube[2,1,0][0]
        R7 = self.cube[2,0,0][0]
        R8 = self.cube[2,0,1][0]
        R0 = self.cube[2,1,1][0]

        B1 = self.cube[2,2,2][1]
        B2 = self.cube[1,2,2][1]
        B3 = self.cube[0,2,2][1]
        B4 = self.cube[0,2,1][1]
        B5 = self.cube[0,2,0][1]
        B6 = self.cube[1,2,0][1]
        B7 = self.cube[2,2,0][1]
        B8 = self.cube[2,2,1][1]
        B0 = self.cube[1,2,1][1]

        U1 = self.cube[0,2,2][2]
        U2 = self.cube[1,2,2][2]
        U3 = self.cube[2,2,2][2]
        U4 = self.cube[2,1,2][2]
        U5 = self.cube[2,0,2][2]
        U6 = self.cube[1,0,2][2]
        U7 = self.cube[0,0,2][2]
        U8 = self.cube[0,1,2][2]
        U0 = self.cube[1,1,2][2]

        D1 = -self.cube[0,0,0][2]
        D2 = -self.cube[1,0,0][2]
        D3 = -self.cube[2,0,0][2]
        D4 = -self.cube[2,1,0][2]
        D5 = -self.cube[2,2,0][2]
        D6 = -self.cube[1,2,0][2]
        D7 = -self.cube[0,2,0][2]
        D8 = -self.cube[0,1,0][2]
        D0 = -self.cube[1,1,0][2]

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

# Next, we'll start to implement twists
    def twist_F(self):
# first move the cubies
        # print(self.cube[2,:,:])
        tmp_cube = np.array(self.empty_cube)
        
        tmp = np.array([list(self.cube[2,:,:][0,:,:][x]) for x in range(0,3)]) # (0,0,0-2)
        self.cube[2,:,:][0,:,:] = self.cube[2,:,:][:,0,:][::-1]
        self.cube[2,:,:][:,0,:] = self.cube[2,:,:][2,:,:]
        self.cube[2,:,:][2,:,:] = self.cube[2,:,:][:,2,:][::-1]
        self.cube[2,:,:][:,2,:] = tmp

# now reorient the cubies
        # tmp2 = self.cube
        # tmp2 = np.array([list(self.cube[2,:,:][x]) for x in range(0,3)])
        # print(tmp2)
        # self.cube[2,:,:][:,:,1] = tmp2[:,:,2]
        # self.cube[2,:,:][:,:,2] = -tmp2[:,:,1]
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(self.cube[2,:,:])

        # print(self.cube)

c = Cube()
print(c.cube[0,0,0][2])
print(c.cube[1,0,0][2])
print(c.cube[2,0,0][2])
print(c.cube[2,1,0][2])
print(c.cube[2,2,0][2])
print(c.cube[1,2,0][2])
print(c.cube[0,2,0][2])
print(c.cube[0,1,0][2])
print(c.cube[1,1,0][2])

# # c.print_cube2()
# c.print_cube()
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# # # c.rotate_cube(1,"Z")
# # c.twist_F()
# c.twist_F()

# print(c.cube)
# # print(c.cube[2,:,:])

# c.print_cube()
# print(c.cube[2,:,:])
# print(c.cube[2,:,:][2,:,:][::-1])
# c.print_cube()
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# c.print_cube()
