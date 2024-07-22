import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Define color options
color_options = {
    'red': (1, 0, 0),
    'green': (0, 1, 0),
    'yellow': (1, 1, 0),
    'blue': (0, 0, 1),
    'cyan': (0, 1, 1),
    'magenta': (1, 0, 1),
    'white': (1, 1, 1),
    'black': (0, 0, 0)
}

# Define speed options
speed_options = {
    '1x': 1,
    '1.5x': 1.5,
    '2x': 2
}

# Prompt user for color selection
def select_color():
    print("Select a color for the cubes:")
    for color in color_options:
        print(f"- {color}")

    chosen_color = input("Enter color (red, green, yellow, blue, cyan, magenta, white, black): ").strip().lower()
    if chosen_color in color_options:
        return color_options[chosen_color]
    else:
        print("Invalid color. Defaulting to red.")
        return color_options['red']

# Prompt user for speed selection
def select_speed():
    print("Select the speed of the cubes:")
    for speed in speed_options:
        print(f"- {speed}")

    chosen_speed = input("Enter speed (1x, 1.5x, 2x): ").strip().lower()
    if chosen_speed in speed_options:
        return speed_options[chosen_speed]
    else:
        print("Invalid speed. Defaulting to 1x.")
        return speed_options['1x']

# Prompt user for cube size
def select_cube_size():
    size = float(input("Enter the size of the cubes (e.g., 1.0, 2.0): ").strip())
    if size <= 0:
        print("Invalid size. Defaulting to 1.0.")
        return 1.0
    return size

# Set the color based on user selection
selected_color = select_color()
colors = [selected_color] * 6  # Apply the selected color to all faces

# Define vertices, edges, and surfaces
base_vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

def set_vertices(size, max_distance, min_distance=-20, camera_x=0, camera_y=0):
    # Scale vertices by the given size
    vertices = [(x * size, y * size, z * size) for x, y, z in base_vertices]

    # Apply random movement
    camera_x = -1 * int(camera_x)
    camera_y = -1 * int(camera_y)

    x_value_change = random.randrange(camera_x - 75, camera_x + 75)
    y_value_change = random.randrange(camera_y - 75, camera_y + 75)
    z_value_change = random.randrange(-1 * max_distance, min_distance)

    new_vertices = []

    for vert in vertices:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices

def Cube(vertices):
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        # Cycle through colors for each surface
        glColor3fv(colors[i % len(colors)])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Get user inputs
    global game_speed
    game_speed = select_speed()
    cube_size = select_cube_size()

    max_distance = 100
    gluPerspective(45, (display[0] / display[1]), 0.1, max_distance)
    glTranslatef(0, 0, -40)

    x_move = 0
    y_move = 0

    cur_x = 0
    cur_y = 0

    direction_speed = 2

    cube_dict = {}
    for x in range(50):
        cube_dict[x] = set_vertices(cube_size, max_distance)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = direction_speed
                if event.key == pygame.K_RIGHT:
                    x_move = -1 * direction_speed
                if event.key == pygame.K_UP:
                    y_move = -1 * direction_speed
                if event.key == pygame.K_DOWN:
                    y_move = direction_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0

        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]

        cur_x += x_move
        cur_y += y_move

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslatef(x_move, y_move, game_speed)

        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])

        for each_cube in cube_dict:
            if camera_z <= cube_dict[each_cube][0][2]:
                new_max = int(-1 * (camera_z - (max_distance * 2)))
                cube_dict[each_cube] = set_vertices(cube_size, new_max, int(camera_z - max_distance), cur_x, cur_y)

        pygame.display.flip()

main()
pygame.quit()
quit()
