"""
Laboratory 2.2
Main module
GitHub: https://github.com/just1ce415/map_generator.git
"""
import folium
from math import sin, cos, sqrt, asin

earth_radius = 6371.0

def get_input() -> tuple:
    '''
    Gets year and coordinated from user and checks it. Returns None, if smth's wrong.
    '''
    year = input('Please enter a year you would like to have a map for: ')
    coordinates = input('Please enter your location (format: lat, long): ').split(', ')
    try:
        year = int(year)
        assert len(coordinates) == 2
        coordinates[0] = float(coordinates[0])
        coordinates[1] = float(coordinates[1])
    except ValueError:
        return None
    except AssertionError:
        return None
    return (year, coordinates)


def gen_first_layer():
    pass


def calculate_distance(x_cor1:float, y_cor1:float, x_cor2:float, y_cor2:float) -> float:
    '''
    Calculates distance between 1 and 2 points with haversinus formula.
    '''
    h_check = ((sin((x_cor2-x_cor1) / 2))**2 + cos(x_cor1)*cos(x_cor2) *
    (sin((y_cor2-y_cor1) / 2))**2)
    # CHECKUNG IF H MAKES SENSE
    try:
        assert 0 < h_check < 1
    except AssertionError:
        return None
    return round(2*earth_radius*asin(sqrt(h_check), 5))


def get_closest_points(arg):
    '''
    '''
    pass


def gen_second_layer():
    pass


def gen_third_layer(arg):
    '''
    '''
    pass


if __name__ == '__main__':
    with open('./map_generator/map_generator/tests/locations.list', 'r', encoding='utf-8') as f_locations:
        for line in f_locations:
            lst = line.split('\t')
