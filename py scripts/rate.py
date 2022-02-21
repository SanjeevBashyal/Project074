import csv, sys, json
from math import sqrt
from rateSteps import rateStep

def statAnal(data, cutHigh = False):
	if len(data)==0:
		return {
			'N': 0,
			'sum': 0,
			'avg': 0,
			'sum2': 0,
			'sigma2': 0,
			'sigma': 0,
			'sd2': 0,
			'sd': 0,
			'min': 0,
			'firstQ': 0,
			'med': 0,
			'thirdQ': 0,
			'max': 0,
			'freq': {
				'0-100': 100,
				'100-200' : 0,
				'200-300' : 0,
				'300-400' : 0
			}
	}
	data.sort()
	dataLen = len(data)
	
	if(dataLen>2):
		thirdQIndex = 3*(dataLen + 1)/4 - 1
		thirdQuartile = data[int(thirdQIndex)]+(thirdQIndex - int(thirdQIndex))*(data[int(thirdQIndex)+1] - data[int(thirdQIndex)])
		
		if cutHigh:
			data = list(filter(lambda x: x <= thirdQuartile, data))
			dataLen = len(data)
			thirdQIndex = 3*(dataLen + 1)/4 - 1
			thirdQuartile = data[int(thirdQIndex)]+(thirdQIndex - int(thirdQIndex))*(data[int(thirdQIndex)+1] - data[int(thirdQIndex)])
			
		
		firstQIndex = (dataLen + 1)/4 - 1
		firstQuartile = data[int(firstQIndex)]+(firstQIndex - int(firstQIndex))*(data[int(firstQIndex)+1] - data[int(firstQIndex)])
		
		medQIndex = (dataLen + 1)/2 - 1
		median = data[int(medQIndex)]+(medQIndex - int(medQIndex))*(data[int(medQIndex)+1] - data[int(medQIndex)])
	else:
		firstQuartile = data[0]
		median = 0.5*(data[0]+data[-1])
		thirdQuartile = data[-1]
	
	minimum = data[0]
	maximum = data[-1]
	quartile = (maximum - minimum)/4
	frequency = [0,0,0,0]
	sumData = 0
	sumData2 = 0
	
	for x in data:
		qIndex = int((x - minimum)/quartile)
		frequency[min([qIndex,3])] += 100/dataLen
		sumData += x
		sumData2 += x**2
		
	average = sumData/dataLen
	sumData2 = sumData2 - dataLen*average**2
	sigma2 = sumData2/dataLen
	sigma = sqrt(sigma2)
	sd2 = sumData2/(dataLen-1)
	sd = sqrt(sd2)
	
	frequency = {
		f'{round(minimum,3)} - {round(minimum + quartile,3)}' : round(frequency[0],3),
		f'{round(minimum + quartile,3)} - {round(minimum + 2 * quartile,3)}' : round(frequency[1],3),
		f'{round(maximum - 2 * quartile,3)} - {round(maximum - quartile,3)}' : round(frequency[2],3),
		f'{round(maximum - quartile,3)} - {round(maximum,3)}' : round(frequency[3],3),
	}
	
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

directory = sys.argv[1]
analysed = directory + '\\CSVs\\analysed.csv'
output = directory + '\\Score\\score.json'


totalLength = 0;
bridges = [];
tunnels = [];
grades = [];
hzAngles = [];

with open(analysed) as pointFile:
	cr = csv.DictReader(pointFile)
	isBridge = 0;
	isTunnel = 0;
	for row in cr:
		grades.append(round(abs(float(row['grade'])),3))
		hzAngles.append(round(float(row['hz. angle']),3))
		isBridgeTemp = int(row['bridge'])
		if isBridgeTemp == 1:
			if isBridge == 0:
				bridges.append(float(row['length']))
			else:
				bridges[-1] += float(row['length'])
		isBridge = isBridgeTemp
		isTunnelTemp = int(row['tunnel'])
		if isTunnelTemp == 1:
			if isTunnel == 0:
				tunnels.append(float(row['length']))
			else:
				tunnels[-1] += float(row['length'])
		isTunnel = isTunnelTemp
		totalLength += float(row['length'])

bridgeAnal = statAnal(bridges)
tunnelAnal = statAnal(tunnels)
gradeAnal = statAnal(grades, True)
hzAnglesAnal = statAnal(hzAngles)

outputJSON = {
	'Length': round(totalLength,3),
	'Bridges': bridgeAnal,
	'Tunnels': tunnelAnal,
	'Grades': gradeAnal,
	'Hz Angles': hzAnglesAnal
}

# def rateAnal(stats, sum = 0, N = 0, med = 0, thirdQ = 0, max = 0, avg = 0, freq = 1):
	# rateDict = {'sum': sum, 'N': N, 'med': med, 'thirdQ': thirdQ, 'max': max, 'avg': avg, 'freq': freq}
	# for x in ['sum', 'N', 'med', 'thirdQ', 'max', 'avg']:
		# if rateDict[x]!=0:
			# rateDict[x] = min([round(stats[x]/rateDict[x],1),10])
	# if rateDict['freq']!=0:
		# rateDict['freq'] = 0
		# statsFreq = list(stats['freq'].values())
		# for x in range(0,4):
			# rateDict['freq'] += round((x+1)*statsFreq[x]/400,1)*5
	# return rateDict
	
# ratingJSON = {
	# 'Length': f"{round((totalLength - 140000)/rateStep['length'], 1)}",
	# 'Bridges': rateAnal(bridgeAnal, **rateStep['bridge']),
	# 'Tunnels': rateAnal(tunnelAnal, **rateStep['tunnel']),
	# 'Grades': rateAnal(gradeAnal, **rateStep['grade']),
	# 'Hz Angles': rateAnal(hzAnglesAnal, **rateStep['hzAngle'])
# }

with open(output, 'w') as outFile:
	outFile.write(json.dumps(outputJSON, indent=4))
	outFile.close()	
	
# with open(output+'Score.json', 'w') as outFile:
	# outFile.write(json.dumps(ratingJSON, indent=4))
	# outFile.close()	
