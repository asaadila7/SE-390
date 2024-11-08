# https://gist.github.com/GrantTrebbin/5382bc3c815a933dbd22d3a1881fa334

# There may be a warning that model isn't closed. Most likely this is an error
# caused by the way numpy-stl tests the model. This usually only happens on
# models with a large number of faces. Ignore this warning but check the model
# to be sure.

import numpy as np
from stl import mesh
from typing import NamedTuple, List


# Simple coordinate storage class
class Vertex(NamedTuple):
    x: float
    y: float
    z: float


def create_mesh(heights, x_vals, y_vals, outfile, scale_factor=1):

    y_number_of_points, x_number_of_points = heights.shape
    number_of_top_faces = (x_number_of_points - 1) * (y_number_of_points - 1) * 2

    total_number_of_faces = number_of_top_faces * 2 + 4 * (
        y_number_of_points + x_number_of_points - 2
    )

    # Storage for vertex coordinates using the x and y index of the coordinates
    top_vertices = dict()
    bottom_vertices = dict()

    # Create the vertices for the top and bottom surfaces
    for y_index in range(y_number_of_points):
        for x_index in range(x_number_of_points):
            # x_coord = x_index * x_spacing
            # y_coord = y_index * y_spacing

            # Create the vertices for the top surface. These are defined by
            # surface_function
            top_vertices[(x_index, y_index)] = Vertex(
                x_vals[y_index, x_index],
                y_vals[y_index, x_index],
                heights[y_index, x_index],
            )

            # Create the vertices for the bottom flat surface at z = 0
            bottom_vertices[(x_index, y_index)] = Vertex(
                x_vals[y_index, x_index], y_vals[y_index, x_index], 0
            )

    # Preallocate storage for the triangles that make up the upper and lower faces.
    # I've chosen to preallocate storage for the face data instead of constantly
    # growing the list. It shouldn't make a difference for models with a small
    # number of faces, but it seems to improve speed for larger models.
    top_faces: List[tuple or None] = [None] * (
        (x_number_of_points - 1) * (y_number_of_points - 1) * 2
    )
    bottom_faces: List[tuple or None] = [None] * (
        (x_number_of_points - 1) * (y_number_of_points - 1) * 2
    )

    counter = 0
    for y_index in range(y_number_of_points - 1):
        for x_index in range(x_number_of_points - 1):

            # Add faces for the top surface by adding the coordinates of three
            # vertices to a tuple
            top_faces[counter * 2] = (
                top_vertices[x_index, y_index],
                top_vertices[x_index + 1, y_index + 1],
                top_vertices[x_index, y_index + 1],
            )
            top_faces[counter * 2 + 1] = (
                top_vertices[x_index, y_index],
                top_vertices[x_index + 1, y_index],
                top_vertices[x_index + 1, y_index + 1],
            )

            # Add faces for the bottom surface
            bottom_faces[counter * 2] = (
                bottom_vertices[x_index, y_index],
                bottom_vertices[x_index, y_index + 1],
                bottom_vertices[x_index + 1, y_index + 1],
            )
            bottom_faces[counter * 2 + 1] = (
                bottom_vertices[x_index, y_index],
                bottom_vertices[x_index + 1, y_index + 1],
                bottom_vertices[x_index + 1, y_index],
            )

            counter += 1

    # Add faces along the edge of the model to close it. These faces are parallel
    # to the x-axis
    x_faces_1: List[tuple or None] = [None] * ((x_number_of_points - 1) * 2)
    x_faces_2: List[tuple or None] = [None] * ((x_number_of_points - 1) * 2)

    counter = 0
    for x_index in range(x_number_of_points - 1):

        x_faces_1[counter * 2] = (
            top_vertices[x_index, 0],
            bottom_vertices[x_index, 0],
            bottom_vertices[x_index + 1, 0],
        )
        x_faces_2[counter * 2] = (
            top_vertices[x_index, y_number_of_points - 1],
            bottom_vertices[x_index + 1, y_number_of_points - 1],
            bottom_vertices[x_index, y_number_of_points - 1],
        )

        x_faces_1[counter * 2 + 1] = (
            top_vertices[x_index + 1, 0],
            top_vertices[x_index, 0],
            bottom_vertices[x_index + 1, 0],
        )
        x_faces_2[counter * 2 + 1] = (
            top_vertices[x_index, y_number_of_points - 1],
            top_vertices[x_index + 1, y_number_of_points - 1],
            bottom_vertices[x_index + 1, y_number_of_points - 1],
        )
        counter += 1

    # Add faces along the edge of the model to close it. These faces are parallel
    # to the y-axis
    y_faces_1: List[tuple or None] = [None] * ((y_number_of_points - 1) * 2)
    y_faces_2: List[tuple or None] = [None] * ((y_number_of_points - 1) * 2)

    counter = 0
    for y_index in range(y_number_of_points - 1):

        y_faces_1[counter * 2] = (
            top_vertices[0, y_index],
            bottom_vertices[0, y_index + 1],
            bottom_vertices[0, y_index],
        )
        y_faces_2[counter * 2] = (
            top_vertices[x_number_of_points - 1, y_index],
            bottom_vertices[x_number_of_points - 1, y_index],
            bottom_vertices[x_number_of_points - 1, y_index + 1],
        )

        y_faces_1[counter * 2 + 1] = (
            top_vertices[0, y_index],
            top_vertices[0, y_index + 1],
            bottom_vertices[0, y_index + 1],
        )
        y_faces_2[counter * 2 + 1] = (
            top_vertices[x_number_of_points - 1, y_index + 1],
            top_vertices[x_number_of_points - 1, y_index],
            bottom_vertices[x_number_of_points - 1, y_index + 1],
        )
        counter += 1

    # Combine all the faces
    all_faces = top_faces + bottom_faces + x_faces_1 + x_faces_2 + y_faces_1 + y_faces_2
    model = mesh.Mesh(np.zeros(total_number_of_faces * 4, dtype=mesh.Mesh.dtype))

    # Create the model
    for index, face in enumerate(all_faces):
        for vertex_index in range(3):
            model.vectors[index][vertex_index] = np.array(
                [
                    face[vertex_index].x * scale_factor,
                    face[vertex_index].y * scale_factor,
                    face[vertex_index].z * scale_factor,
                ]
            )

    # Save the model
    model.save(outfile)
