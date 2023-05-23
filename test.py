from PIL import Image, ExifTags

img = Image.open("sample.jpg")
img_exif = img.getexif()
print(type(img_exif))
# <class 'PIL.Image.Exif'>

if img_exif is None:
    print('Sorry, image has no exif data.')
else:
    for key, val in img_exif.items():
        if key in ExifTags.TAGS:
            print(f'{ExifTags.TAGS[key]}:{val}')
            # ExifVersion:b'0230'
            # ...
            # FocalLength:(2300, 100)
            # ColorSpace:1
            # ...
            # Model:'X-T2'
            # Make:'FUJIFILM'
            # LensSpecification:(18.0, 55.0, 2.8, 4.0)
            # ...
            # DateTime:'2019:12:01 21:30:07'
            # ...
        else:
            print(key,val)

'''
GPSINFO_TAG = next(
    tag for tag, name in ExifTags.TAGS.items() if name == "GPSInfo"
)  # should be 34853

# GPSINFO_TAG = 34853
print("GPSINFO_TAG:",GPSINFO_TAG)

# path = "my_geotagged_image.jpg"
# image = Image.open(path)
# info = image.getexif()
info = img_exif

gpsinfo = info.get_ifd(GPSINFO_TAG)
print(gpsinfo)
'''

gps_ifd = img_exif.get_ifd(ExifTags.IFD.GPSInfo)
print(gps_ifd)

# FROM https://stackoverflow.com/questions/19804768/interpreting-gps-info-of-exif-data-from-photo-in-python
#

import exifread as ef
# borrowed from 
# https://gist.github.com/snakeye/fdc372dbf11370fe29eb 
def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

def getGPS(filepath):
    '''
    returns gps data if present other wise returns empty dictionary
    '''
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return {}
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return {}
        return {'lat': lat_value, 'lon': lon_value}
    return {}

file_path = "sample.jpg"
gps = getGPS(file_path)
print(gps)