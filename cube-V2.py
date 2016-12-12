import numpy as np

class Cube:
# going to try represent the cube as a 3x3x3 array with piece positions, and colour positions
# i.e. we could have the (x,y,z) = (0,1,0) piece which would have colour (cx,cy,cz) = (R,0,G)
# 2x2x2 case
# positions [ [ [[cx,cy,cz],[cx,xy,cz]], [0,1]], [ [0,1], [0,1] ] ]
# 3x3x3 case positions

    def __init__(self):
        cubie_colour = [0,0,0]
        line = [cubie_colour,cubie_colour,cubie_colour]
        face = [line,line,line]
        cube = [face,face,face]

        cube = np.array(cube)

        for x in range(0,3):
            for y in range(0,3):
                for z in range(0,3):

                    if x == 0:
                        cube[x,y,z,0] = 1
                    elif x == 1:
                        cube[x,y,z,0] = 0
                    elif x == 2:
                        cube[x,y,z,0] = 6

                    if y == 0:
                        cube[x,y,z,1] = 2
                    elif y == 1:
                        cube[x,y,z,1] = 0
                    elif y == 2:
                        cube[x,y,z,1] = 5

                    if z == 0:
                        cube[x,y,z,2] = 3
                    elif z == 1:
                        cube[x,y,z,2] = 0
                    elif z == 2:
                        cube[x,y,z,2] = 4

        print(cube[1,0,1])

c = Cube()
