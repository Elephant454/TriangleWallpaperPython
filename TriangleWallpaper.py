#!/usr/bin/python
import argparse
import math, numpy, random
from PIL import Image, ImageDraw

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

def genTessellation():
    verts = []
    xdel = (width-1) / (xVerts-1)
    ydel = (height-1) / (yVerts-1)
    for y in numpy.arange(0, yVerts):
        for x in numpy.arange(0, xVerts):
            verts.append((x*xdel, y*ydel))
    return(verts)

def getImageColors(image): #get a list of colors from an image
    return(list(original.resize([(xVerts-1)*2,yVerts-1], Image.LANCZOS).getdata()))

def drawTriangleFan(verts, colors):
    index = 0
    result = Image.new("RGB", (original.width, original.height))
    draw = ImageDraw.Draw(result)
    for i in range(0, len(verts)-xVerts):
        if (i+1)%xVerts == 0: continue
        draw.polygon([verts[i], verts[i+xVerts], verts[i+xVerts+1]], fill=colors[index])
        index += 1
        draw.polygon([verts[i], verts[i+1], verts[i+xVerts+1]], fill=colors[index])
        index += 1
    del draw
    return(result)

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

def distance(a, b):
    return(math.sqrt(((b[0]-a[0])**2) + ((b[1]-a[1])**2)))

def pullTessellation(center, verts):
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

            print("X: " + (str)(verts[i][0]) + " + (" + (str)(verts[center][0]) + " - " + (str)(verts[i][0]) + ") = " + (str)(verts[i][0] + (verts[center][0] - verts[i][0])/3))
            print("Y: " + (str)(verts[i][1]) + " + (" + (str)(verts[center][1]) + " - " + (str)(verts[i][1]) + ") = " + (str)(verts[i][1] + (verts[center][1] - verts[i][1])/3))
            result.append((verts[i][0] + (verts[center][0] - verts[i][0]), verts[i][1] + (verts[center][1] - verts[i][1])))

    return(result)


#gen = genTessellation()
#for i in range(0, 10):
#    gen = randomizeTessellation(gen)
#drawTriangleFan(gen)

#tes = genTessellation()
#center = round(random.random()*len(tes))
#drawTriangleFan(pullTessellation(center, tes)).show()

drawTriangleFan(randomizeTessellation(genTessellation()), getImageColors(original)).save("output." + original.filename.rpartition('.')[2], original.format)
