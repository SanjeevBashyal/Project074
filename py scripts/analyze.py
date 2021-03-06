from math import sqrt, pi, sin, cos, tan, acos
import csv, sys

directory = sys.argv[1]
latLonAlt = directory + '\\CSVs\\data.csv'
output = directory + "\\CSVs\\analysed.csv"
projectCoords = True if 'p' in sys.argv else False
STRT_SPEED = float(input('Enter straight reach speed [default = 30kmph]'))
STRT_SPEED = STRT_SPEED if STRT_SPEED > 0 else 30

# ref: https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates
def getXYZ(lat, lon, alt):
	a = 6378137 #semi-major axis
	b = 6356752.314245 #semi-minor axis
	e = 1 - (b/a)**2
	N = lambda lat: a/sqrt(1-e**2*sin(lat)**2)
	lat = lat*pi/180
	lon = lon*pi/180
	X = (N(lat) + alt)*cos(lat)*cos(lon)
	Y = (N(lat) + alt)*cos(lat)*sin(lon)
	Z = ((1-e)*N(lat) + alt)*sin(lat)
	return [X,Y,Z]

data = [['id', 'X','Y','Z', 'length','bridge','tunnel','grade','hz. angle','speed','time']]
with open(latLonAlt) as csvFile:
	cr = csv.DictReader(csvFile)
	rowIndex = 0
	for row in cr:
		Y = float(row['Y'])
		X = float(row['X'])
		alt = float(row['Z'])
		x,y,z = getXYZ(Y, X, alt) if projectCoords else [X,Y,alt]
		bridge = int(row['bridge']=='T')
		tunnel = int(row['tunnel']=='T')
		if rowIndex == 0:
			len = grade = 0
		else:
			x0,y0,z0 = data[-1][1:4]
			len = sqrt((x-x0)**2+(y-y0)**2+(z-z0)**2)
			grade = 100*(alt - alt0)/len
		if rowIndex < 2:
			hz = 0
			speed = STRT_SPEED
		else:
			x_1,y_1 = data[-2][1:3]
			l1 = sqrt((x-x0)**2+(y-y0)**2)
			l2 = sqrt((x0-x_1)**2+(y0-y_1)**2)
			gr = 0.005*(grade + data[-1][7])
			hz = acos(min(1,((x-x0)*(x0-x_1)+(y-y0)*(y0-y_1))/(l1*l2)))
			min_speed=STRT_SPEED
			if not hz==0:
				min_speed=min(STRT_SPEED,5.292*sqrt((1-gr)*min(l1,l2)/tan(hz/2)))
			speed = max(float(row['maxspeed']), min_speed)
		data.append([rowIndex+1, x, y, z, len, bridge, tunnel, grade, hz*180/pi, speed, 3.6*len/speed])
		rowIndex += 1
		alt0 = alt

with open(output, 'w', newline='') as csvFile:
	writer = csv.writer(csvFile)
	writer.writerows(data)