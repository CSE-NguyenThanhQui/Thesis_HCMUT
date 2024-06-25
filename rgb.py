from PIL import Image
import numpy
img= Image.open("90.png")
np_array_img = numpy.array(img)
print(np_array_img)