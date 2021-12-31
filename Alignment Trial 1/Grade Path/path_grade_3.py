import numpy as np

def setdiff2d(A,B):
    nrows, ncols = A.shape
    dtype={'names':['f{}'.format(i) for i in range(ncols)],
           'formats':ncols * [A.dtype]}

    C = np.setdiff1d(A.view(dtype), B.view(dtype))

    # This last bit is optional if you're okay with "C" being a structured array...
    C = C.view(A.dtype).reshape(-1, ncols)
    return C

gd=5

gr=Grid(mat)
slp=Grid(mats)

#rf is RasterF instance from first.py (execute script first.py first)
sp=np.array(ss[0][0]);tsp=np.array(rf._row_col_to_point_list(sp)) 
ep=np.array(es[0][0]);tep=np.array(rf._row_col_to_point_list(ep)) 
collect=np.array([sp])
i=1
psp=sp

flag=0

while i<4000:
    spv=gr.value(sp)
    slpv=slp.value(sp)
    delta=np.arcsin(gd/slpv)*180/np.pi
    if np.isnan(delta):
        delta=np.sign(gd)*90
    
    sp1=spv+90+delta;spd1=sp1* np.pi / 180; vp1=np.array([np.sin(spd1), np.cos(spd1)]);
    sp2=spv-90-delta;spd2=sp2* np.pi / 180; vp2=np.array([np.sin(spd2), np.cos(spd2)]);

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
    k=0
    while True:
        dp=np.array([np.dot(uv,v) for v in unit_vec])
        pos=np.argmax(dp)
        pp=nei[pos]
        if (pp==psp).all(0)==False:
            break;
        else:
            k=k+1
            theta=carry[1]
            uv=carry[3]
            if k>1:
                flag=1
#                print(i)
#                print(sp)
#                print(spv,slpv,delta)
#                print(sp1,sp2,spd1,spd2,vp1,vp2,v,d1,d2,theta,uv)
#                print(npv,nei,tnei,diff,unit_vec,dp,pos,pp)
                break
                
    chk=(pp== collect).all(1)
    if 1 in chk:
        nei=setdiff2d(nei,collect)
        if nei.size==0:
            print("Reached to elevation well")
            break;
        tnei=np.array(rf.create_points_from_path_list(nei))
        diff=tnei-tsp
        mag=np.linalg.norm(diff,axis=1)
        unit_vec=diff/mag[:,None]
        dp=np.array([np.dot(uv,v) for v in unit_vec])
        pos=np.argmax(dp)
        pp=nei[pos]
    collect=np.insert(collect,len(collect),pp,axis=0)
#    if i==296:
#        print(i,sp)
#        print(spv,slpv,delta)
#        print(sp1,sp2,spd1,spd2,vp1,vp2,v,d1,d2,theta,uv)
#        print(npv,nei,tnei,diff,unit_vec,dp,pos,pp)
#    if flag==1:
#        break
    i=i+1
    psp=sp
    sp=pp
    tsp=np.array(rf._row_col_to_point_list(sp))

#print(collect)

points=rf.create_points_from_path(collect)
geo=RasterF.create_path_feature_from_points(points,0)
geo.setAttributes([1])
loc=r'C:\Users\SANJEEV BASHYAL\Documents\QGIS\Test\aspect_path25.shp'
fields=QgsFields()
fields.append(QgsField('id',QVariant.Int))
writer=QgsVectorFileWriter(loc,'UTF-8',fields,QgsWkbTypes.LineString,QgsCoordinateReferenceSystem('ESRI:102306'),'ESRI Shapefile')
writer.addFeature(geo)
del(writer)
iface.addVectorLayer(loc,'','ogr')