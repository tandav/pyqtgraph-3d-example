import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def xyz():
    """
    # 31.2 MB
    curl -O http://download.geonames.org/export/dump/cities500.zip
    unzip cities500.zip

    The main 'geoname' table has the following fields :
    ---------------------------------------------------
    geonameid         : integer id of record in geonames database
    name              : name of geographical point (utf8) varchar(200)
    asciiname         : name of geographical point in plain ascii characters, varchar(200)
    alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
    latitude          : latitude in decimal degrees (wgs84)
    longitude         : longitude in decimal degrees (wgs84)
    feature class     : see http://www.geonames.org/export/codes.html, char(1)
    feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
    country code      : ISO-3166 2-letter country code, 2 characters
    cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
    admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
    admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
    admin3 code       : code for third level administrative division, varchar(20)
    admin4 code       : code for fourth level administrative division, varchar(20)
    population        : bigint (8 byte int) 
    elevation         : in meters, integer
    dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
    timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
    modification date : date of last modification in yyyy-MM-dd format
    """
    d = pd.read_csv('http://download.geonames.org/export/dump/cities500.zip', sep='\t', header=None, names=[
        'geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 
        'longitude', 'feature class', 'feature code', 'country code', 
        'cc2', 'admin1 code', 'admin2 code', 'admin3 code', 'admin4 code', 
        'population', 'elevation', 'dem', 'timezone', 'modification date',
    ])[['latitude', 'longitude']]
    lat, lon = d.latitude.values, d.longitude.values
    earth_radius = 6.3781e6
    x = earth_radius * np.cos(lat) * np.cos(lon)
    y = earth_radius * np.cos(lat) * np.sin(lon)
    z = earth_radius * np.sin(lat)
    return x, y, z


x, y, z = xyz()
X = np.vstack((x, y, z)).T
X = MinMaxScaler(feature_range=(-1, 1)).fit_transform(X)
np.save('X.npy', X)
