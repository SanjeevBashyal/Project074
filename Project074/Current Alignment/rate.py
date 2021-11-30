import csv, sys, json
from math import sqrt

def statAnal(data):
	data.sort()
	minimum = data[0]
	maximum = data[-1]
	dataLen = len(data)
	quartile = (maximum - minimum)/3
	frequency = [0,0,0,0]
	sumData = 0
	sumData2 = 0
	for x in data:
		qIndex = (x - minimum)/quartile
		frequency[int(qIndex)] += 100/dataLen
		sumData += x
		sumData2 += x**2
	frequency = {
		f'{round(minimum,3)} - {round(minimum + quartile,3)}' : round(frequency[0],3),
		f'{round(minimum + quartile,3)} - {round(minimum + 2 * quartile,3)}' : round(frequency[1],3),
		f'{round(minimum + 2 * quartile,3)} - {round(maximum - quartile,3)}' : round(frequency[2],3),
		f'{round(maximum - quartile,3)} - {round(maximum,3)}' : round(frequency[3],3),
	}
	average = sumData/dataLen
	sumData2 = sumData2 - dataLen*average**2
	sigma2 = sumData2/dataLen
	sigma = sqrt(sigma2)
	sd2 = sumData2/(dataLen-1)
	sd = sqrt(sd2)
	firstQIndex = (dataLen + 1)/4 - 1
	medQIndex = (dataLen + 1)/2 - 1
	thirdQIndex = 3*(dataLen + 1)/4 - 1
	firstQuartile = data[int(firstQIndex)]+(firstQIndex - int(firstQIndex))*(data[int(firstQIndex)+1] - data[int(firstQIndex)])
	median = data[int(medQIndex)]+(medQIndex - int(medQIndex))*(data[int(medQIndex)+1] - data[int(medQIndex)])
	thirdQuartile = data[int(thirdQIndex)]+(thirdQIndex - int(thirdQIndex))*(data[int(thirdQIndex)+1] - data[int(thirdQIndex)])
	return {
		'N': dataLen,
		'sum': round(sumData,3),
		'avg': round(average,3),
		'sum2': round(sumData2,3),
		'sigma2': round(sigma2,3),
		'sigma': round(sigma,3),
		'sd2': round(sd2,3),
		'sd': round(sd,3),
		'min': round(minimum,3),
		'firstQ': round(firstQuartile,3),
		'med': round(median,3),
		'thirdQ': round(thirdQuartile,3),
		'max': round(maximum,3),
		'freq': frequency
	}

lines, points, output = sys.argv[1:]

totalLength = 0;
bridges = [];

with open(lines) as lineFile:
	cr = csv.DictReader(lineFile)
	for row in cr:
		totalLength += float(row['len'])
		if float(row['bridgeLen']) > 0:
			bridges.append(round(float(row['bridgeLen']),3))

grades = [];
hzAngles = [];
with open(points) as pointFile:
	cr = csv.DictReader(pointFile)
	for row in cr:
		grades.append(round(abs(float(row['grade'])),3))
		hzAngles.append(round(float(row['hz. angle']),3))

bridgeAnal = statAnal(bridges)
gradeAnal = statAnal(grades)
hzAnglesAnal = statAnal(hzAngles)

outputJSON = {
	'Length': round(totalLength,3),
	'Bridges': bridgeAnal,
	'Grades': gradeAnal,
	'Hz Angles': hzAnglesAnal
}
	
with open(output+'.json', 'w') as outFile:
	outFile.write(json.dumps(outputJSON, indent=4))
	outFile.close()	
