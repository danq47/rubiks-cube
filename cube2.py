import numpy as np
import random as rd

# code to solve a rubik's cube
# Author: Daniel Quill

# When the robot is up and running, this code will take the current state of the cube as input
# and calculate a solution (as a list of moves).
#
# Obviously, there is much work that can be done to shorten this solution (as of yet, I
# haven't optimised it at all so we have many moves like RR'BD'D which is actually equivalent to B and 
# triple moves which can be written as anticlockwise moves i.e. RRR = R'
#
# The cube is represented as a numpy array where we can access each
# individual cubie by self.cube[x,y,z]. This will return us a colour vector [cx,cy,cz]
# which tells us the colour in the x,y,z directions (numbered
# 1-6, and 0 for no colour, as in the cx colour on the upper face)
#
# The cube is sitting with the [0,0,0] cube at the origin in the xyz positive octant
# The axes are pointing z(+ve) up, x(+ve) to the right, y(+ve) into screen, 
# with F facing us (i.e. the negative y direction)
# so the faces are defined by the planes F:y=0, B:y=2, L:x=0, R:x=2, D:z=0, U:z=2

class Cube:
 
##################################################################
#                                                                #
# Step 1 - Initialise the cube and define useful class variables #
#                                                                #
##################################################################

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
        self.corner_pieces = [ [self.r_col,self.d_col], [self.d_col,self.l_col], [self.l_col,self.u_col], [self.u_col,self.r_col] ] # when looking at B face, this is the corners 7 9 3 1
        # often we wish to know which face is opposite the one we are currently dealing with
        self.opposites = { "U":"D", "D":"U", "L":"R", "R":"L", "F":"B", "B":"F" }
        # we use these dicts for doing the a1_left/right algorithms
        self.face_to_right = { "D":"R", "R":"U", "U":"L", "L":"D" }
        self.face_to_left = { "D":"L", "L":"U", "U":"R", "R":"D" }


###################################################
#                                                 #
# Step 2 - define useful methods such as twists,  #
# and printing the cube to screen (for debugging) #
#                                                 #
###################################################


    # ----- 2.1 Print cube to screen -----
    def print_cube(self):
        # will be unfolded like 
        #    U
        #  L F R B
        #    D
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



    # ----- 2.2 Define twists on the faces of the cube -----
    def twist(self,face,clockwise=True,save_move=True): 

        # method to twist around a given face. Optional arguments are 
        # clockwise :(True/False) -> should we twist the face clockwise (default) or anticlockwise
        # save_move :(True/False) -> should we take a note of the move for the solution (always True except when we are scrambling the cube)

        # ----- 2.2.1 Save the moves to the solution array (if this isn't part of the initial scramble)
        if save_move : # take note of the move
            if clockwise :
                self.solution.append(face)
            elif not clockwise :
                self.solution.append(face+"'") # we use prime notation to denote anticlockwise turns i.e. R' is the opposite of R

        # ----- 2.2.2 Save current state of cube before moving anything
        new_cube = np.array(self.cube) # this will be the copy cube that we do all of our twists on, and eventually will set the main cube equal to this

        # ----- 2.2.3 Find the rotation matrix appropriate for a given face. The rest of the array gives the limits of the loop 
        # i.e. for rotating the Z=2 face, we have Zlow = 2 and Zhigh = 3 i.e. we never need to touch any pieces that have Z<2
        matrix_and_loop_ranges = { "F":[3,0,3,0,1,0,3] ,"B":[2,0,3,2,3,0,3], "L":[1,0,1,0,3,0,3], \
        "R":[0,2,3,0,3,0,3],"U":[4,0,3,0,3,2,3], "D":[5,0,3,0,3,0,1] } # this array is [matrix_index, xlow, xhigh, ylow, yhigh, zlow, zhigh]
        [matrix_index, xlow, xhigh, ylow, yhigh, zlow, zhigh] = matrix_and_loop_ranges[face]

        # ----- 2.2.4 Rotate the cubies in place 
        xyz_grid = [(x,y,z) for x in range(xlow -1,xhigh -1) for y in range(ylow -1,yhigh -1) for z in range(zlow -1,zhigh -1 ) ] # we subtract 1 from each coordinate to centre the cube on (0,0,0) so we can use the rotation matrices
        for xyz in xyz_grid :

            # ----- 2.2.4.1 Get destination position of current piece
            [ x1, y1, z1 ] = np.dot( self.rotation_matrices[matrix_index], xyz ) # coordinates of cubie after the twist

            # ----- 2.2.4.2 Get colour vector of current piece BEFORE it moves
            cubie_colour_vector = self.cube[ xyz[0]+1, xyz[1]+1, xyz[2]+1 ] # colour vector of the piece before the twist - need to add ones as the loops run through (-1,0,1) whereas self.cube is defined on 0 <= x(or y or z) <= 2

            # ----- 2.2.4.3 Rotate the cubie, and move it to the destination coordinates
            new_cube[ x1 +1, y1 +1, z1 +1 ] = abs( np.dot( self.rotation_matrices[matrix_index], cubie_colour_vector ) ) # this second dot with the rotation matrix rotates the orientation of the cubie

        # ----- 2.2.5 Set the main cube equal to the copied cube (which we have been twisting)
        self.cube = new_cube




    # ----- 2.3 Scramble cube -----
    def scramble(self,a=0):
        rd.seed(a) # set random seed for reproducability 
        for _ in range( rd.randint(20,40) ) :
            face , clockwise = rd.choice(["F","B","L","R","U","D"]) , rd.choice([0,1]) # choose a random face and turn it either clockwise or anticlockwise
            save_move = False
            self.twist( face , clockwise , save_move ) 
 



    # ----- 2.4 Combinations of moves -----
    def move_string(self, input_string):
        # This function takes a string of successive moves, and carries them out, i.e. FFDL does F(x2) then D then L

        # First rewrite any primed moves as a triple (i.e. R' = RRR )
        no_primes = "".join( input_string[ixx] if input_string[ixx] != "'" else input_string[ixx-1]*2 for ixx in range( len( input_string) ) )
        # Now separate this out into a list of single characters
        no_primes = list( no_primes )
        for move in no_primes:
            self.twist( move )




    # ----- 2.5 Find a certain piece -----
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




############################################
#                                          #
# Step 3 - Define the algorithms and moves #
#                                          #
############################################

    # ----- 3.1 Move edge pieces to back face - we need this to make the intial cross. 
    # If the cross pieces are in the back face then we can just rotate B until it is in the appropriate position (i,e, L face for FL piece) then rotate LL
    def edge_to_back( self, current_position ) :
        [x,y,z] = current_position

        if y == 0 : # piece is in the front, but the wrong position
            face_to_turn = { (1,0):"D", (2,1):"R", (1,2):"U", (0,1):"L" } # choose which face to turn based on [x,z]
            for _ in range(2) : self.twist( face_to_turn[(x,z)] ) # twist twice

        elif y == 1 : # piece is in the middle layer
            face_to_turn = { (2,0):"D", (2,2):"R", (0,2):"U", (0,0):"L"}
            move_to_back = face_to_turn[(x,z)] + "B" + face_to_turn[(x,z)] + "'" # move it to the back, rotate it out of the way, then turn the other face back. This stops us messing up F
            self.move_string( move_to_back )



    # ----- 3.2 Move from middle layer to back (to do a1_left/right)
    def middle_layer_to_back(self,position): 
        [x,y,z] = position
        face_to_move = { (2,0):"D", (2,2):"R" , (0,2):"U" , (0,0):"L" } # choose which face to turn based on [x,z]
        self.a1_right(face_to_move[(x,z)])




    # ----- 3.3 Flip FD edge piece
    def edge_flip(self):
        move = "DR'B'RDD"
        self.move_string(move)




    # ----- 3.4 Corner left ----
    def left_corner(self, input_face):
        # Now we imagine rotating the F face is on top and D is facing us. 
        # This method puts a corner piece from the bottom left of D to the top left, i.e. into the F face
        # This is actually more general, and takes the face (D in the example) as an input
        # All later algorithms are built around this
        
        # The algorithm will be made up of B twists, and a different face, depending on which face we're doing this algo on
        face_to_twist = { "D":"L", "L":"U", "U":"R", "R":"D" }
        algorithm = "B" + face_to_twist[input_face] + "B'" + face_to_twist[input_face] + "'"
        self.move_string(algorithm)



    # ----- 3.5 Corner Right -----
    def right_corner(self, input_face):
        # Same as above except moving piece from bottom right to top right corner
        face_to_twist = { "D":"R", "R":"U", "U":"L", "L":"D" }
        algorithm = "B'" + face_to_twist[input_face] + "'" + "B" + face_to_twist[input_face]
        self.move_string(algorithm)




    # ----- 3.6 A1 left ----
    def a1_left(self, input_face):
        # This is the main algorithm, used to fill the second layer
        # It involves two faces, input_face, and the face to the left
        self.left_corner(input_face)
        self.right_corner( self.face_to_left[input_face] )




    # ----- 3.7 A1 Right
    def a1_right(self, input_face):
        # same as above but putting a piece in the middle layer to the right rather than the left
        self.right_corner(input_face)
        self.left_corner( self.face_to_right[input_face] )




        
#############################
#                           #
# Step 4 - Solve the cube!! #
#                           #
#############################


    # ----- 4.1 Make a cross on F -----
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

        # manually check that we do have the cross
        for piece in pieces_of_cross :
            current_position, original_position = self.find_piece( self.f_col, piece )
            if current_position != original_position :
                print("Error")
                print("Couldn't build cross on F-face")
                print("Exiting...")
                exit()




    # ----- 4.2 Reorient F_cross ------
    def flip_F_cross(self):
        ixx = 0 
        while ixx < 4 :
            if self.cube[1,0,0][1] != self.f_col : # check if it is oriented correctly
                self.edge_flip()
            self.twist("F") # move to next piece
            ixx += 1 # do this a maximum of 4 times to get back to original state

        # check 
        ixx = 0 
        while ixx < 4 :
            if self.cube[1,0,0][1] != self.f_col : # check if it is oriented correctly
                print("Error")
                print("Couldn't reorient F-cross properly")
                print("Exiting...")
                exit()
            self.twist("F")
            ixx += 1




    # ----- 4.3 Solve top corners ------
    def solve_top_corners(self):
        # ------ 4.3.1 These will be the colours of the 4 corner pieces (along with f_col obviously)
        for piece in self.corner_pieces :

            current_position, original_position = self.find_piece( self.f_col, *piece ) # *piece means that the elements of piece are arguments of the function

            # ----- 4.3.2 Three cases now, (1) Piece is in the correct position already, (2) Piece is in the F layer but wrong position (put to back and then move to correct position), (3) Piece is in B layer (move to correct position)
            if current_position != original_position : 

                if current_position[1] == 0 : # it's in the front, move to back with left_corner(). The current location tells us which face to do left_corner() on
                    face_to_twist = { (2,2):"U", (0,2):"L", (0,0):"D", (2,0):"R" }
                    self.left_corner( face_to_twist[ (current_position[0], current_position[2]) ] )
                    current_position, original_position = self.find_piece( self.f_col, *piece )

                # ----- 4.3.3 Now it's definitely in the back
                cxz = [ current_position[0], current_position[2] ] # current xz
                oxz = [ original_position[0], original_position[2] ] # original xz
                while cxz != oxz : # while not in the right face
                    self.twist("B") # rotate
                    current_position, original_position = self.find_piece( self.f_col, *piece )
                    cxz = [ current_position[0], current_position[2] ]
                    
                # ----- 4.3.4 It's in the right place, just put it in with right_corner()
                self.right_corner( self.faces_to_colours[ piece[1] ] )

        # check
        for piece in self.corner_pieces :
            current_position, original_position = self.find_piece( self.f_col, *piece )
            if current_position != original_position :
                print("Error")
                print("F corners not correct")
                print("Exiting...")
                exit()



    # ----- 4.4 Reorient top corners
    def corner_flip(self):
        # reorient the bottom right corner on F
        corner_flip_algo="RD'R'DRD'R'D"
        ixx=0
        while ixx < 4:
            while self.cube[2,0,0][1] != self.f_col :
                self.move_string(corner_flip_algo)
            self.move_string("F'")
            ixx += 1

        # check
        ixx=0
        while ixx < 4:
            if self.cube[2,0,0][1] != self.f_col :
                print("Error")
                print("F corners not oriented correctly")
                print("Exiting...")
                exit()
            self.twist("F")
            ixx += 1
                


    # ---- 4.5 Solve Middle layer
    def second_layer(self):
        start_algorithm = { self.r_col:(2,1) , self.u_col:(1,2) , self.l_col:(0,1) , self.d_col:(1,0) }  # this is the position we need to get each piece into before performing a1_right()
        face_to_twist = { (1,0):"D" , (2,1):"R" , (1,2):"U" , (0,1):"L" }

        for piece in self.corner_pieces :
            current_position, original_position = self.find_piece( *piece )

            if current_position != original_position :
                # 4.5.1 If the piece is already in the middle layer, then move to the back
                if current_position[1] == 1 :
                    self.middle_layer_to_back(current_position)
                    current_position, original_position = self.find_piece( *piece )

                # 4.5.2 Now it's in the back, move to the correct mid layer position
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

        # check
        for piece in self.corner_pieces :
            current_position, original_position = self.find_piece( *piece )
            if current_position != original_position :
                print("Error")
                print("Second layer edge pieces not in correct position")
                print("Exiting...")
                exit()




    # ----- 4.6 Make a cross on the bottom layer
    def bottom_cross(self):
        b_cross_algorithm = "URBR'B'U'"
        piece_colours = [ piece[0] for piece in self.corner_pieces ]

        def get_orientations():
            # returns a list of the orientations of [ R, D, L, U ] edges (with B face) where we have 1 for correct orientation and 0 for incorrect. This is pieces 4 8 6 2 when looking at B.
            orientations = []
            for piece in piece_colours :
                current_position, original_position = self.find_piece( piece, self.b_col )
                orientations.append( self.cube[original_position][1] == self.b_col) 
            return orientations

        # Want to make a cross on the B layer oriented correctly (we don't need the pieces in the right place in this step, we will move them next)
        # Different possibilities are
        # (1) Already there
        # (2) none are oriented right
        # (3) veritcal line shape, 2 and 8 
        # (4) horizontal line, 4 and 6
        # (5) L shape i.e. pieces 2 and 4 or 2 and 6 etc are oriented right

        if sum( get_orientations() ) == 4:
            pass
        elif sum( get_orientations() ) == 0:
            self.move_string( b_cross_algorithm ) # do the algorithm randomly so we flip 2 pieces


        if get_orientations() == [0,1,0,1] :
            self.move_string("B")
            self.move_string( b_cross_algorithm )
        elif get_orientations() == [1,0,1,0] :
            self.move_string( b_cross_algorithm )
        elif sum( get_orientations() ) != 4 : # don't need to do anything if they're all already oriented correctly
            while get_orientations() != [0,1,1,0] :
                self.move_string("B")
            self.move_string( b_cross_algorithm )
            self.move_string( b_cross_algorithm )

        # check
        ixx = 0 
        while ixx < 4 :
            if self.cube[1,2,0][1] != self.b_col : # check if it is oriented correctly
                print("Error")
                print("B-cross not oriented properly")
                print("Exiting...")
                exit()
            self.twist("B")
            ixx += 1




    # ----- 4.7 put bottom cross pieces in right place
    def bottom_cross_swap(self):

        def position_of_edges():
            # returns a list [ R, D, L, U ] edges on the bottom, with a 1 if the RB edge piece (for example) is in the correct position
            piece_colours = [ piece[0] for piece in self.corner_pieces ] # R D L U i.e. when looking at B this is pieces 4 8 6 2
            correct_position = []
            for piece in piece_colours :
                current_position, original_position = self.find_piece( piece, self.b_col )
                correct_position.append( current_position == original_position)
            return correct_position

        # first check we don't already have the correct cross
        ixx = 0
        while ixx < 4 :
            ixx += 1
            if sum(position_of_edges()) == 4 :
                break
            else:
                self.move_string("B")

        valid_starting_position = [ [1,1,0,0], [0,1,1,0], [0,0,1,1], [1,0,0,1] ] # if position_of_edges() equals any of these, then we can do the algorithm. Basically, we need two adjacent edges correct and the other two swapped 
        algorithm_face = { (1,1,0,0):"R", (0,1,1,0):"D", (0,0,1,1):"L", (1,0,0,1):"U" } # the face we twist in the algorithm depends on which edge pieces are adjacent

        ixx = 0
        tmp = position_of_edges()
        while tmp not in valid_starting_position :

            if ixx % 4 == 0 :
                self.move_string( "RBR'BRBBR'B" ) # If none of the positions are in valid_starting_position, do the algorithm randomly and next time one should be valid

            self.move_string("B") # twist B, then check again if we can start the algorithm
            ixx += 1
            tmp = position_of_edges()

        face = algorithm_face[ tuple(tmp) ] # figure out which face we use for the algorithm
        algo = face + "B" + face + "'B" + face + "BB" + face + "'B" # build the algorithm using the correct face

        self.move_string( algo )

        # check
        piece_colours = [ piece[0] for piece in self.corner_pieces ]
        for piece in piece_colours :
            current_position, original_position = self.find_piece( piece, self.b_col )
            if current_position != original_position :
                print("Error")
                print("B-cross pieces not in correct positions")
                print("Exiting...")
                exit()




    # ----- 4.8 put B corner pieces in place, very similar to moving around the edge pieces
    def bottom_corners(self):

        def position_of_corners():
            # returns a list [ RDB, DLB, LUB, URB ] corners with a 1 corner piece is in the right position
            correct_position = []
            for piece in self.corner_pieces : # this will be corner pieces 7 9 3 1 when looking at B
                current_position, original_position = self.find_piece( self.b_col, *piece )
                correct_position.append( current_position == original_position)
            return correct_position


        if sum( position_of_corners() ) == 4 : # all corners are in right place
            pass
        elif sum( position_of_corners() ) == 0 :
            self.move_string( "BRB'L'BR'B'L" )

        face = ["",""]

        if position_of_corners() == [1,0,0,0] : # RDB corner is in place
            face = ["D","U"]
        elif position_of_corners() == [0,1,0,0]: # DLB corner is in place
            face = ["L","R"]
        elif position_of_corners() == [0,0,1,0]: # LUB corner is in place
            face = ["U","D"]
        elif position_of_corners() == [0,0,0,1]: # URB corner is in place
            face = ["R","L"]

        algorithm = "B" + face[0] + "B'" + face[1] + "'B" + face[0] + "'B'" + face[1]

        while sum( position_of_corners() ) != 4 :
            self.move_string( algorithm )

        # check
        for piece in self.corner_pieces : # this will be corner pieces 7 9 3 1 when looking at B
            current_position, original_position = self.find_piece( self.b_col, *piece )
            if current_position != original_position :
                print("Error")
                print("B-corner pieces not in correct position")
                print("Exiting...")
                exit()





    # 4.9 The final bit, now that the corners are in the right places we just need to reorient them
    def reorient_bottom_corners(self):
        # reorient the bottom right corner of the B face (piece 9 if looking at the face)
        moves_to_undo = []
        algorithm = "LD'L'DLD'L'D"

        ixx = 0
        while ixx < 4 :
            while self.cube[0,2,0][1] != self.b_col : # not oriented correctly
                self.move_string( algorithm )
            self.move_string("B'")
            moves_to_undo.append("B")
            ixx += 1

        self.move_string( ''.join(moves_to_undo) )

        # check
        ixx = 0
        while ixx < 4 :
            if self.cube[0,2,0][1] != self.b_col :
                print("Error")
                print("B-corner pieces not oriented correctly")
                print("Exiting...")
                exit()
            self.move_string("B'")
            ixx += 1


################################################
#                                              #
# Step 5 - putting it all together and solving #
#                                              #
################################################


    def solve(self):

        self.make_F_cross()
        self.flip_F_cross()
        self.solve_top_corners()
        self.corner_flip()
        self.second_layer() 
        self.bottom_cross()
        self.bottom_cross_swap()
        self.bottom_corners()
        self.reorient_bottom_corners()
        self.print_cube()
        # print( len(self.solution), self.solution )



###########################################################
#                                                         #
# Step 6 - beginning to reduce the length of the solution #
#                                                         #
###########################################################

    
    # ----- 6.1 Delete anything that comes up 4 in a row ----
    def delete_quads(self, move_list): 
        new_solution = []
        for move in move_list :
            if len( new_solution ) >= 4 and \
            new_solution[-1] == new_solution[-2] and \
            new_solution[-1] == new_solution[-3] and \
            new_solution[-1] == move :
                new_solution.pop()
                new_solution.pop()
                new_solution.pop()
            else:
                new_solution.append(move)

        return new_solution


    # ----- 6.2 Replace XXX with X' and X'X'X' with X ------
    def replace_trips(self, move_list) :
        new_solution = []
        for move in move_list :
            if len( new_solution ) >= 3 and \
            new_solution[-1] == new_solution[-2] and \
            new_solution[-1] == move :
                new_solution.pop()
                new_solution.pop()
                if len(move) == 2 :
                    new_solution.append( move[0] ) # if it's R'R'R' replace with R
                else:
                    new_solution.append( move + "'" ) # append a prime
            else:
                new_solution.append( move )

        return new_solution




    # ----- 6.X Reduce solution (not finished!!) -----
    def reduce_solution(self):
        self.solution = self.delete_quads( self.solution )
        self.solution = self.replace_trips( self.solution )

# Can further reduce this by looking at what subset of moves commute with each other
# i.e. I know that opposite sides commute: RLR' = L and we can look for more complicated patterns that commute





c = Cube()
c.scramble()
c.solve()
c.print_cube()
print( "Solution is ",len(c.solution)," moves before we reduce it." )
c.reduce_solution()
print( "Solution is ",len(c.solution)," moves after we reduce it.")

for kxx in range(10000):
    print(kxx)
    c=Cube()
# c.print_cube()
    c.scramble(kxx)
    c.solve()



