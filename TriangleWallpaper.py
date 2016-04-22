#!/usr/bin/python
import argparse, math
from PIL import Image
from LibTriangleWallpaper import Tessellation, get_image_colors, randomizeTessellation, draw_triangle_fan

parser = argparse.ArgumentParser(description="Turn an image into triangles.")
parser.add_argument("file", type=open, help="image file to turn into triangles")
parser.add_argument("-v", type=int, default=2048, metavar="verticies",
                    help="number of verticies that the picture should aim to have (default is 2048)")
args = parser.parse_args()

original = Image.open(args.file.name)
#original = Image.open("fenstack.jpg")

width = original.width
height = original.height

# The number of vertices to aim for. The actual number may be less.
targetVerts = args.v
#targetVerts = 2048

# The number of vertices in each row or column in order to be spread vertices evenly
xVerts = (round(math.sqrt((width*targetVerts)/height))-1)
yVerts = (round(math.sqrt((height*targetVerts)/width))-1)

tes = Tessellation(original.width, original.height, targetVerts)
print(len(tes.vertices))
tes = randomizeTessellation(tes)
print(len(tes.vertices))
draw_triangle_fan(tes, get_image_colors(original, (xVerts - 1) * 2, (yVerts - 1))).save(
    "output." + original.filename.rpartition('.')[2], original.format)
