import numpy as np
import itertools

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

at_last=""" 
			</coordinates>
		</LineString>
	</Placemark>
</Document>
</kml>"""

res=0.0005
extent=[84.5129267936814,84.82782897754934,27.758668447143553,28.027348316440317]
i=np.floor((extent[3]-extent[2])/res)
j=np.floor((extent[1]-extent[0])/res)
y=np.arange(i)
x=np.arange(j)

to_loop=4
for i in range(to_loop):
    start=np.floor(j/to_loop*i)
    stop=np.floor(j/to_loop*(i+1))
    xx=np.arange(start,stop)
    nc=extent[2]+y*res
    ec=extent[0]+xx*res
    z=np.array([x for x in itertools.product(ec, nc,np.arange(1))])
    st = ' '.join([','.join([str(e) for e in l]) for l in z])
    path=r'C:/Users/SANJEEV BASHYAL/Documents/Project074/Phase 4/out_'+str(i)+r'.kml'
    with open(path,'w') as f:
        f.write(initial)
        f.write(st)
        f.write(at_last)
    print(i)

