import math


def does_module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    return True


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [int(x), int(y)]


def distance(start, end):
    """
    Computes the distance between 2 points on the image
    :param start: The "from" vector
    :param end: The "to" vector
    :return: Magnitude
    """
    x_squared = math.pow(end[0] - start[0], 2)
    y_squared = math.pow(end[1] - start[1], 2)
    return math.sqrt(x_squared + y_squared)
