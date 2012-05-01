# create a Lumpy object and capture reference state
import Lumpy
lumpy = Lumpy.Lumpy()
lumpy.make_reference()

# run the test code
x = [1, 2, 3]
y = x
z = list(x)

# draw the current state (relative to the last ref)
lumpy.object_diagram()
