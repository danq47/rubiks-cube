import numpy as np
import random as rd
import copy

class Cube:
# We will represent the cube as a numpy array where we can access each
# individual cubie by cube[x,y,z]. This will return us a colour vector [cx,cy,cz]
# which tells us the colour in the x,y,z directions (numbered
# 1-6, and 0 for no colour, as in the cx colour on the upper face)
# A minus sign for colour means that it is facing in the negative i direction
# The cube is sitting with the [0,0,0] cube at the origin in the xyz positive octant
# The axes are pointing z up, x to the right, y into screen with F facing us (negative y direction)

# Only issue so far is it's unclear how this corresponds to a solved/unsolved cube
# it's not clear to see. Maybe we can just have a mapping to our old way of showing this
    def __init__(self):
        self.cubie_colour = [0,0,0] # this will be the colour vector at each cubie point, start it off empty (as zeros)
        self.line = [ self.cubie_colour[:] for _ in range(3)]
        self.face = [ self.line[:] for _ in range(3)]
        self.empty_cube = [ self.face[:] for _ in range(3)] # build up the cube

        self.cube = np.array(self.empty_cube) # this is the best way I can see of copying a very deeply nested list?? Surely there's a better way but I don't see one yet

        x_colour = { 0:-1, 1:0, 2:6 } # colours for the faces - x=0 layer (L) has colour -1 in the minus x direction, x=1 layer has no x colour, and x=2 layer (R) has colour 6 
        y_colour = { 0:-2, 1:0, 2:5 }
        z_colour = { 0:-3, 1:0, 2:4 }

# loop over x, y, and z, and set the colours of the solved cube
        for x in range(0,3):
            for y in range(0,3):
                for z in range(0,3):

                    self.cube[x,y,z] = [ x_colour[x], y_colour[y], z_colour[z] ]

# debug - checking the front is being printed properly
        # self.cube[0][0][0][1]=1
        # self.cube[1][0][0][1]=2
        # self.cube[2][0][0][1]=3
        # self.cube[2][0][1][1]=4
        # self.cube[2][0][2][1]=5
        # self.cube[1][0][2][1]=6
        # self.cube[0][0][2][1]=7
        # self.cube[0][0][1][1]=8
        # self.cube[1][0][1][1]=9
        self.original_cube=self.cube # so we can check if pieces are in the correct place
        # set up some rotation matrices for later
        self.x_clockwise = [ [1,0,0], [0,0,1], [0,-1,0] ]
        self.x_anticlockwise = [ [1,0,0], [0,0,-1], [0,1,0] ]
        self.y_clockwise = [ [0,0,-1], [0,1,0], [1,0,0] ]
        self.y_anticlockwise = [ [0,0,1], [0,1,0], [-1,0,0] ]
        self.z_clockwise = [ [0,1,0], [-1,0,0], [0,0,1] ]
        self.z_anticlockwise = [ [0,-1,0], [1,0,0], [0,0,1] ]
        self.rotation_matrices = [self.x_clockwise,self.x_anticlockwise,self.y_clockwise,self.y_anticlockwise,self.z_clockwise,self.z_anticlockwise]

    # def print_front(self):
    #         x=[ 0 for _ in range(3) ]
    #         xz=[x[:] for _ in range(3) ]
    #         for x in range(3):
    #             for z in range(3):
    #                 xz[ 2-z ][x] = abs(self.cube[x,0,z][1])




    def print_cube(self):
# redoing the printing stage "manually" like
#[["U1","U2","U3"],["U8","U0","U4"],["U7","U6","U5"]]
#[["L1","L2","L3"],["L8","L0","L4"],["L7","L6","L5"]]
#[["F1","F2","F3"],["F8","F0","F4"],["F7","F6","F5"]] i.e. each face numbers go
#[["R1","R2","R3"],["R8","R0","R4"],["R7","R6","R5"]] 1 2 3
#[["B1","B2","B3"],["B8","B0","B4"],["B7","B6","B5"]] 8 0 4
#[["D1","D2","D3"],["D8","D0","D4"],["D7","D6","D5"]] 7 6 5
        # f0 = self.cube[1,0,1][1]
        F1 = -self.cube[0][0][2][1]
        F2 = -self.cube[1][0][2][1]
        F3 = -self.cube[2][0][2][1]
        F4 = -self.cube[2][0][1][1]
        F5 = -self.cube[2][0][0][1]
        F6 = -self.cube[1][0][0][1]
        F7 = -self.cube[0][0][0][1]
        F8 = -self.cube[0][0][1][1]
        F0 = -self.cube[1][0][1][1]
        F = [F1,F2,F3,F4,F5,F6,F7,F8,F0]

        L1 = -self.cube[0][2][2][0]
        L2 = -self.cube[0][1][2][0]
        L3 = -self.cube[0][0][2][0]
        L4 = -self.cube[0][0][1][0]
        L5 = -self.cube[0][0][0][0]
        L6 = -self.cube[0][1][0][0]
        L7 = -self.cube[0][2][0][0]
        L8 = -self.cube[0][2][1][0]
        L0 = -self.cube[0][1][1][0]
        L = [L1,L2,L3,L4,L5,L6,L7,L8,L0]

        R1 = self.cube[2][0][2][0]
        R2 = self.cube[2][1][2][0]
        R3 = self.cube[2][2][2][0]
        R4 = self.cube[2][2][1][0]
        R5 = self.cube[2][2][0][0]
        R6 = self.cube[2][1][0][0]
        R7 = self.cube[2][0][0][0]
        R8 = self.cube[2][0][1][0]
        R0 = self.cube[2][1][1][0]
        R = [R1,R2,R3,R4,R5,R6,R7,R8,R0]

        B1 = self.cube[2][2][2][1]
        B2 = self.cube[1][2][2][1]
        B3 = self.cube[0][2][2][1]
        B4 = self.cube[0][2][1][1]
        B5 = self.cube[0][2][0][1]
        B6 = self.cube[1][2][0][1]
        B7 = self.cube[2][2][0][1]
        B8 = self.cube[2][2][1][1]
        B0 = self.cube[1][2][1][1]
        B = [B1,B2,B3,B4,B5,B6,B7,B8,B0]

        U1 = self.cube[0][2][2][2]
        U2 = self.cube[1][2][2][2]
        U3 = self.cube[2][2][2][2]
        U4 = self.cube[2][1][2][2]
        U5 = self.cube[2][0][2][2]
        U6 = self.cube[1][0][2][2]
        U7 = self.cube[0][0][2][2]
        U8 = self.cube[0][1][2][2]
        U0 = self.cube[1][1][2][2]
        U = [U1,U2,U3,U4,U5,U6,U7,U8,U0]

        D1 = -self.cube[0][0][0][2]
        D2 = -self.cube[1][0][0][2]
        D3 = -self.cube[2][0][0][2]
        D4 = -self.cube[2][1][0][2]
        D5 = -self.cube[2][2][0][2]
        D6 = -self.cube[1][2][0][2]
        D7 = -self.cube[0][2][0][2]
        D8 = -self.cube[0][1][0][2]
        D0 = -self.cube[1][1][0][2]
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


    def twist(self,face,layers=1): # twist around a given face, for how many layers

        layers_to_add=layers-1 # will manually enter the ranges on the loops, and will just add (or subtract) this in
        face_to_matrix_and_ranges = { "F":[3,0,3,0,1+layers_to_add,0,3] ,\
        "B":[2,0,3,2-layers_to_add,3,0,3], "L":[1,0,1+layers_to_add,0,3,0,3], "R":[0,2-layers_to_add,3,0,3,0,3],\
        "U":[4,0,3,0,3,2-layers_to_add,3], "D":[5,0,3,0,3,0,1+layers_to_add] } # this array is [matrix_index, xlow, xhigh, ylow, yhigh, zlow, zhigh]

        [matrix_index, xlow, xhigh, ylow, yhigh, zlow, zhigh] = face_to_matrix_and_ranges[face]

# now rotate the cubies
        tmp_cube = np.array(self.cube) # save 
        for i in range(xlow,xhigh):
            for j in range(ylow,yhigh):
                for k in range(zlow,zhigh): # loop over all cubies

                    [ x, y, z ] = [ i-1, j-1, k-1 ] # centre the cube on (0,0,0)
                    [ x1, y1, z1 ] = np.dot(self.rotation_matrices[matrix_index],[x,y,z]) # new coordinates after rotating
                    [ i1, j1, k1 ] = [ x1+1, y1+1, z1+1 ] # translate back to our original coordinate system

                    tmp=self.cube[i,j,k] # rotate the cubies, but keep their original orientation
                    tmp_cube[i1,j1,k1] = np.dot(self.rotation_matrices[matrix_index],tmp) # this rotates the cubies' orientation

        self.cube = tmp_cube

    def scramble(self):
# method to scramble the cube
        rd.seed(a=3) # set random seed for reproducability 
        rand = rd.randint(20,40)
        for i in range(rand):
            face = rd.choice(["F","B","L","R","U","D"]) # choose a random face
            n_turns = rd.choice([1,2,3]) # choose number of turns clockwise
            for _ in range(n_turns):
                self.twist(face,1)


# now we want to start adding in algorithms for solving the cube
# We'll solve the front face I think

# We'll need a method to locate certain pieces
# This will take 1, 2 or 3 colours, and return the location of that piece

    def locate_piece(self,original,c1,c2=0,c3=0):
# if original = 1, then we are looking for the position in the original (solved state)
# otherwise we're looking on our current cube

        c1 = abs(c1)
        c2 = abs(c2)
        c3 = abs(c3)
        colours=set([c1,c2,c3])
        pieces = []
        
        xyz_grid = [(x,y,z) for x in range(3) for y in range(3) for z in range(3)]
        
        if original == 1:
            for xyz in xyz_grid:
                if colours <= set( abs( self.original_cube[ xyz ] ) ):
                        pieces.append(xyz)

        else:
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

        return pieces[0]



# # if we consider F the front, then we want to put pieces in the back (for making the cross)
#     def to_back(self,cubie):
#         x=cubie[0]
#         y=cubie[1]
#         z=cubie[2]
        
# # First check if it is in the back face

#         if y == 2: # it's in the back face already
#             pass
    

#         elif y == 0: # it's in the front face, need to figure out which face to turn
            
#             if x == 0 and z == 1:
#                 face = "L"
#             elif x == 1 and z == 0:
#                 face = "D"
#             elif x == 2 and z == 1:
#                 face = "R"
#             elif x == 1 and z == 2:
#                 face = "U"

#             for _ in range(2):
#                 self.twist(face) # rotate clockwise twice around whichever face we've chosen
                

#         elif y == 1: # it's in the middle layer, and we once again need to twist a face

#             if x == 0 and z == 0:
#                 face = "L"
#             elif x == 2 and z == 0:
#                 face = "D"
#             elif x == 2 and z == 2:
#                 face = "R"
#             elif x == 0 and z == 2:
#                 face = "U"

#             self.twist(face)

#         self.solution.append(".")
            



    def make_cross(self):
        u_col = abs(self.cube[1,1,2][2])
        d_col = abs(self.cube[1,1,0][2])
        f_col = abs(self.cube[1,0,1][1])
        b_col = abs(self.cube[1,2,1][1])
        l_col = abs(self.cube[0,1,1][0])
        r_col = abs(self.cube[2,1,1][0])
# try find FL piece first. should be at (0,0,1). First we'll put it into the bottom (y=2) face
# 3 steps - (1) find the piece, (2) put it in the bottom, (3) rotate so that it is in the right face,
# (4) rotate the face (i.e. here L) until the piece is in the correct position, (5) if it's not already
# (5) in the right orientation, flip it

# 1. Find the pieces

        piece_colours = [ r_col, d_col, l_col, u_col ]
        faces = { r_col:"R", d_col:"D", l_col:"L", u_col:"U" }

        original_position = self.locate_piece(1,f_col,r_col)
        current_position  = self.locate_piece(0,f_col,r_col)

#         if current_position == original_position : # it's already in the right place
#             pass

#         else: # 3 scenarios. It can be either in F face but in the wrong spot, it can be in the middle layer, or it can be in the back layer

# # it is in the front layer
#             if current_position[1] == 0 : # piece is in the front layer, just the wrong position

# #         for piece in piece_colours:


#             original_position = self.locate_piece(1,f_col,piece)
#             current_position  = self.locate_piece(0,f_col,piece)

#             if current_position == original_position:
#                 pass

#             else:

# # 2.a if piece is in F layer, put in back, otherwise 
#                 if current_position[1] == 1:
#                     self.to_back(current_position)
#                     current_position  = self.locate_piece(0,f_col,piece)
# # 2.b else if it's in the middle (i.e. between F and B) layer 

# # 3. Rotate B so that it's on the right face

#                 print(faces[piece])
#                 print("current position:",current_position)
#                 print("original position:",original_position)
                
#                 cxz=[current_position[0],current_position[2]] # current position x and z coordinates
#                 oxz=[original_position[0],original_position[2]] # original position x and z coordinates

#                 while cxz != oxz:
#                     self.twist("B")
#                     current_position  = self.locate_piece(0,f_col,piece)
#                     cxz=[current_position[0],current_position[2]]
#                     print("current position:",current_position)

# # 4. Rotate it back into F

#                 for _ in range(2):
#                     self.twist(faces[piece])
#                     self.solution.append("'")

c = Cube()

# c.scramble()

# c.twist("L")
# c.twist("F")
# c.twist("R")
# c.twist("B")
# I've done this with U=green, L=white, F=orange
c.twist2("L",1)
c.twist2("F",3)
c.print_cube()
# c.print_front()
print("~~~~~~~~~~~~~~~~~~~~~~")
# c.twist("B")
# c.make_cross()
# c.print_cube()
# print(c.solution)




