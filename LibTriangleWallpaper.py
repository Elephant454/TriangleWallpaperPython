#!/usr/bin/python
import math, numpy, random, copy
from PIL import Image, ImageDraw


class Tessellation:
    def __init__(self, width, height, target_verts):
        self.verts = []
        self.width = width
        self.height = height
        # The number of vertices in one row in order to be spread evenly
        self.xVerts = round(math.sqrt((width * target_verts) / height)) - 1

        # The number of vertices in each column in order to be spread evenly
        self.yVerts = round(math.sqrt((height * target_verts) / width)) - 1
        xdel = (width - 1) / (self.xVerts - 1)
        ydel = (height - 1) / (self.yVerts - 1)
        for y in numpy.arange(0, self.yVerts):
            for x in numpy.arange(0, self.xVerts):
                self.verts.append((x * xdel, y * ydel))


def get_image_colors(image, width, height):  # get a list of colors from an image
    return list(image.resize([width, height], Image.LANCZOS).getdata())


def draw_triangle_fan(tes: Tessellation, colors: object) -> object:
    index = 0
    result = Image.new("RGB", (int(tes.verts[len(tes.verts) - 1][0] + 1), int(tes.verts[len(tes.verts) - 1][1] + 1)))
    draw = ImageDraw.Draw(result)
    for i in range(0, len(tes.verts) - tes.xVerts):
        if (i + 1) % tes.xVerts == 0: continue
        draw.polygon([tes.verts[i], tes.verts[i + tes.xVerts], tes.verts[i + tes.xVerts + 1]], fill=colors[index])
        index += 1
        draw.polygon([tes.verts[i], tes.verts[i + 1], tes.verts[i + tes.xVerts + 1]], fill=colors[index])
        index += 1
    del draw
    return result


def randomizeTessellation(tes):
    newVerts = []
    result = copy.deepcopy(tes)
    for i in range(0, len(tes.verts)):
        if i < tes.xVerts:
            newVerts.append(tes.verts[i])
            True
        elif i > len(tes.verts) - tes.xVerts:
            newVerts.append(tes.verts[i])
            True
        elif i % tes.xVerts == 0:
            newVerts.append(tes.verts[i])
            True
        elif (i + 1) % tes.xVerts == 0:
            newVerts.append(tes.verts[i])
            True
        else:
            newVerts.append((tes.verts[i][0] - (tes.width / (tes.xVerts - 1) / 2) + (
            tes.width / (tes.xVerts - 1)) * random.random() / 2,
                             tes.verts[i][1] - (tes.height / (tes.yVerts - 1) / 2) + (
                             tes.height / (tes.yVerts - 1)) * random.random() / 2))
    result.verts = newVerts
    return (result)


def distance(a, b):
    return (math.sqrt(((b[0] - a[0]) ** 2) + ((b[1] - a[1]) ** 2)))


def pullTessellation(center, verts):
    result = []
    for i in range(0, len(verts)):
        if i < xVerts:
            result.append(verts[i])
        elif i > len(verts) - xVerts:
            result.append(verts[i])
        elif i % xVerts == 0:
            result.append(verts[i])
        elif (i + 1) % xVerts == 0:
            result.append(verts[i])
        else:

            print(
                "X: " + (str)(verts[i][0]) + " + (" + (str)(verts[center][0]) + " - " + (str)(verts[i][0]) + ") = " + (
                str)(verts[i][0] + (verts[center][0] - verts[i][0]) / 3))
            print(
                "Y: " + (str)(verts[i][1]) + " + (" + (str)(verts[center][1]) + " - " + (str)(verts[i][1]) + ") = " + (
                str)(verts[i][1] + (verts[center][1] - verts[i][1]) / 3))
            result.append(
                (verts[i][0] + (verts[center][0] - verts[i][0]), verts[i][1] + (verts[center][1] - verts[i][1])))

    return (result)

# gen = genTessellation()
# for i in range(0, 10):
#    gen = randomizeTessellation(gen)
# drawTriangleFan(gen)

# tes = genTessellation()
# center = round(random.random()*len(tes))
# drawTriangleFan(pullTessellation(center, tes)).show()

# drawTriangleFan(randomizeTessellation(genTessellation(original.width, original.height, targetVerts)), getImageColors(original)).save("output." + original.filename.rpartition('.')[2], original.format)
