import numpy as np
import random as rd

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
# set up some rotation matrices for later
        self.x_clockwise = [ [1,0,0], [0,0,1], [0,-1,0] ]
        self.x_anticlockwise = [ [1,0,0], [0,0,-1], [0,1,0] ]
        self.y_clockwise = [ [0,0,-1], [0,1,0], [1,0,0] ]
        self.y_anticlockwise = [ [0,0,1], [0,1,0], [-1,0,0] ]
        self.z_clockwise = [ [0,1,0], [-1,0,0], [0,0,1] ]
        self.z_anticlockwise = [ [0,-1,0], [1,0,0], [0,0,1] ]

        self.rotation_matrices = [self.x_clockwise,self.x_anticlockwise,self.y_clockwise,self.y_anticlockwise,self.z_clockwise,self.z_anticlockwise]

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
# redoing the printing stage "manually" like
#[["U1","U2","U3"],["U8","U0","U4"],["U7","U6","U5"]]
#[["L1","L2","L3"],["L8","L0","L4"],["L7","L6","L5"]]
#[["F1","F2","F3"],["F8","F0","F4"],["F7","F6","F5"]] i.e. each face numbers go
#[["R1","R2","R3"],["R8","R0","R4"],["R7","R6","R5"]] 1 2 3
#[["B1","B2","B3"],["B8","B0","B4"],["B7","B6","B5"]] 8 0 4
#[["D1","D2","D3"],["D8","D0","D4"],["D7","D6","D5"]] 7 6 5
        # f0 = self.cube[1,0,1][1]
        F1 = -self.cube[0,0,2][1]
        F2 = -self.cube[1,0,2][1]
        F3 = -self.cube[2,0,2][1]
        F4 = -self.cube[2,0,1][1]
        F5 = -self.cube[2,0,0][1]
        F6 = -self.cube[1,0,0][1]
        F7 = -self.cube[0,0,0][1]
        F8 = -self.cube[0,0,1][1]
        F0 = -self.cube[1,0,1][1]
        F = [F1,F2,F3,F4,F5,F6,F7,F8,F0]

        L1 = -self.cube[0,2,2][0]
        L2 = -self.cube[0,1,2][0]
        L3 = -self.cube[0,0,2][0]
        L4 = -self.cube[0,0,1][0]
        L5 = -self.cube[0,0,0][0]
        L6 = -self.cube[0,1,0][0]
        L7 = -self.cube[0,2,0][0]
        L8 = -self.cube[0,2,1][0]
        L0 = -self.cube[0,1,1][0]
        L = [L1,L2,L3,L4,L5,L6,L7,L8,L0]

        R1 = self.cube[2,0,2][0]
        R2 = self.cube[2,1,2][0]
        R3 = self.cube[2,2,2][0]
        R4 = self.cube[2,2,1][0]
        R5 = self.cube[2,2,0][0]
        R6 = self.cube[2,1,0][0]
        R7 = self.cube[2,0,0][0]
        R8 = self.cube[2,0,1][0]
        R0 = self.cube[2,1,1][0]
        R = [R1,R2,R3,R4,R5,R6,R7,R8,R0]

        B1 = self.cube[2,2,2][1]
        B2 = self.cube[1,2,2][1]
        B3 = self.cube[0,2,2][1]
        B4 = self.cube[0,2,1][1]
        B5 = self.cube[0,2,0][1]
        B6 = self.cube[1,2,0][1]
        B7 = self.cube[2,2,0][1]
        B8 = self.cube[2,2,1][1]
        B0 = self.cube[1,2,1][1]
        B = [B1,B2,B3,B4,B5,B6,B7,B8,B0]

        U1 = self.cube[0,2,2][2]
        U2 = self.cube[1,2,2][2]
        U3 = self.cube[2,2,2][2]
        U4 = self.cube[2,1,2][2]
        U5 = self.cube[2,0,2][2]
        U6 = self.cube[1,0,2][2]
        U7 = self.cube[0,0,2][2]
        U8 = self.cube[0,1,2][2]
        U0 = self.cube[1,1,2][2]
        U = [U1,U2,U3,U4,U5,U6,U7,U8,U0]

        D1 = -self.cube[0,0,0][2]
        D2 = -self.cube[1,0,0][2]
        D3 = -self.cube[2,0,0][2]
        D4 = -self.cube[2,1,0][2]
        D5 = -self.cube[2,2,0][2]
        D6 = -self.cube[1,2,0][2]
        D7 = -self.cube[0,2,0][2]
        D8 = -self.cube[0,1,0][2]
        D0 = -self.cube[1,1,0][2]
        D = [D1,D2,D3,D4,D5,D6,D7,D8,D0]

        print("       ",U1,U2,U3)
        print("       ",U8,U0,U4)
        print("       ",U7,U6,U5)
        print()
        print(L1,L2,L3," ",F1,F2,F3," ",R1,R2,R3," ",B1,B2,B3)
        print(L8,L0,L4," ",F8,F0,F4," ",R8,R0,R4," ",B8,B0,B4)
        print(L7,L6,L5," ",F7,F6,F5," ",R7,R6,R5," ",B7,B6,B5)
        print()
        print("       ",D1,D2,D3)
        print("       ",D8,D0,D4)
        print("       ",D7,D6,D5)

# Next, we need to implement rotations of the cube, where we don't
# perform any twist, just a rotation in space

    def rotate_cube(self,clockwise,axis):

        if clockwise != 0 and clockwise != 1:
            raise("first argument must be 1 or 0 (clockwise or anticlockwise rotation)")

        tmp_cube = np.array(self.cube)

        for i in range(0,3):
            for j in range(0,3):
                for k in range(0,3):

                    x = i - 1 # centre the cube at 0,0,0
                    y = j - 1 # so we can rotate about z axis
                    z = k - 1

                    if axis == "X":
                        if clockwise == 1:
                            matrix = self.rotation_matrices[0]
                        else:
                            matrix = self.rotation_matrices[1]
                    elif axis == "Y":
                        if clockwise == 1:
                            matrix = self.rotation_matrices[2]
                        else:
                            matrix = self.rotation_matrices[3]
                    elif axis == "Z":
                        if clockwise == 1:
                            matrix = self.rotation_matrices[4]
                        else:
                            matrix = self.rotation_matrices[5]
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

    def twist(self,clockwise,face):
        if clockwise != 0 and clockwise != 1:
            raise("first argument must be 1 or 0 (clockwise or anticlockwise rotation)")

        xlow   = 0 # these will be the ranges of the loops
        xhigh  = 3 # the twist works like the rotation
        ylow   = 0 # method above, except it only rotates
        yhigh  = 3 # one face as opposed to all 3
        zlow   = 0
        zhigh  = 3

        if face == "F":
            if clockwise == 1:
                ix_matrix = 3 # this is the index of the array rotation_matrices
            else:
                ix_matrix = 2
            yhigh = 1
        
        elif face == "B":
            if clockwise == 1:
                ix_matrix = 2
            else:
                ix_matrix = 3
            ylow = 2

        elif face == "L":
            if clockwise == 1:
                ix_matrix = 1
            else:
                ix_matrix = 0
            xhigh = 1

        elif face == "R":
            if clockwise == 1:
                ix_matrix = 0
            else:
                ix_matrix = 1
            xlow = 2

        elif face == "U":
            if clockwise == 1:
                ix_matrix = 4
            else:
                ix_matrix = 5
            zlow = 2

        elif face == "D":
            if clockwise == 1:
                ix_matrix = 5
            else:
                ix_matrix = 4
            zhigh = 1

        else:
            raise("invalid face")

        matrix = self.rotation_matrices[ix_matrix]
# now we rotate the cubies
        tmp_cube = np.array(self.cube)
        for i in range(xlow,xhigh):
            for j in range(ylow,yhigh):
                for k in range(zlow,zhigh):

                    x = i - 1 # centre the cube at 0,0,0
                    y = j - 1 # so we can rotate about z axis
                    z = k - 1

                    [x1,y1,z1] = np.dot(matrix,[x,y,z]) # new coordinates after rotating

                    i1 = x1 + 1 # translate back to
                    j1 = y1 + 1 # out original frame
                    k1 = z1 + 1

                    tmp = self.cube[i,j,k] # rotate the cubies, but keep their original orientation
                    
                    tmp_cube[i1,j1,k1] = np.dot(matrix,tmp) # this rotates the cubies' orientation

        self.cube = tmp_cube

    def scramble(self):
# method to scramble the cube
        rd.seed(a=1) # set random seed for reproducability 
        rand = rd.randint(30,50)
        for i in range(rand):
            face = rd.choice(["F","B","L","R","U","D"]) # choose a random face
            clockwise = rd.choice([0,1]) # choose whether it will be a clockwise or anti clockwise twist
            self.twist(clockwise,face)


# now we want to start adding in algorithms for solving the cube
# We'll solve the front face I think

# We'll need a method to locate certain pieces
# This will take 1, 2 or 3 colours, and return the location of that piece

    def locate_piece(self,c1,c2=0,c3=0):

        c1 = abs(c1)
        c2 = abs(c2)
        c3 = abs(c3)
        colours=set([c1,c2,c3])
        pieces = []
        
        xyz_grid = [(x,y,z) for x in range(3) for y in range(3) for z in range(3)]
        
        for xyz in xyz_grid:
            if colours <= set( abs( self.cube[ xyz ] ) ):
                    pieces.append(xyz)

        if len(pieces) > 1: # this will happen for centre pieces, which have 2 zeros in the colour vector
# # drop any pieces which aren't central pieces
            for i in pieces:
                tmp = i
                i = list(i)
                i.remove(1)
                if 1 in i:
                    pieces = tmp

        print(pieces)

c = Cube()
# c.scramble()
# c.print_cube()
c.locate_piece(2)
# list1=[1,0,2]
# list1.remove(1)
# list1.remove(1)
# print(list1)
# print(abs(c.cube[0,0,0]))
# # print(c.cube[:,0,:])
# # c.rotate_cube(1,"Y")
# c.twist(1,"U")
# c.rotate_cube(1,"Y")
# c.twist(0,"U")
# c.twist(1,"U")
# c.twist(0,"L")
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# c.print_cube()
