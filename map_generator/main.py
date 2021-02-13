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
    return (year, tuple(coordinates))


def gen_first_layer() -> object:
    '''
    Creates an object Map - first layer for final map.
    '''
    return folium.Map()


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
    return round(2*earth_radius*asin(sqrt(h_check)), 5)


def get_closest_points(year:int, coordinates:tuple) -> list:
    '''
    Returns a sorted by distance list of tuples with info (film_name, location,
    title_coordinates, distance) of first ten films.
    '''
    output_list = []
    with open('./../tests/locations_transformed.tsv', 'r', encoding='iso-8859-1') as f_transformed:
        for line in f_transformed:
            sample_lst = line.split('\t')
            # CHECK IF YEAR IS CORRECT
            if sample_lst[0].find('('+str(year)) == -1 or sample_lst[2] == 'None':
                continue
            title_lat = float(sample_lst[2])
            title_len = float(sample_lst[3][:-1])
            distance = calculate_distance(coordinates[0], coordinates[1], title_lat, title_len)
            output_list.append((sample_lst[0], sample_lst[1], (title_lat, title_len), distance))
    return sorted(output_list, key=lambda x: x[3])[:11]


def gen_second_layer(closests_points:list, custom_map:object) -> object:
    '''
    Creates a second layer (film locations) for final Map, adds it to first layer and returns it.
    '''
    fg = folium.FeatureGroup(name='Film Locations')
    for elem in closests_points:
        fg.add_child(folium.Marker(location=[elem[2][0], elem[2][1]],
        popup=str(elem[0] + ', ' + elem[1]), icon=folium.Icon()))
    custom_map.add_child(fg)
    return custom_map    


def gen_third_layer(custom_map:object) -> object:
    '''
    Creates a third layer (population) for final Map, adds it, and returns it.
    '''
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('./../data/world.json', 'r',
    encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':'green'
    if x['properties']['POP2005'] < 10000000
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
    else 'red'}))
    custom_map.add_child(fg_pp)
    custom_map.add_child(folium.LayerControl())
    return custom_map


if __name__ == '__main__':
    year, coordinates = get_input()
    print('Map is generating...\nPlease wait...')
    generated_map = gen_first_layer()
    film_locations = get_closest_points(year, coordinates)
    generated_map = gen_second_layer(film_locations, generated_map)
    generated_map = gen_third_layer(generated_map)
    generated_map.save(str(year) + '_movies_map.html')
    print('Finished. Please have look at the map ' + str(year) + '_movies_map.html')
