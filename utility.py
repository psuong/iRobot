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


def get_average_line(line1, line2):
    """
    Attempts to get the average line between the actual lane and the predicted lane
    :param line1: four tuple representing the coordinates of a line
    :param line2: four tuple representing the coordinates of a line
    :return: The line between the two lines
    """
    line1_p1 = line1[0]
    line1_p2 = line1[1]

    line2_p1 = line2[0]
    line2_p2 = line2[1]

    average_p1 = int((line1_p1[0] + line2_p1[0]) / 2), int((line1_p1[1] + line2_p1[1]) / 2)
    average_p2 = int((line1_p2[0] + line2_p2[0]) / 2), int((line2_p2[1] + line2_p2[1]) / 2)

    return average_p1, average_p2


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
