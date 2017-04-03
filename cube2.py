# second attempt at writing code to solve Rubik's cube

import numpy as np
import random as rd




# We will represent the cube as a numpy array where we can access each
# individual cubie by cube[x,y,z]. This will return us a colour vector [cx,cy,cz]
# which tells us the colour in the x,y,z directions (numbered
# 1-6, and 0 for no colour, as in the cx colour on the upper face)
# A minus sign for colour means that it is facing in the negative i direction
# The cube is sitting with the [0,0,0] cube at the origin in the xyz positive octant
# The axes are pointing z up, x to the right, y into screen with F facing us (negative y direction)
# so the faces are defined by the planes F:y=0, B:y=2, L:x=0, R:x=2, D:z=0, U:z=2

class Cube:
  
    # ----- 1. Initialise a cube, and also define some useful global variables
    def __init__(self):

        # ----- 1.1 Build an empty cube -----
        self.cubie_colour = [0,0,0] # this will be the colour vector at each cubie point, start it off empty (as zeros)
        self.line = [ self.cubie_colour[:] for _ in range(3)]
        self.face = [ self.line[:] for _ in range(3)]
        self.empty_cube = [ self.face[:] for _ in range(3)] # build up the cube
        self.cube = np.array(self.empty_cube) # this is the best way I can see of copying a very deeply nested list?? Surely there's a better way but I don't see one yet

        # ----- 1.2 Define the colours of the faces
        [ self.l_col, self.f_col, self.d_col, self.u_col, self.b_col, self.r_col ] = [1,2,3,4,5,6] # colours of the left, front, down etc faces explicitly set as numbers
        x_colour = { 0:self.l_col, 1:0, 2:self.r_col } # colours for the faces - x=0 layer (L) has colour -1 in the minus x direction, x=1 layer has no x colour, and x=2 layer (R) has colour 6 
        y_colour = { 0:self.f_col, 1:0, 2:self.b_col }
        z_colour = { 0:self.d_col, 1:0, 2:self.u_col }

        # ----- 1.3 Set the face colours
        xyz_grid = [(x,y,z) for x in range(3) for y in range(3) for z in range(3)]
        for xyz in xyz_grid :
            self.cube[xyz] = [ x_colour[xyz[0]] , y_colour[xyz[1]] , z_colour[xyz[2]] ]

        # ----- 1.4 Save the solved cube
        self.original_cube=self.cube # so we can check if pieces are in the correct place
        
        # ----- 1.5 Save the solution string (each twist we do to solve gets appended to this)
        self.solution=[] 

        # ----- 1.6 Define rotation matrices used for twists
        self.x_clockwise = [ [1,0,0], [0,0,1], [0,-1,0] ]
        self.x_anticlockwise = [ [1,0,0], [0,0,-1], [0,1,0] ]
        self.y_clockwise = [ [0,0,-1], [0,1,0], [1,0,0] ]
        self.y_anticlockwise = [ [0,0,1], [0,1,0], [-1,0,0] ]
        self.z_clockwise = [ [0,1,0], [-1,0,0], [0,0,1] ]
        self.z_anticlockwise = [ [0,-1,0], [1,0,0], [0,0,1] ]
        self.rotation_matrices = [self.x_clockwise,self.x_anticlockwise,self.y_clockwise,self.y_anticlockwise,self.z_clockwise,self.z_anticlockwise]
    
        # 1.7 Dict to get the associated face for a colour or vice versa
        self.faces_to_colours = { self.r_col:"R", self.d_col:"D", self.l_col:"L", self.u_col:"U" , "R":self.r_col, "D":self.d_col, "L":self.l_col, "U":self.u_col }
        self.corner_pieces = [ [self.r_col,self.d_col], [self.d_col,self.l_col], [self.l_col,self.u_col], [self.u_col,self.r_col] ]
        # often we wish to know which face is opposite the one we are currently dealing with
        self.opposites = { "U":"D", "D":"U", "L":"R", "R":"L", "F":"B", "B":"F" }
        # we use these dicts for doing the a1_left/right algorithms
        self.face_to_right = { "D":"R", "R":"U", "U":"L", "L":"D" }
        self.face_to_left = { "D":"L", "L":"U", "U":"R", "R":"D" }

    # ----- 2. Print cube -----
    def print_cube(self):
        # will be unfolded like 
        #   U
        #  LFRB
        #   D
        l_face = [ [ self.cube[ 0, 2-y, 2-z ][0] for y in range(3) ] for z in range(3) ]
        f_face = [ [ self.cube[ x , 0 , 2-z ][1] for x in range(3) ] for z in range(3) ]
        r_face = [ [ self.cube[ 2 , y , 2-z ][0] for y in range(3) ] for z in range(3) ]
        b_face = [ [ self.cube[ 2-x, 2, 2-z ][1] for x in range(3) ] for z in range(3) ]
        u_face = [ [ self.cube[ x , 2-y , 2 ][2] for x in range(3) ] for y in range(3) ]
        d_face = [ [ self.cube[ x , y , 0   ][2] for x in range(3) ] for y in range(3) ]

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for _ in range(3) :
            print("         ", u_face[_])
        for _ in range(3) :
            print( l_face[_] , f_face[_] , r_face[_], b_face[_] )
        for _ in range(3) :
            print("         ", d_face[_])

    # ----- 3. Define twists on the faces of the cube -----
    def twist(self,face,clockwise=True,save_move=True): 

        # method to twist around a given face. Optional arguments are 
        # clockwise :(True/False) -> should we twist the face clockwise (default) or anticlockwise
        # save_move :(True/False) -> should we take a note of the move for the solution (always True except when we are scrambling the cube)

        # ----- 2.1 Save the moves to the solution array (if this isn't part of the initial scramble)
        if save_move : # take note of the move
            if clockwise :
                self.solution.append(face)
            elif not clockwise :
                self.solution.append(face+"'") # we use prime notation to denote anticlockwise turns i.e. R' is the opposite of R

        # ----- 2.2 Save current state of cube before moving anything
        new_cube = np.array(self.cube) # this will be the copy cube that we do all of our twists on, and eventually will set the main cube equal to this

        # ----- 2.3 Find the rotation matrix appropriate for a given face. The rest of the array gives the limits of the loop i.e. for rotating the Z=2 face, we do not need to Zlow = 2 and Zhigh =3 i.e. we never need to touch any pieces that have Z<2
        matrix_and_loop_ranges = { "F":[3,0,3,0,1,0,3] ,"B":[2,0,3,2,3,0,3], "L":[1,0,1,0,3,0,3], \
        "R":[0,2,3,0,3,0,3],"U":[4,0,3,0,3,2,3], "D":[5,0,3,0,3,0,1] } # this array is [matrix_index, xlow, xhigh, ylow, yhigh, zlow, zhigh]
        [matrix_index, xlow, xhigh, ylow, yhigh, zlow, zhigh] = matrix_and_loop_ranges[face]

        # ----- 2.4 Rotate the cubies in place 
        xyz_grid = [(x,y,z) for x in range(xlow -1,xhigh -1) for y in range(ylow -1,yhigh -1) for z in range(zlow -1,zhigh -1 ) ] # we subtract 1 from each coordinate to centre the cube on (0,0,0) so we can use the rotation matrices
        for xyz in xyz_grid :

            # ----- 2.4.1 Get destination position of current piece
            [ x1, y1, z1 ] = np.dot( self.rotation_matrices[matrix_index], xyz ) # coordinates of cubie after the twist

            # ----- 2.4.2 Get colour vector of current piece BEFORE it moves
            cubie_colour_vector = self.cube[ xyz[0]+1, xyz[1]+1, xyz[2]+1 ] # colour vector of the piece before the twist - need to add ones as the loops run through (-1,0,1) whereas self.cube is defined on 0 <= x(or y or z) <= 2

            # ----- 2.4.3 Rotate the cubie, and move it to the destination coordinates
            new_cube[ x1 +1, y1 +1, z1 +1 ] = abs( np.dot( self.rotation_matrices[matrix_index], cubie_colour_vector ) ) # this second dot with the rotation matrix rotates the orientation of the cubie

        # ----- 2.5 Set the main cube equal to the copied cube (which we have been twisting)
        self.cube = new_cube

    # ----- 4. Scramble cube -----
    def scramble(self):
        rd.seed(a=4) # set random seed for reproducability 
        for _ in range( rd.randint(20,40) ) :
            face , clockwise = rd.choice(["F","B","L","R","U","D"]) , rd.choice([0,1]) # choose a random face and turn it either clockwise or anticlockwise
            save_move = False
            self.twist( face , clockwise , save_move ) 
 
    # ----- 5. Combinations of moves -----
    def move_string(self, input_string):
        # This function takes a string of successive moves, and carries them out, i.e. FFDL does F(x2) then D then L

        # First rewrite any primed moves as a triple (i.e. R' = RRR )
        no_primes = "".join( input_string[ixx] if input_string[ixx] != "'" else input_string[ixx-1]*2 for ixx in range( len( input_string) ) )
        # Now separate this out into a list of single characters
        no_primes = list( no_primes )
        for move in no_primes:
            self.twist( move )

    # ----- 6. Find a certain piece -----
    def find_piece(self, c1, c2=0, c3=0 ):
        # Returns a list of 2 tuples, the coordinates of the piece now, and its location in the solved cube
        # It takes at least 1 colour as an input, but up to 3.
        colours = abs( np.array( [ c1, c2, c3 ] ) ) # take absolute value as we don't care about orientation
        colours = set( colours ) # we also don't care about the order so we convert to set
        xyz_grid = [(x,y,z) for x in range(3) for y in range(3) for z in range(3)]

        # We will find both the original location, and the current location, and return both
        for xyz in xyz_grid :
            if colours == set( abs( self.original_cube[ xyz ] ) ) : original = xyz
            if colours == set( abs( self.cube[ xyz ] ) ) : current = xyz

        return [ current, original ]

    # ----- 7. Algorithms/moves -----

    # ----- 7.1 Move edge pieces to back - we need this to make the intial cross. If the cross pieces are in the back face then we can just rotate B until it is in the appropriate position (i,e, L face for FL piece) then rotate LL
    def edge_to_back( self, current_position ) :
        [x,y,z] = current_position

        if y == 0 : # piece is in the front, but the wrong position
            face_to_turn = { (1,0):"D", (2,1):"R", (1,2):"U", (0,1):"L" } # choose which face to turn based on [x,z]
            for _ in range(2) : self.twist( face_to_turn[(x,z)] ) # twist twice

        elif y == 1 : # piece is in the middle layer
            face_to_turn = { (2,0):"D", (2,2):"R", (0,2):"U", (0,0):"L"}
            move_to_back = face_to_turn[(x,z)] + "B" + face_to_turn[(x,z)] + "'" # move it to the back, rotate it out of the way, then turn the other face back. This stops us messing up F
            self.move_string( move_to_back )

    # ----- 7.2 Move from middle layer to back (to do a1_left/right)
    def middle_layer_to_back(self,position): 
        [x,y,z] = position
        face_to_move = { (2,0):"D", (2,2):"R" , (0,2):"U" , (0,0):"L" } # choose which face to turn based on [x,z]
        self.a1_right(face_to_move[(x,z)])

    # ----- 7.2 Flip FD edge piece
    def edge_flip(self):
        move = "DR'B'RDD"
        self.move_string(move)

    # ----- 7.3 Corner left ----
    def left_corner(self, input_face):
        # Now we imagine rotating the F face is on top and D is facing us. 
        # This method puts a corner piece from the bottom left of D to the top left, i.e. into the F face
        # This is actually more general, and takes the face (D in the example) as an input
        # All later algorithms are built around this
        
        # The algorithm will be made up of B twists, and a different face, depending on which face we're doing this algo on
        face_to_twist = { "D":"L", "L":"U", "U":"R", "R":"D" }
        algorithm = "B" + face_to_twist[input_face] + "B'" + face_to_twist[input_face] + "'"
        self.move_string(algorithm)

    # ----- 7.4 Corner Right -----
    def right_corner(self, input_face):
        # Same as above except moving piece from bottom right to top right corner
        face_to_twist = { "D":"R", "R":"U", "U":"L", "L":"D" }
        algorithm = "B'" + face_to_twist[input_face] + "'" + "B" + face_to_twist[input_face]
        self.move_string(algorithm)

    # ----- 7.5 A1 left ----
    def a1_left(self, input_face):
        # This is the main algorithm, used to fill the second layer
        # It involves two faces, input_face, and the face to the left
        self.left_corner(input_face)
        self.right_corner( self.face_to_left[input_face] )

    # ----- 7.6 A1 Right
    def a1_right(self, input_face):
        # same as above but putting a piece in the middle layer to the right rather than the left
        self.right_corner(input_face)
        self.left_corner( self.face_to_right[input_face] )

    def a2_left(self, input_face):
        # a1_left followed by a1_right
        self.a1_left(input_face)
        self.twist("B")
        self.a1_right( self.face_to_left[input_face] )

    def a2_right(self, input_face):
        # a1_left followed by a1_right
        self.a1_left(input_face)
        self.twist("B'")
        self.a1_right( self.face_to_right[input_face] )

    def bottom_cross_algo(self):
        # reorient bottom cross pieces
        self.move_string("URBR'B'U'")
        
    # ----- 8. Steps to solve the cube

    # ----- 8.1 Make a cross on F -----
    def make_F_cross(self):
        pieces_of_cross = [ piece[0] for piece in self.corner_pieces ] # these are the pieces we need for the cross (along with f_col)
        for piece in pieces_of_cross :

            current_position, original_position = self.find_piece( self.f_col, piece )

            if current_position != original_position :
                if current_position[1] < 2 : # it's not yet in the back
                    self.edge_to_back(current_position) 
                    current_position = self.find_piece( self.f_col, piece )[0] # update current position of piece after moving it

                # Now the piece is definitely in the back, we just need to rotate it to the right face, and then rotate into place
                cxz = [ current_position[0], current_position[2] ] # current xz
                oxz = [ original_position[0], original_position[2] ] # original xz
                while cxz != oxz : # while not in the right face
                    self.twist("B",1) # rotate
                    current_position  = self.find_piece( self.f_col , piece )[0]
                    cxz=[current_position[0],current_position[2]]

                self.twist( self.faces_to_colours[piece] )
                self.twist( self.faces_to_colours[piece] )

    # ----- 8.2 Reorient F_cross ------
    def flip_F_cross(self):
        ixx = 0 
        while ixx < 4 :
            if self.cube[1,0,0][1] != self.f_col : # check if it is oriented correctly
                self.edge_flip()
            self.twist("F") # move to next piece
            ixx += 1 # do this a maximum of 4 times to get back to original state

    # ----- 8.3 Solve top corners ------
    def solve_top_corners(self):
        # ------ 8.3.1 These will be the colours of the 4 corner pieces (along with f_col obviously)
        for piece in self.corner_pieces :

            current_position, original_position = self.find_piece( self.f_col, *piece ) # *piece means that the elements of piece are arguments of the function

            # ----- 8.3.2 Three cases now, (1) Piece is in the correct position already, (2) Piece is in the F layer but wrong position (put to back and then move to correct position), (3) Piece is in B layer (move to correct position)
            if current_position != original_position : 

                if current_position[1] == 0 : # it's in the front, move to back with left_corner(). The current location tells us which face to do left_corner() on
                    face_to_twist = { (2,2):"U", (0,2):"L", (0,0):"D", (2,0):"R" }
                    self.left_corner( face_to_twist[ (current_position[0], current_position[2]) ] )
                    current_position, original_position = self.find_piece( self.f_col, *piece )

                # ----- 8.3.3 Now it's definitely in the back
                cxz = [ current_position[0], current_position[2] ] # current xz
                oxz = [ original_position[0], original_position[2] ] # original xz
                while cxz != oxz : # while not in the right face
                    self.twist("B") # rotate
                    current_position, original_position = self.find_piece( self.f_col, *piece )
                    cxz = [ current_position[0], current_position[2] ]
                    
                # ----- 8.3.4 It's in the right place, just put it in with right_corner()
                self.right_corner( self.faces_to_colours[ piece[1] ] )

    # ----- 8.4 Reorient top corners
    def corner_flip(self):
        # reorient the bottom right corner on F
        corner_flip_algo="RD'R'DRD'R'D"
        ixx=0
        while ixx < 4:
            while self.cube[2,0,0][1] != self.f_col :
                self.move_string(corner_flip_algo)
            self.move_string("F'")
            ixx += 1

    # ---- 8.5 Solve Middle layer
    def second_layer(self):
        start_algorithm = { self.r_col:(2,1) , self.u_col:(1,2) , self.l_col:(0,1) , self.d_col:(1,0) }  # this is the position we need to get each piece into before performing a1_right()
        face_to_twist = { (1,0):"D" , (2,1):"R" , (1,2):"U" , (0,1):"L" }

        for piece in self.corner_pieces :
            current_position, original_position = self.find_piece( *piece )

            if current_position != original_position :
                # 8.5.1 If the piece is already in the middle layer, then move to the back
                if current_position[1] == 1 :
                    self.middle_layer_to_back(current_position)
                    current_position, original_position = self.find_piece( *piece )

                # 8.5.2 Now it's in the back, move to the correct mid layer position
                cxz = ( current_position[0] , current_position[2] )
                while cxz != start_algorithm[piece[0]] : # while the piece isn't in the correct position in the back layer
                    self.twist("B")
                    current_position, original_position = self.find_piece( *piece )
                    cxz = ( current_position[0] , current_position[2] )
                # it's in the right position, now just need to do algorithm a1
                self.a1_left( face_to_twist[cxz] )

            # Now they are all in the right place, just need to check they are oriented correctly
            oriented_correctly = all( self.cube[original_position] == self.original_cube[original_position] )
            if not oriented_correctly:
                face = self.faces_to_colours[ piece[0] ]
                self.a1_left(face)
                self.move_string("BB")
                self.a1_left(face)


    # ----- 8.6 Make a cross on the bottom layer
    def bottom_cross(self):
        piece_colours = [ piece[0] for piece in self.corner_pieces ]
        orientations = []
        # Want to make a cross on the B layer oriented correctly (we don't need the pieces in the right place in this step, we will move them next)
        # Different possibilities are
        # (1) Already there
        # (2) none are oriented right
        # (3) veritcal line shape, 2 and 8 
        # (4) horizontal line, 4 and 6
        # (5) L shape i.e. pieces 2 and 4 or 2 and 6 etc are oriented right
        # we will make an array of the 6 2 4 8 orientations (true is correct and false is incorrect) on the B face
        for piece in piece_colours :
            current_position, original_position = self.find_piece( piece, self.b_col )
            orientations.append( self.cube[original_position][1] == self.b_col) 

        if sum(orientations) == 4:
            pass
        elif sum(orientations) == 0:
            self.bottom_cross_algo()
            self.move_string("BB")
            self.bottom_cross_algo()
        elif orientations == [0,1,0,1] :
            self.move_string("B")
            self.bottom_cross_algo()
        elif orientations == [1,0,1,0] :
            self.bottom_cross_algo()
        else:
            while orientations != [0,1,1,0] :
                self.move_string("B")
                orientations.append( orientations.pop(0) ) # update the orientations by cycling through once
            self.bottom_cross_algo()
            self.bottom_cross_algo()






        # first check if we've got a cross at all (even if we need to rotate B)
        # cross = False
        # ixx=0
        # while ixx < 4 and cross == False :
        #     current_position, original_position = self.find_piece( piece, self.b_col )

        #     if original_position == current_position : 
        #         cross = True
        #     else:
        #         self.move("B")
        #     ixx+=1

        # # if we've got a cross, great, we'll just skip straight to the end stage (where we reorient the cross)
        # if cross == False : # now we've got two cases - either we have a configuration where only one piece is in the right position (start position), and we can work with this, or else we can't get this 1 right position, and we will have to appply the algorithm twice

        #     start_position = False
        #     while start_position == False :
                
        #         ixx = 0
        #         while ixx < 4 and start_position == False :
        #             current_position, original_position = self.find_piece( piece, self.b_col )
        #             check_positions=0 # check how many of the cross pieces are in the right place
                    
        #             for _ in range(4):
        #                 if original_position[_] == current_position[_] :
        #                     check_positions += 1

        #             if check_positions == 1 :
        #                 start_position = True
        #             else:
        #                 self.move("B")
        #             ixx+=1
        #         # if we finish the inner while loop without a start position we can just do the algorithm and then we will definitely have a start position next time round
        #         if start_position == False :
        #             self.a2_right("U")

        #     # now we're in a position to do the algorithm, we just need to work out which direction and which faces
        #     start_face=""
        #     for piece in piece_colours:
        #         current_position, original_position = self.find_piece( piece, self.b_col )
        #         if current_position == original_position :
        #             start_face = self.faces_to_colours[piece]
        #             break


        #     start_right=False
        #     self.move_string("B") # move to check which direction we should start the algorithm. if the opposite face has the piece in the right position then this is the wrong first move - we'll start the algorithm to the left instead
        #     current, original = self.locate_piece( self.faces_to_colours [ self.opposites[ start_face ] ] , b_col) # this is checking the direction we permute the other 3 pieces
        #     start_right = (current == original)# start the algorithm to the right if these are equivalent, and to the left if not
        #     self.move_string("B'") # undo the checking move    

        #     if start_right self.a2_right(start_face) else self.a2_left(start_face) 





    def solve(self):
        self.make_F_cross()
        self.flip_F_cross()
        self.solve_top_corners()
        self.corner_flip()
        self.second_layer()
        self.print_cube()
        self.bottom_cross()
        self.print_cube()

        # print( len(self.solution), self.solution )













c=Cube()
c.print_cube()
c.scramble()
c.solve()


# print(c.cube[:,0,:][:,1,:])

# print(c.find_piece(1,2,3))
# c.twist("L")
# print(c.find_piece(1,2,3))
# c.twist("B")
# print(c.find_piece(1,2,3))
# print(c.cube[0,0,2])
# c.twist("L")
# c.move_string("LLDD'L'L'L'")
# print(c.cube[0,0,2])
# print(c.u_col)
