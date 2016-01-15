#!/usr/bin/python
import argparse
import math, numpy, random
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description="Turn an image into triangles.")
parser.add_argument("file", type=open, help="image file to turn into triangles")
parser.add_argument("-v", type=int, default=2048, metavar="verticies", help="number of verticies that the picture should aim to have")
args = parser.parse_args()

original = Image.open(args.file.name)
new = Image.new("RGB", (original.width, original.height))

width = original.width
height = original.height
targetVerts = args.v
xVerts = (round(math.sqrt((width*targetVerts)/height))-1)
yVerts = (round(math.sqrt((height*targetVerts)/width))-1)

def genTessellation():
    verts = []
    xdel = (width-1) / (xVerts-1)
    ydel = (height-1) / (yVerts-1)
    for y in numpy.arange(0, yVerts):
        for x in numpy.arange(0, xVerts):
            verts.append((x*xdel, y*ydel))
    return(verts)

def drawTriangleFan(verts):
    index = 0
    colors = list(original.resize([(xVerts-1)*2,yVerts-1], Image.LANCZOS).getdata())
    draw = ImageDraw.Draw(new)
    for i in range(0, len(verts)-xVerts):
        if (i+1)%xVerts == 0: continue
        draw.polygon([verts[i], verts[i+xVerts], verts[i+xVerts+1]], fill=colors[index])
        index += 1
        draw.polygon([verts[i], verts[i+1], verts[i+xVerts+1]], fill=colors[index])
        index += 1
    del draw

def randomizeTessellation(verts):
    result = []
    for i in range(0, len(verts)):
        if i<xVerts:
            result.append(verts[i])
        elif i>len(verts)-xVerts:
            result.append(verts[i])
        elif i%xVerts == 0:
            result.append(verts[i])
        elif (i+1)%xVerts == 0:
            result.append(verts[i])
        else:
            result.append((verts[i][0] - (width/(xVerts-1)/2) + (width/(xVerts-1))*random.random()/2, verts[i][1] - (height/(yVerts-1)/2) + (height/(yVerts-1))*random.random()/2))
    return(result)


drawTriangleFan(randomizeTessellation(genTessellation()))
gen = genTessellation()
#for i in range(0, 10):
#    gen = randomizeTessellation(gen)
#drawTriangleFan(gen)
new.save("output." + original.filename.rpartition('.')[2], original.format)
