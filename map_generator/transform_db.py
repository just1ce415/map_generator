"""
Laboratory 2.2
Transformation DB module (adding coordinates)
One-use module
"""
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

PATH = './../tests/'

if __name__ == '__main__':
    # CONVERT TO LIST
    buffer_lst = []
    geolocator = Nominatim(user_agent='map_generator')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)
    with open(PATH+'locations.list', 'r', encoding='utf-8') as f_locations:
        # SKIPPING USELESS LINES
        for _ in range(14):
            f_locations.readline()
        for line in f_locations:
            # SKIPPING USELESS --- LINES
            if line.startswith('----'):
                continue
            sample_lst = line.split('\t')
            film_name = sample_lst[0]
            film_location = sample_lst[-1][:-1]
            # CHECKING FOR UNEXPECTED ERROR
            try:
                location = geolocator.geocode(film_location)
            except Exception:
                location = None
            # CHECKING IF LOCATION EXISTS
            if location == None:
                continue
            else:
                latitude = str(location.latitude)
                longitude = str(location.longitude)
            buffer_lst.append((film_name, film_location, latitude, longitude))
    # WRITE IN FILE
    with open(PATH+'locations_transformed.tsv', 'w', encoding='utf-8') as f_locations:
        for line in buffer_lst:
            f_locations.write(line[0] + '\t' + line[1] + '\t' + line[2] + '\t' + line[3] + '\n')
