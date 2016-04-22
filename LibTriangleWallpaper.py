#!/usr/bin/python
import math, numpy, random, copy
from PIL import Image, ImageDraw


class Tessellation:
    def __init__(self, width, height, target_vertices):
        self.vertices = []
        self.width = width
        self.height = height
        # The number of vertices in one row in order to be spread evenly
        self.x_vertices = round(math.sqrt((width * target_vertices) / height)) - 1

        # The number of vertices in each column in order to be spread evenly
        self.y_vertices = round(math.sqrt((height * target_vertices) / width)) - 1
        delta_x = (width - 1) / (self.x_vertices - 1)
        delta_y = (height - 1) / (self.y_vertices - 1)
        for y in numpy.arange(0, self.y_vertices):
            for x in numpy.arange(0, self.x_vertices):
                self.vertices.append((x * delta_x, y * delta_y))


# get a list of colors from an image
def get_image_colors(image: Image, width: float, height: float) -> list:
    return list(image.resize([width, height], Image.LANCZOS).getdata())


def draw_triangle_fan(tes: Tessellation, colors: list) -> Image:
    index = 0
    # result = Image.new("RGB",
    #                    (int(tes.vertices[len(tes.vertices) - 1][0] + 1),
    #                     int(tes.vertices[len(tes.vertices) - 1][1] + 1)))
    result = Image.new("RGB", (tes.width, tes.height))
    draw = ImageDraw.Draw(result)
    for i in range(0, len(tes.vertices) - tes.x_vertices):
        if (i + 1) % tes.x_vertices == 0:
            continue
        draw.polygon([tes.vertices[i], tes.vertices[i + tes.x_vertices], tes.vertices[i + tes.x_vertices + 1]], fill=colors[index])
        index += 1
        draw.polygon([tes.vertices[i], tes.vertices[i + 1], tes.vertices[i + tes.x_vertices + 1]], fill=colors[index])
        index += 1
    del draw
    return result


def randomizeTessellation(tes):
    new_vertices = []
    result = copy.deepcopy(tes)
    for i in range(0, len(tes.vertices)):
        if i < tes.x_vertices:
            new_vertices.append(tes.vertices[i])
        elif i > len(tes.vertices) - tes.x_vertices:
            new_vertices.append(tes.vertices[i])
        elif i % tes.x_vertices == 0:
            new_vertices.append(tes.vertices[i])
        elif (i + 1) % tes.x_vertices == 0:
            new_vertices.append(tes.vertices[i])
        else:
            new_vertices.append((tes.vertices[i][0] - (tes.width / (tes.x_vertices - 1) / 2) + (
            tes.width / (tes.x_vertices - 1)) * random.random() / 2,
                             tes.vertices[i][1] - (tes.height / (tes.y_vertices - 1) / 2) + (
                             tes.height / (tes.y_vertices - 1)) * random.random() / 2))
    result.vertices = new_vertices
    return result


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
