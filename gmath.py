import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The first index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#variable definitions
    # A: The color of ambient light (RGB or a single value [0-255])
        # e.g. 255, 255, 255 (white)
    # P: The color of a point light source (RGB or a single value [0-255])
        # e.g. 255, 0, 255 (magenta)
        # light's second index COLOR
    # Vector L: The vector from the surface of an object to a point light source ( <x, y, z> ).
        # e.g. 1, 0.5, 1 (to the right, slightly up and in front)
        # light's first index LOCATION
    # Vector V: The view vector (from the surface of an object to the viewer) ( <x, y, z> ).
        # e.g. 0, 0, 1 (directly in front)
    # Vector N: The surface normal of a polygon, see notes on backface culling for more on this.
    # Ka: Constant of ambient reflection; how much ambient light is reflected by the object. ( RGB or a single value [0-1], think of it like a %).
        # e.g. 0.1, 0.1, 0.1
    # Kd: Constant of diffuse reflection; how much a point light is reflected diffusely by the object. ( RGB or a single value [0-1] ).
        # e.g. 0.5, 0.5, 0.5
    # Ks: Constant of specular reflection; how much a point light is reflected specularly by the object. ( RGB or a single value [0-1] ).
        # e.g. 0.5, 0.5, 0.5
    # In general, I (for illumination), or the color of an object based on lighting will be calculated by:
        # I = Iambient + Idiffuse + Ispecular

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    Ia = calculate_ambient(ambient, areflect)
    Id = calculate_diffuse(light, dreflect, normal)
    Is = calculate_specular(light, sreflect, view, normal)
    color = [
        int(Ia[0] + Id[0] + Is[0]),
        int(Ia[1] + Id[1] + Is[1]),
        int(Ia[2] + Id[2] + Is[2])
    ]
    # limit_color(color)
    return color

def calculate_ambient(alight, areflect):
    Ia = [
        alight[0] * areflect[0],
        alight[1] * areflect[1],
        alight[2] * areflect[2]
    ]
    return limit_color(Ia)

def calculate_diffuse(light, dreflect, normal):
    normalize(normal)
    normalize(light[LOCATION])
    prod = dot_product(normal, light[LOCATION])
    Id = [
        light[COLOR][0] * dreflect[0] * prod,
        light[COLOR][1] * dreflect[1] * prod,
        light[COLOR][2] * dreflect[2] * prod
    ]
    return limit_color(Id)

def calculate_specular(light, sreflect, view, normal):
    normalize(normal)
    normalize(light[LOCATION])
    prod = dot_product(normal, light[LOCATION])
    vecR = [
        2 * normal[0] * prod - light[LOCATION][0],
        2 * normal[1] * prod - light[LOCATION][1],
        2 * normal[2] * prod - light[LOCATION][2]
    ]
    normalize(view)
    normalize(vecR)
    cosAlpha = dot_product(vecR, view)
    Is = [
        light[COLOR][0] * sreflect[0] * cosAlpha,
        light[COLOR][1] * sreflect[1] * cosAlpha,
        light[COLOR][2] * sreflect[2] * cosAlpha
    ]
    return limit_color(Is)

def limit_color(color):
    for i in range(3):
        color[i] = int(color[i])
        if color[i] > 255: # should be very bright --> max is 255
            color[i] = 255
        if color[i] < 0: # should be very dark --> min is 0
            color[i] = 0
    return color

#vector functions
#normalize vector, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
