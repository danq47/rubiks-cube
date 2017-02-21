import numpy as np
import random as rd

# TODO
####### 1. modify the input of twist so we can give it a long string like LLFU'D which it would know to do left,left,front,up(anticlockwise),down
# 2. probably change it so we put all the pieces in place first, then we can go about rotating all cubies into their right positions

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

        self.original_cube=self.cube # so we can check if pieces are in the correct place
        # set up some rotation matrices for later
        self.x_clockwise = [ [1,0,0], [0,0,1], [0,-1,0] ]
        self.x_anticlockwise = [ [1,0,0], [0,0,-1], [0,1,0] ]
        self.y_clockwise = [ [0,0,-1], [0,1,0], [1,0,0] ]
        self.y_anticlockwise = [ [0,0,1], [0,1,0], [-1,0,0] ]
        self.z_clockwise = [ [0,1,0], [-1,0,0], [0,0,1] ]
        self.z_anticlockwise = [ [0,-1,0], [1,0,0], [0,0,1] ]
        self.rotation_matrices = [self.x_clockwise,self.x_anticlockwise,self.y_clockwise,self.y_anticlockwise,self.z_clockwise,self.z_anticlockwise]

        self.solution=[]

    def print_cube(self):
        x=[ 0 for _ in range(3) ]
        face_print=[x[:] for _ in range(3) ]
        all_faces=np.array([face_print[:] for _ in range(6) ])

        self.twist("D",3,1,1) # rotate so L is the first one in the list
        for face in range(4): # going to store the face, and then rotate. will do this 4 times to get back to the beginning
            for x in range(3):
                for z in range(3): # z is the coordinate facing up 
                    all_faces[face][ 2-z ][x] = abs(self.cube[x,0,z][1])
            self.twist("U",3,1,1) # rotate whole cube clockwise
        self.twist("U",3,1,1) # rotate back so F is facing the front again
# ok now we have FLBR, need U and D
        self.twist("L",3,1,1) # gets us U
        for face in range(4,6):
            for x in range(3):
                for z in range(3):
                    all_faces[face][ 2-z ][x] = abs(self.cube[x,0,z][1])
            self.twist("L",3,1,1)
            self.twist("L",3,1,1) # gets us D, and then finishes back on U
        self.twist("R",3,1,1) # back to original orientation

        for _ in range(3):
            print("       ",all_faces[4][_])
        for _ in range(3):
            print(all_faces[0][_],all_faces[1][_],all_faces[2][_],all_faces[3][_])
        for _ in range(3):
            print("       ",all_faces[5][_])

    def move(self,move_string): # this is where we can input algorithms etc and do a sequence of twists
# a big letter means a clockwise twist and a small letter means clockwise twist of face and middle slice (i.e. layers=2)
        move_dict={ "F":["F",1], "U":["U",1], "L":["L",1], "R":["R",1], "D":["D",1], "B":["B",1],\
        "f":["F",2], "u":["U",2], "l":["L",2], "r":["R",2], "d":["D",2], "b":["B",2]}

        for ixx in range(len(move_string) - 1):
            if move_string[ixx] != "'" : # these are two modifiers, the dash means anticlockwise rotation and the 2 means 2 layers
                if move_string[ixx+1] == "'" :
                    clockwise = 0
                else:
                    clockwise = 1
                [ face , layers ] = move_dict[ move_string[ixx] ]
                self.twist(face, layers, clockwise)
        if move_string[-1] != "'" :
            [ face , layers ] = move_dict[ move_string[-1] ]
            self.twist(face, layers)

    def twist(self,face,layers=1,clockwise=1,scramble=0): # twist around a given face, for how many layers. scramble is set to 0 usually, except if the computer is scrambling it then it's 1. otherise (scramble=0) we save the moves into self.solution

        if scramble == 0 and clockwise == 1 :
            if layers > 1:
                self.solution.append(face+str(layers))
            else:
                self.solution.append(face)
        elif scramble ==0 and clockwise == 0 :
            if layers > 1:
                self.solution.append(face+str(layers)+"'")
            else:
                self.solution.append(face+"'")


        layers_to_add=layers-1 # will manually enter the ranges on the loops, and will just add (or subtract) this in
        face_to_matrix_and_ranges = { "F":[3,0,3,0,1+layers_to_add,0,3] ,\
        "B":[2,0,3,2-layers_to_add,3,0,3], "L":[1,0,1+layers_to_add,0,3,0,3], "R":[0,2-layers_to_add,3,0,3,0,3],\
        "U":[4,0,3,0,3,2-layers_to_add,3], "D":[5,0,3,0,3,0,1+layers_to_add] } # this array is [matrix_index, xlow, xhigh, ylow, yhigh, zlow, zhigh]

        [matrix_index, xlow, xhigh, ylow, yhigh, zlow, zhigh] = face_to_matrix_and_ranges[face]
        if clockwise != 1 :
            anticlockwise_matrices = { 0:1, 1:0, 2:3, 3:2, 4:5, 5:4 }
            matrix_index=anticlockwise_matrices[matrix_index]
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
        rd.seed(a=0) # set random seed for reproducability 
        rand = rd.randint(20,40)
        for i in range(rand):
            face = rd.choice(["F","B","L","R","U","D"]) # choose a random face
            n_turns = rd.choice([1,2,3]) # choose number of turns clockwise
            for _ in range(n_turns):
                self.twist(face,1,1,1)


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

    def side_to_back(self, position): # function to put a side piece to the back

        [x,y,z] = position
        if position[1] == 2 :
            pass # it's already in the back

        elif position[1] == 0 : # it's in the front but the wrong position
            face_to_turn = { (1,0):"D", (2,1):"R", (1,2):"U", (0,1):"L" } # choose which face to turn based on [x,z]
            for _ in range(2):
                self.twist(face_to_turn[(x,z)],1) # twist twice
        
        else: # it's in the middle layer. This is the first algorithm we've got to put in because we can't mess up the front layer
            face_to_turn = { (2,0):"D", (2,2):"R", (0,2):"U", (0,0):"L"}
            self.twist(face_to_turn[(x,z)],1)
            self.twist("B",1)
            for _ in range(3):
                self.twist(face_to_turn[(x,z)],1)

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

        for piece in piece_colours:

            original_position = self.locate_piece(1,f_col,piece)
            current_position  = self.locate_piece(0,f_col,piece)

            if current_position == original_position : # piece is already in the right place
                pass

            else:

                if current_position[1] < 2 : # it's not yet in the back
                    self.side_to_back(current_position)
                    current_position  = self.locate_piece(0,f_col,piece)

# now it's definitely in the back
                cxz = [ current_position[0], current_position[2] ] # current xz
                oxz = [ original_position[0], original_position[2] ] # original xz


                while cxz != oxz : # while not in the right face
                    self.twist("B",1) # rotate
                    current_position  = self.locate_piece(0,f_col,piece)
                    cxz=[current_position[0],current_position[2]]

# Rotate it back into F

                for _ in range(2):
                    self.twist(faces[piece],1)


# edge flip 2 pieces in the front 
    def edge_flip(self):
        moves_to_undo=[]
        f_col = abs(self.cube[1,0,1][1])
        edge_flip_algo="RbB'RbB'RbB'RbB'"
        # self.move(edge_flip_algo)

        finished=False
        while not finished:
            while abs(self.cube[2,0,1][1]) == f_col :
                self.move("F'")
                moves_to_undo.append("F")
            self.move(edge_flip_algo)

            if abs(self.cube[2,0,1][1]) == f_col and abs(self.cube[1,0,2][1]) == f_col\
            and abs(self.cube[0,0,1][1]) == f_col and abs(self.cube[1,0,0][1]) == f_col :
                finished=True
        self.move(moves_to_undo)


    def corner_to_back(self,position): # function to put a corner piece to the back face

        [x,y,z] = position
        if position[1] == 2 :
            pass # it's already in the back

        elif position[1] == 1 : # it's in the middle slice?? this should never happem
            pass

        elif position[1] == 0 : # it's in the front
            face_to_turn = { (2,0):"D", (2,2):"R", (0,2):"U", (0,0):"L" } # choose which face to turn based on [x,z]
            self.twist(face_to_turn[(x,z)],1) # twist to bottom
            self.twist("B",1) # twist away
            self.twist(face_to_turn[(x,z)],1,0) # return the side piece by rotating the original face back anticlockwise

    def solve_top_corners(self):

        u_col = abs(self.cube[1,1,2][2])
        d_col = abs(self.cube[1,1,0][2])
        f_col = abs(self.cube[1,0,1][1])
        b_col = abs(self.cube[1,2,1][1])
        l_col = abs(self.cube[0,1,1][0])
        r_col = abs(self.cube[2,1,1][0])

# 1. Find the pieces

        piece_colours = [ [r_col,d_col], [d_col,l_col], [l_col,u_col], [u_col,r_col] ]
        faces = { r_col:"R", d_col:"D", l_col:"L", u_col:"U" }

        for piece in piece_colours:

            original_position = self.locate_piece(1,f_col,piece[0],piece[1])
            current_position  = self.locate_piece(0,f_col,piece[0],piece[1])

            if current_position == original_position : # piece is already in the right place
                pass

            else:
                if current_position[1] == 0 : # it's in the front but in the wrong spot, put to back
                    self.corner_to_back(current_position)
                    current_position = self.locate_piece(0,f_col,piece[0],piece[1])

# now it's definitely in the back
                cxz = [ current_position[0], current_position[2] ] # current xz
                oxz = [ original_position[0], original_position[2] ] # original xz
                while cxz != oxz : # while not in the right face
                    self.twist("B",1) # rotate
                    current_position = self.locate_piece(0,f_col,piece[0],piece[1])
                    cxz=[current_position[0],current_position[2]]

# now it's in the right position, it just needs to be moved into the front face. we'll make a mini algo to do this
                face_to_turn={ (2,0):"R", (2,2):"U", (0,2):"L", (0,0):"D" }
                self.twist("B",1,0)
                self.twist(face_to_turn[ ( cxz[0], cxz[1] ) ], 1 ,0 )
                self.twist("B",1)
                self.twist(face_to_turn[ ( cxz[0], cxz[1] ) ], 1 ,1 )


    def corner_flip(self): # flip all 4 corners (if necessary) on the front face. We'll flip everything in the bottom right corner, rotating the face around
        moves_to_undo=[]
        f_col = abs(self.cube[1,0,1][1])
        corner_flip_algo="RD'R'DRD'R'D"

        finished=False
        while not finished:
            while abs(self.cube[2,0,0][1]) != f_col :
                self.move(corner_flip_algo) # flips the corner, now need to move on and check the next one

            self.move("F'")
            moves_to_undo.append("F")

            if abs(self.cube[2,0,0][1]) == f_col and abs(self.cube[2,0,2][1]) == f_col\
            and abs(self.cube[0,0,0][1]) == f_col and abs(self.cube[0,0,2][1]) == f_col :
                finished=True
        self.move(moves_to_undo)





    def solve(self):
        self.scramble()
        self.print_cube()
        print("~~~~~~~~~~~~~~~~~~~")
        self.make_cross()
        self.print_cube()
        print("~~~~~~~~~~~~~~~~~~~")
        self.edge_flip()
        self.print_cube()
        print("~~~~~~~~~~~~~~~~~~~")
        self.solve_top_corners()
        self.print_cube()
        print("~~~~~~~~~~~~~~~~~~~")
        self.corner_flip()
        self.print_cube()
        print("~~~~~~~~~~~~~~~~~~~")
        print(len(self.solution))
        print(" ".join(self.solution))



c=Cube()

c.solve()



