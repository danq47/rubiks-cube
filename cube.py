class Cube:

# initialize a full cube

    def __init__(self):
        self.upper  = [[1 ,2 ,3 ],[4 ,"U",5 ],[6 ,7 ,8 ]]
        self.left   = [[9 ,10,11],[12,"L",13],[14,15,16]]
        self.front  = [[17,18,19],[20,"F",21],[22,23,24]]
        self.right  = [[25,26,27],[28,"R",29],[30,31,32]]
        self.back   = [[33,34,35],[36,"B",37],[38,39,40]]
        self.down   = [[41,42,43],[44,"D",45],[46,47,48]]

# make a dictionary to make move functions which can operate on different faces        
        self.which_face = { 0:self.upper, 1:self.left,
        2:self.front, 3:self.right, 4:self.back, 5:self.down }
    def print_cube(self):
        print("              ","\t",self.upper[0])
        print("              ","\t",self.upper[1])
        print("              ","\t",self.upper[2])
        print(self.left[0],"\t",self.front[0],"\t",self.right[0],"\t",self.back[0])
        print(self.left[1],"\t",self.front[1],"\t",self.right[1],"\t",self.back[1])
        print(self.left[2],"\t",self.front[2],"\t",self.right[2],"\t",self.back[2])
        print("              ","\t",self.down[0])
        print("              ","\t",self.down[1])
        print("              ","\t",self.down[2])

    def r1(self):
        tmp = self.upper[0][0]
        self.upper[0][0] = self.upper[0][1]
        self.upper[0][1] = tmp

    def corners_clockwise(self,face):
        if face == 1:
            f=self.upper
        return f[0][0]



    def F(self):
# this will be the rotation of the front face by 90^ clockwise
        self.corners_clockwise(self.front)
        self.sides_clockwise(self.front)


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

x = Cube()

# print(x.upper)
x.print_cube()
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
x.F()
x.print_cube()