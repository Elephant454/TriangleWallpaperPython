#!/usr/bin/python
import argparse
import copy
import math
import numpy
import random

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
    result = Image.new("RGB", (tes.width, tes.height))
    draw = ImageDraw.Draw(result)
    for i in range(0, len(tes.vertices) - tes.x_vertices):
        if (i + 1) % tes.x_vertices == 0:
            continue
        draw.polygon([tes.vertices[i], tes.vertices[i + tes.x_vertices], tes.vertices[i + tes.x_vertices + 1]],
                     fill=colors[index])
        index += 1
        draw.polygon([tes.vertices[i], tes.vertices[i + 1], tes.vertices[i + tes.x_vertices + 1]], fill=colors[index])
        index += 1
    del draw
    return result


def randomize_tessellation(tes):
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
            new_vertices.append((tes.vertices[i][0] - (tes.width / (tes.x_vertices - 1) / 2) +
                                 (tes.width / (tes.x_vertices - 1)) * random.random() / 2,
                                 tes.vertices[i][1] - (tes.height / (tes.y_vertices - 1) / 2) +
                                 (tes.height / (tes.y_vertices - 1)) * random.random() / 2))
    result.vertices = new_vertices
    return result


def distance(a, b):
    return math.sqrt(((b[0] - a[0]) ** 2) + ((b[1] - a[1]) ** 2))


def pull_tessellation(tes: Tessellation, center: tuple):
    result = []
    for i in range(0, len(tes.vertices)):
        if i < tes.vertices:
            result.append(tes.vertices[i])
        elif i > len(tes.vertices) - tes.x_vertices:
            result.append(tes.vertices[i])
        elif i % tes.x_vertices == 0:
            result.append(tes.vertices[i])
        elif (i + 1) % tes.x_vertices == 0:
            result.append(tes.vertices[i])
        else:

            print(
                "X: " + str(tes.vertices[i][0]) + " + (" + str(tes.vertices[center][0]) + " - " +
                str(tes.vertices[i][0]) + ") = " + str(tes.vertices[i][0] +
                                                       (tes.vertices[center][0] - tes.vertices[i][0]) / 3))
            print(
                "Y: " + str(tes.vertices[i][1]) + " + (" + str(tes.vertices[center][1]) + " - " +
                str(tes.vertices[i][1]) + ") = " + str(tes.vertices[i][1] +
                                                       (tes.vertices[center][1] - tes.vertices[i][1]) / 3))
            result.append(
                (tes.vertices[i][0] + (tes.vertices[center][0] - tes.vertices[i][0]), tes.vertices[i][1] +
                 (tes.vertices[center][1] - tes.vertices[i][1])))

    return result


# if the module is ran as a script, it will take arguments and produce output
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turn an image into triangles.")
    parser.add_argument("file", type=open, help="image file to turn into triangles")
    parser.add_argument("-v", type=int, default=2048, metavar="vertices",
                        help="number of vertices that the picture should aim to have (default is 2048)")
    parser.add_argument("--no-randomization", dest="randomize", action="store_false", help="don't randomize vertices")
    args = parser.parse_args()

    original = Image.open(args.file.name)

    width = original.width
    height = original.height

    # The number of vertices to aim for. The actual number may be less.
    targetVerts = args.v

    # The number of vertices in each row or column in order to be spread vertices evenly
    xVerts = (round(math.sqrt((width*targetVerts)/height))-1)
    yVerts = (round(math.sqrt((height*targetVerts)/width))-1)

    tes = Tessellation(original.width, original.height, targetVerts)
    if args.randomize:
        tes = randomize_tessellation(tes)
    draw_triangle_fan(tes, get_image_colors(original, (xVerts - 1) * 2, (yVerts - 1))).save(
        "output." + original.filename.rpartition('.')[2], original.format)
