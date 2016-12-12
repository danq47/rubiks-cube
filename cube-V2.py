import numpy as np

class Cube:
# We will represent the cube as a numpy array where we can access each
# individual cubie by cube[x,y,z]. This will return us a colour vector [cx,cy,cz]
# which tells us the colour in the x,y,z directions (numbered
# 1-6, and 0 for no colour, as in the cx colour on the upper face)
# Only issue so far is it's unclear how this corresponds to a solved/unsolved cube
# it's not clear to see. Maybe we can just have a mapping to our old way of showing this
    def __init__(self):
        self.cubie_colour = [0,0,0] # this will be the colour vector at each cubie point, start it off empty (as zeros)
        self.line = [self.cubie_colour,self.cubie_colour,self.cubie_colour]
        self.face = [self.line,self.line,self.line] 
        self.cube = [self.face,self.face,self.face] # build up the cube

        self.cube = np.array(self.cube) # np array is easier to navigate

# next we need to set the colour vectors
        for x in range(0,3):
            for y in range(0,3):
                for z in range(0,3):

                    if x == 0:
                        self.cube[x,y,z,0] = 1
                    elif x == 1:
                        self.cube[x,y,z,0] = 0
                    elif x == 2:
                        self.cube[x,y,z,0] = 6

                    if y == 0:
                        self.cube[x,y,z,1] = 2
                    elif y == 1:
                        self.cube[x,y,z,1] = 0
                    elif y == 2:
                        self.cube[x,y,z,1] = 5

                    if z == 0:
                        self.cube[x,y,z,2] = 3
                    elif z == 1:
                        self.cube[x,y,z,2] = 0
                    elif z == 2:
                        self.cube[x,y,z,2] = 4


c = Cube()
print(c.cube[1,1,0])
