import math

def rectangle(length, width):
    area = length * width
    perimeter = 2 * (length + width)
    diagonal = math.sqrt(length**2 + width**2)
    return round(area, 2), round(perimeter, 2), round(diagonal, 2)

def square(side):
    area = side * side
    perimeter = 4 * side
    diagonal = side * math.sqrt(2)
    return round(area, 2), round(perimeter, 2), round(diagonal, 2)

def triangle(base, height, side1, side2):
    area = 0.5 * base * height
    perimeter = base + side1 + side2
    return round(area, 2), round(perimeter, 2)

def circle(radius):
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    diameter = 2 * radius
    return round(area, 2), round(circumference, 2), round(diameter, 2)

def ellipse(major_axis, minor_axis):
    a = major_axis / 2
    b = minor_axis / 2
    area = math.pi * a * b
    perimeter = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
    return round(area, 2), round(perimeter, 2)

def rhombus(side, diagonal1, diagonal2):
    area = 0.5 * diagonal1 * diagonal2
    perimeter = 4 * side
    return round(area, 2), round(perimeter, 2)

def trapezium(base_a, base_b, side_c, side_d, height):
    area = 0.5 * (base_a + base_b) * height
    perimeter = base_a + base_b + side_c + side_d
    return round(area, 2), round(perimeter, 2)

def pentagon(side):
    area = 0.25 * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * side ** 2
    perimeter = 5 * side
    return round(area, 2), round(perimeter, 2)

def hexagon(side):
    area = (3 * math.sqrt(3) / 2) * side ** 2
    perimeter = 6 * side
    return round(area, 2), round(perimeter, 2)

def cube(side):
    surface_area = 6 * side ** 2
    volume = side ** 3
    diagonal = side * math.sqrt(3)
    return round(surface_area, 2), round(volume, 2), round(diagonal, 2)

def cuboid(length, width, height):
    surface_area = 2 * (length * width + width * height + length * height)
    volume = length * width * height
    diagonal = math.sqrt(length ** 2 + width ** 2 + height ** 2)
    return round(surface_area, 2), round(volume, 2), round(diagonal, 2)

def cylinder(radius, height):
    surface_area = 2 * math.pi * radius * (radius + height)
    curved_surface_area = 2 * math.pi * radius * height
    volume = math.pi * radius ** 2 * height
    return round(surface_area, 2), round(curved_surface_area, 2), round(volume, 2)

def cone(radius, height):
    slant_height = math.sqrt(radius ** 2 + height ** 2)
    surface_area = math.pi * radius * (radius + slant_height)
    volume = (1 / 3) * math.pi * radius ** 2 * height
    return round(surface_area, 2), round(slant_height, 2), round(volume, 2)

def sphere(radius):
    surface_area = 4 * math.pi * radius ** 2
    volume = (4 / 3) * math.pi * radius ** 3
    return round(surface_area, 2), round(volume, 2)
