from math import sqrt, e, pi, sin, cos, acos
import csv, sys

latLonAlt, output = sys.argv[1:]

a = 6378137 #semi-major axis
b = 6356752.314245 #semi-minor axis
e = 1 - (b/a)**2

N = lambda lat: a/sqrt(1-e**2*sin(lat)**2)

def getXYZ(lat, lon, alt):
	lat = lat*pi/180
	lon = lon*pi/180
	X = (N(lat) + alt)*cos(lat)*cos(lon)
	Y = (N(lat) + alt)*cos(lat)*sin(lon)
	Z = ((1-e)*N(lat) + alt)*sin(lat)
	return [X,Y,Z]

data = [['id','lat', 'lon', 'alt', 'x','y','z', 'length','grade','hz. angle']]
with open(latLonAlt) as csvFile:
	cr = csv.DictReader(csvFile)
	rowIndex = 0
	for row in cr:
		lat = float(row['y'])
		lon = float(row['x'])
		alt = float(row['z'])
		x,y,z = getXYZ(float(row['y']), float(row['x']), alt)
		if rowIndex == 0:
			len = grade = 0
		else:
			alt0,x0,y0,z0 = data[-1][3:7]
			len = sqrt((x-x0)**2+(y-y0)**2+(z-z0)**2)
			grade = 100*(alt - alt0)/len
		if rowIndex < 2:
			hz = 0
		else:
			x_1,y_1 = data[-2][4:6]
			hz = acos(((x-x0)*(x0-x_1)+(y-y0)*(y0-y_1))/sqrt(((x-x0)**2+(y-y0)**2)*((x0-x_1)**2+(y0-y_1)**2)))*180/pi
		data.append([rowIndex+1, lat, lon, alt, x, y, z, len, grade, hz])
		rowIndex += 1

with open(output, 'w', newline='') as csvFile:
	writer = csv.writer(csvFile)
	writer.writerows(data)