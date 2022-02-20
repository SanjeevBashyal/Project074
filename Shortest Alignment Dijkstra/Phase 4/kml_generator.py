import numpy as np
import itertools
import time as t

initial="""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>test.kml</name>
	<StyleMap id="m_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_ylw-pushpin_hl</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="s_ylw-pushpin_hl">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
	</Style>
	<Style id="s_ylw-pushpin">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
	</Style>
	<Placemark>
		<name>test</name>
		<styleUrl>#m_ylw-pushpin</styleUrl>
		<LineString>
			<tessellate>1</tessellate>
			<coordinates>
				"""

res=0.00033
extent=[87.38351878050827,87.52360304217966,27.28180312854887,27.38263521208897]
# extent=np.array([83.7170,85.7245,27.6089,28.2818])
i=np.floor((extent[3]-extent[2])/res)
j=np.floor((extent[1]-extent[0])/res)
y=np.arange(i)
x=np.arange(j)
nc=extent[2]+y*res
ec=extent[0]+x*res
t0=t.time()
z=np.array([x for x in itertools.product(ec, nc,np.arange(1))])
t1=t.time()
st = ' '.join([','.join([str(e) for e in l]) for l in z])
t2=t.time()
at_last=""" 
			</coordinates>
		</LineString>
	</Placemark>
</Document>
</kml>"""
with open(r'C:/Users/SANJEEV BASHYAL/Documents/Project074/Phase 4/out_kumar.kml','w') as f:
    f.write(initial)
    f.write(st)
    f.write(at_last)


t3=t.time()
print('Here')
print(t1-t0,t2-t1,t3-t2, sep='--')

