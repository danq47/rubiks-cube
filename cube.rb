# We're working in a flattened out cube arranged as below
#  U
# LFRB
#  D
class Cube

  def initialize
# initialise a solved cube
    # @upper  = [[1 ,2 ,3 ],[4 ,"U",5 ],[6 ,7 ,8 ]]
    # @left   = [[9 ,10,11],[12,"L",13],[14,15,16]]
    # @front  = [[17,18,19],[20,"F",21],[22,23,24]]
    # @right  = [[25,26,27],[28,"R",29],[30,31,32]]
    # @back   = [[33,34,35],[36,"B",37],[38,39,40]]
    # @down   = [[41,42,43],[44,"D",45],[46,47,48]]
    @upper  = [["U1","U2","U3"],["U4","UC","U5"],["U6","U7","U8"]]
    @left   = [["L1","L2","L3"],["L4","LC","L5"],["L6","L7","L8"]]
    @front  = [["F1","F2","F3"],["F4","FC","F5"],["F6","F7","F8"]]
    @right  = [["R1","R2","R3"],["R4","RC","R5"],["R6","R7","R8"]]
    @back   = [["B1","B2","B3"],["B4","BC","B5"],["B6","B7","B8"]]
    @down   = [["D1","D2","D3"],["D4","DC","D5"],["D6","D7","D8"]]
    @cube   = [@upper,@left,@front,@right,@back,@down]
# make a hash so we can call moves on faces numbered 0-5
    @which_face = Hash[ 0 => @upper,1 => @left,
    2 => @front,3 => @right,4 => @back,5 => @down]
  end

  def print_cube
    p ["              "]+@upper[0]
    p ["              "]+@upper[1]
    p ["              "]+@upper[2]
    p @left[0]+@front[0]+@right[0]+@back[0]
    p @left[1]+@front[1]+@right[1]+@back[1]
    p @left[2]+@front[2]+@right[2]+@back[2]
    p ["              "]+@down[0]
    p ["              "]+@down[1]
    p ["              "]+@down[2]
  end

  def clockwise_upper

    # @upper = clockwise[@upper]

  end

  def corners_clockwise(input)
    face = @which_face[input]

    tmp = face[0][2]
    face[0][2] = face[0][0]
    face[0][0] = face[2][0]
    face[2][0] = face[2][2]
    face[2][2] = tmp
  end

  def sides_clockwise(input)
    face = @which_face[input]

    tmp = face[0][1]
    face[0][1] = face[1][0]
    face[1][0] = face[2][1]
    face[2][1] = face[1][2]
    face[1][2] = tmp
  end

end

# # Now I want to make a class of moves
# class Move

#   def upper_clockwise


c = Cube.new
c.print_cube
c.corners_clockwise(0)
p "~"*40
c.print_cube
c.sides_clockwise(0)
p "~"*40
c.print_cube