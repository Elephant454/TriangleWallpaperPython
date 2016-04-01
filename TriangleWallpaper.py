#!/usr/bin/python
import argparse, math
from PIL import Image
import LibTriangleWallpaper as ltw

parser = argparse.ArgumentParser(description="Turn an image into triangles.")
parser.add_argument("file", type=open, help="image file to turn into triangles")
parser.add_argument("-v", type=int, default=2048, metavar="verticies", help="number of verticies that the picture should aim to have (default is 2048)")
args = parser.parse_args()

original = Image.open(args.file.name)
#original = Image.open("fenstack.jpg")

width = original.width
height = original.height
targetVerts = args.v #The number of verticies to aim for. The actual number may be less.
#targetVerts = 2048 #The number of verticies to aim for. The actual number may be less.
xVerts = (round(math.sqrt((width*targetVerts)/height))-1) #The number of verticies in one row in order to be spread evenly
yVerts = (round(math.sqrt((height*targetVerts)/width))-1) #The number of verticies in each column in order to be spread evenly

tes = ltw.Tessellation(original.width, original.height, targetVerts)
print(len(tes.verts))
ltw.randomizeTessellation(tes)
print(len(tes.verts))
ltw.drawTriangleFan(tes, ltw.getImageColors(original, (xVerts-1)*2, (yVerts-1))).save("output." + original.filename.rpartition('.')[2], original.format)
