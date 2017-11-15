from urllib import request
import urllib
import io
from PIL import Image
import math

# Required Pillow installed. (Fork of PIL)

# A Python script that downloads a map on a level 13 zoom from OpenStreetMap. Input parameters are (1, 2)
# latitude and longitude of the first chosen point and (3, 4) lat and lon of the second point.
# The program will generate a map between these points as a rectangle.
# 5th parameter determines the filename of the saved image file.

# both converters are from OSM's own docuentation.
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

# creates a picture(= 256x256 png tile) from the given coordinates and zoom.
def createPic(lat, lon, zoom):
    xTile, yTile = deg2num(lat, lon, zoom)
    url = "http://tile.openstreetmap.org/{ZOOM}/{X}/{Y}.png".format(ZOOM=13, X=xTile, Y=yTile)
    image = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
    return xTile, yTile, image

# determines the zoom level of the pictures. Don't touch! Your temp folder will thank me.
zoom = 13

# Latitude and longitude of the top-left corner given by the command line arguments.
print("1st point latitude: ")
topLeftLat = float(input())
print("1st point longitude: ")
topLeftLon = float(input())

# Latitude and longitude of the bottom-right corner, respectively.
print("2nd point latitude: ")
botRightLat = float(input())
print("2nd point longitude: ")
botRightLon = float(input())

print("Working...")

# Bottom-right corner x and y tiles.
xTileBotCorner , yTileBotCorner = deg2num(botRightLat, botRightLon, zoom)

coords0 = deg2num(topLeftLat, topLeftLon, zoom)
coords1 = num2deg((coords0[0]), (coords0[1]), zoom)
coords2 = num2deg((coords0[0]+1), (coords0[1]+1), zoom)

height = math.ceil( (topLeftLat-botRightLat)/(coords1[0]-coords2[0]) )
width = math.ceil( (botRightLon-topLeftLon)/(coords2[1]-coords1[1]) )

# Since the tiles are 256x256
height = height * 256
width = width * 256

# destination image for all the tiles.
finalImage = Image.new("RGB", (width, height))

# Again, some default variables.
lat = topLeftLat
x = 0
y = 0
xTile = 1
yTile = 1

# Save loop. Generates one row at a time, whilst simultaneously saving each downloaded tile into the
# "finalImage"-image variable. The indexes are by pixels hence the *256 multiplier on X and Y.
while(yTile != yTileBotCorner):
    lon = topLeftLon
    while (lon <= botRightLon + 0.05):
        xTile, yTile , img = createPic(lat, lon, zoom)
        lon += 0.045
        finalImage.paste(img, ((x*256), (y*256)))
        x += 1
    lat, NOT_USED = num2deg(xTile, yTile, zoom)
    x = 0
    y += 1
    lat -= 0.04

print("Done!")

# Shows the generated picture. It's a temp file.
finalImage.show()
