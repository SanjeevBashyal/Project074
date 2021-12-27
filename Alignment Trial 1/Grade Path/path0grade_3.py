import numpy as np

gr=Grid(mat)

#rf is RasterF instance from first.py (execute script first.py first)
sp=np.array(ss[0][0]);tsp=np.array(rf._row_col_to_point_list(sp)) 
ep=np.array(es[0][0]);tep=np.array(rf._row_col_to_point_list(ep)) 
collect=np.array([sp])
i=1
psp=sp

while i<500:
    spv=gr.value(sp)
    sp1=spv+90;spd1=sp1* np.pi / 180; vp1=np.array([np.sin(spd1), np.cos(spd1)]);
    sp2=spv-90;spd2=sp2* np.pi / 180; vp2=np.array([np.sin(spd2), np.cos(spd2)]);

    v=tep-tsp
    d1=np.dot(vp1,v)
    d2=np.dot(vp2,v)
    theta=sp1
    uv=vp1
    carry=[sp1,sp2,vp1,vp2];
    if d2>d1:
        theta=sp2
        uv=vp2
        carry=[sp2,sp1,vp2,vp1];
#    print(spv,sp1,sp2,spd1,spd2,vp1,vp2,v,d1,d2,theta,uv)

    nei=gr.neighbors_ext(sp)
#    nei=np.delete(nei,np.where((nei== psp).all(1)),axis=0)
    tnei=np.array(rf.create_points_from_path_list(nei))

    spv=gr.value(sp)
    npv=gr.values(nei)
    
    diff=tnei-tsp
    mag=np.linalg.norm(diff,axis=1)
    unit_vec=diff/mag[:,None]
    while True:
        dp=np.array([np.dot(uv,v) for v in unit_vec])
        pos=np.argmax(dp)
        pp=nei[pos]
        if (pp==psp).all(0)==False:
            break;
        else:
            theta=carry[1]
            uv=carry[3]
#    print(npv,nei,tnei,diff,unit_vec,dp,pos,pp)
    collect=np.insert(collect,len(collect),pp,axis=0)
    i=i+1
    psp=sp
    sp=pp
    tsp=np.array(rf._row_col_to_point_list(sp))

#print(collect)
points=rf.create_points_from_path(collect)
geo=RasterF.create_path_feature_from_points(points,0)
geo.setAttributes([1])
loc=r'C:\Users\SANJEEV BASHYAL\Documents\QGIS\Test\aspect_path10.shp'
fields=QgsFields()
fields.append(QgsField('id',QVariant.Int))
writer=QgsVectorFileWriter(loc,'UTF-8',fields,QgsWkbTypes.LineString,QgsCoordinateReferenceSystem('ESRI:102306'),'ESRI Shapefile')
writer.addFeature(geo)
del(writer)
iface.addVectorLayer(loc,'','ogr')