import numpy as np

class Cube:

# initialize a full cube

    def __init__(self):
        # self.upper  = np.array([[1 ,2 ,3 ],[4 ,"U",5 ],[6 ,7 ,8 ]])
        # self.left   = np.array([[9 ,10,11],[12,"L",13],[14,15,16]])
        # self.front  = np.array([[17,18,19],[20,"F",21],[22,23,24]])
        # self.right  = np.array([[25,26,27],[28,"R",29],[30,31,32]])
        # self.back   = np.array([[33,34,35],[36,"B",37],[38,39,40]])
        # self.down   = np.array([[41,42,43],[44,"D",45],[46,47,48]])
        # self.upper  = np.array([["U","U","U"],["U","U","U"],["U","U","U"]])
        # self.left   = np.array([["L","L","L"],["L","L","L"],["L","L","L"]])
        # self.front  = np.array([["F","F","F"],["F","F","F"],["F","F","F"]])
        # self.right  = np.array([["R","R","R"],["R","R","R"],["R","R","R"]])
        # self.back   = np.array([["B","B","B"],["B","B","B"],["B","B","B"]])
        # self.down   = np.array([["D","D","D"],["D","D","D"],["D","D","D"]])
        self.upper  = np.array([["U1","U2","U3"],["U8","U0","U4"],["U7","U6","U5"]])
        self.left   = np.array([["L1","L2","L3"],["L8","L0","L4"],["L7","L6","L5"]])
        self.front  = np.array([["F1","F2","F3"],["F8","F0","F4"],["F7","F6","F5"]])
        self.right  = np.array([["R1","R2","R3"],["R8","R0","R4"],["R7","R6","R5"]])
        self.back   = np.array([["B1","B2","B3"],["B8","B0","B4"],["B7","B6","B5"]])
        self.down   = np.array([["D1","D2","D3"],["D8","D0","D4"],["D7","D6","D5"]])
        self.cube = np.array([self.upper,self.left,self.front,self.right,self.back,self.down])
# make a dictionary to make move functions which can operate on different faces        
        self.which_face = { 0:self.upper, 1:self.left,
        2:self.front, 3:self.right, 4:self.back, 5:self.down }
    
    def print_cube(self):
        print("                  ",self.upper[0])
        print("                  ",self.upper[1])
        print("                  ",self.upper[2])
        print(self.left[0]," ",self.front[0]," ",self.right[0]," ",self.back[0])
        print(self.left[1]," ",self.front[1]," ",self.right[1]," ",self.back[1])
        print(self.left[2]," ",self.front[2]," ",self.right[2]," ",self.back[2])
        print("                  ",self.down[0])
        print("                  ",self.down[1])
        print("                  ",self.down[2])

# methods which rotate corners and sides of a face
# called by self.corners_clockwise(self.front)
    def corners_clockwise(self,f):
        tmp = f[0][0]
        f[0][0] = f[2][0]
        f[2][0] = f[2][2]
        f[2][2] = f[0][2]
        f[0][2] = tmp

    def sides_clockwise(self,f):
        tmp = f[0][1]
        f[0][1] = f[1][0]
        f[1][0] = f[2][1]
        f[2][1] = f[1][2]
        f[1][2] = tmp

    def turn_face(self,clockwise,f):
# here we define an anticlockwise rotation as 3 clockwise rotations
# this is not a full move yet, as we haven't moved the pieces attached to each of those on the face we are moving
        if clockwise == 1:
                n = 1
        elif clockwise == 0:
            n = 3
        else:
            print("value of 'clockwise' should be 1 (for clockwise) or 0 (for anticlockwise)")
        for _ in range(n):
            self.corners_clockwise(f)
            self.sides_clockwise(f)

# Now we can rotate the cube, without doing any moves
    def turn_cube_left(self):
        tmp         = self.left
        self.left   = self.front
        self.front  = self.right
        self.right  = self.back
        self.back   = tmp

        self.turn_face(1,self.upper)
        self.turn_face(0,self.down)

    def turn_cube_down(self):
        tmp        = self.front
        self.front = self.upper
        self.upper = self.back[::-1,::-1]
        self.back  = self.down[::-1,::-1]
        self.down = tmp
        self.turn_face(0,self.right)
        self.turn_face(1,self.left)

# turn to make the a certain face face the user
    def turn_cube(self,f):
        if f is self.front:
            pass
        elif f is self.left:
            for _ in range(3):
                self.turn_cube_left()
        elif f is self.upper:
            self.turn_cube_down()
        elif f is self.down:
            for _ in range(3):
                self.turn_cube_down()
        elif f is self.right:
            self.turn_cube_left()
        elif f is self.back:
            for _ in range(2):
                self.turn_cube_left()
        else:
            print("invalid face to move to")

# this method maps out all the transformations we need to make for the edges attached to the face we're rotating clockwise
    def associated_sides(self,f):
        if f is self.front: # checked
            tmp = list(self.upper[2]) # Need to put this as a list so that changing upper[2] doesn't change tmp
            self.upper[2] = self.left[:,2][::-1] # returns each element that is a multiple of -1 i.e. -1, -2, -3 ... the whole list reversed!
            self.left[:,2] = self.down[0]
            self.down[0] = self.right[:,0][::-1]
            self.right[:,0] = tmp
        elif f is self.upper: # checked
            tmp = list(self.front[0])
            self.front[0] = self.right[0]
            self.right[0] = self.back[0]
            self.back[0] = self.left[0]
            self.left[0] = tmp
        elif f is self.left: # checked
            tmp = list(self.front[:,0])
            self.front[:,0] = self.upper[:,0]
            self.upper[:,0] = self.back[:,2][::-1]
            self.back[:,2][::-1] = self.down[:,0]
            self.down[:,0] = tmp
        elif f is self.down: # checked
            tmp = list(self.front[2])
            self.front[2] = self.left[2]
            self.left[2] = self.back[2]
            self.back[2] = self.right[2]
            self.right[2] = tmp
        elif f is self.right: # checked
            tmp = list(self.front[:,2])
            self.front[:,2] = self.down[:,2]
            self.down[:,2] = self.back[:,0][::-1]
            self.back[:,0][::-1] = self.upper[:,2]
            self.upper[:,2] = tmp
        elif f is self.back:
            tmp = list(self.right[:,2])
            self.right[:,2] = self.down[2][::-1]
            self.down[2] = self.left[:,0]
            self.left[:,0] = self.upper[0][::-1]
            self.upper[0] = tmp


# This method ties them all in together. Clockwise can be either 1 or 0 (yes or no)

# just turn the face, so don't move any of the joined edge pieces

    def rotate_face(self,clockwise,f):
# here we define an anticlockwise rotation as 3 clockwise rotations
        if clockwise == 1:
                n = 1
        elif clockwise == 0:
            n = 3
        else:
            print("value of 'clockwise' should be 1 (for clockwise) or 0 (for anticlockwise)")
        for _ in range(n):
            self.corners_clockwise(f)
            self.sides_clockwise(f)
            self.associated_sides(f)

    def F(self):
        self.rotate_face(1,self.front)

    def U(self):
        self.rotate_face(1,self.upper)
    
    def D(self):
        self.rotate_face(1,self.down)
    
    def R(self):
        self.rotate_face(1,self.right)

    def L(self):
        self.rotate_face(1,self.left)

    def B(self):
        self.rotate_face(1,self.back)



    def f(self):
        self.turn_cube(self.front)

    def u(self):
        self.turn_cube(self.upper)
    
    def d(self):
        self.turn_cube(self.down)
    
    def r(self):
        self.turn_cube(self.right)

    def l(self):
        self.turn_cube(self.left)

    def b(self):
        self.turn_cube(self.back)

x = Cube()
y = Cube()
z = Cube()

x.B()
x.b()
y.b()
y.F()

z.print_cube()
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
x.print_cube()
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
y.print_cube()


# # print(x.upper)
# x.print_cube()
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# x.R()
# x.print_cube()

# print(x.upper[:,2])