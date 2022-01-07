import pickle
ele=QgsProject.instance().mapLayersByName('Elevation_TM_1000')[0]
stp=QgsProject.instance().mapLayersByName('stp_tm')[0]
etp=QgsProject.instance().mapLayersByName('etp_tm')[0]
rfe=RasterF(ele)
blocke=rfe.get_block(1)
#mate,oute=rfe.block2matrix(blocke)
ss=rfe.features_to_tuples(list(stp.getFeatures()),blocke)
es=rfe.features_to_tuples(list(etp.getFeatures()),blocke)

gd=20 #design grade
ad=10 #slope scaling in weightage

# gr=Grid(mate);del(mate)
gr = Grid(rfe.block2matrix(blocke)[0])
srd=Grid(np.full([gr.h,gr.w],None)) #stores least distances
srn=Grid(np.full([gr.h,gr.w],None)) #stores neighbouring points
sru=Grid(np.full([gr.h,gr.w],None)) #stores legit nodes
for i in range(gr.h):
    for j in range(gr.w):
        point=np.array([i,j])
        if not gr.is_valid(point):
            continue;
            
        nei=gr.neighbors_ext(point)
        if nei.size==0:
            continue
        tnei=np.array(rfe.create_points_from_path_list(nei))
        tpoint=np.array(rfe._row_col_to_point_list(point))
        
        e0=gr.value(point)
        en=gr.values(nei)
        ediff=en-e0

        diff=tnei-tpoint
        mag=np.linalg.norm(diff,axis=1)

        sl=ediff/mag*100
        xsl=np.where(np.abs(sl)<gd)[0]
        if xsl.size==0:
            continue
        ppd=mag[xsl]*(1+ad*np.abs(sl[xsl])/100)
        oxsl=ppd.argsort()
        srd.insert(ppd[oxsl],point)
        srn.insert(nei[xsl][oxsl],point)
        sru.insert(True,point)

pickle.dump([gr.map, ss[0][0], es[0][0], srd.map, srn.map, sru.map], open("C:\\Users\\SANJEEV BASHYAL\\Documents\\QGIS\\Grade Path\\o_gr_sp_ep_srd_srn_sru_20_10.dat", "wb"))



#
#mgr=gr.map
#mgr[mgr!=None]=True
#grd=Grid(np.full([gr.h,gr.w],np.inf)) #stores least distances
#gru=Grid(mgr) #unvisited nodes as True
#del(mgr)
#grp=Grid(np.full([gr.h,gr.w],None)) #save path in form of points list
#grn=Grid(np.full([gr.h,gr.w],False)) #nodes to get neighbours from
#
#gd=5 #design grade
#ad=5 #slope scaling in weightage
#sp=np.array(ss[0][0]);tsp=np.array(rfe._row_col_to_point_list(sp)) 
#ep=np.array(es[0][0]);tep=np.array(rfe._row_col_to_point_list(ep)) 
#
#grd.insert(0,sp)
#gru.insert(None,sp)
#grp.insert(np.array([sp]),sp)
#grn.insert(True,sp)
#
#collect=np.array([sp])
#i=1
#psp=sp
#while (sp!=ep).any():
#    c_length=[]
#    c_pp=[]
#    c_sp=[]
#    get_nei=np.transpose((grn.map==True).nonzero())
#    for point in get_nei:
#        nei=gru.neighbors_ext(point)
#        if nei.size==0:
#            grn.insert(False,point)
#            continue
#        tnei=np.array(rfe.create_points_from_path_list(nei))
#        
#        e0=gr.value(point)
#        en=gr.values(nei)
#        ediff=en-e0
#
#        diff=tnei-tsp
#        mag=np.linalg.norm(diff,axis=1)
#
#        sl=ediff/mag*100
#        xsl=np.where(np.abs(sl)<5)[0]
#        if xsl.size==0:
#            grn.insert(False,point)
#            continue
#        ppd=mag[xsl]*(1+ad*np.abs(sl[xsl])/100)
#        lpd=grd.value(point)
#        total_ppd=lpd+ppd
#        index=np.argmin(total_ppd)
#        c_length.append(total_ppd[index])
#        c_pp.append(nei[xsl][index])
#        c_sp.append(point)
#        
#    index=np.argmin(c_length)
#    pp=c_pp[index]
#    prev_path=grp.value(c_sp[index])
#    new_path=np.insert(prev_path,len(prev_path),pp,axis=0)
#    grd.insert(c_length[index],pp)
#    gru.insert(None,pp)
#    grp.insert(new_path,pp)
#    grn.insert(True,pp)
#    psp=sp
#    sp=pp
#    collect=np.insert(collect,len(collect),pp,axis=0)
#    
#    i=i+1
#    if i>1000000:
#        break;
#        
#        
#        
##        grd.update(wt,nei[xsl])
#        
#        
#
#    
#points=rfe.create_points_from_path(grp.value(ep))
#geo=RasterF.create_path_feature_from_points(points,0)
#geo.setAttributes([1])
#loc=r'C:\Users\SANJEEV BASHYAL\Documents\QGIS\Test\aspect_path30.shp'
#fields=QgsFields()
#fields.append(QgsField('id',QVariant.Int))
#writer=QgsVectorFileWriter(loc,'UTF-8',fields,QgsWkbTypes.LineString,QgsCoordinateReferenceSystem('ESRI:102306'),'ESRI Shapefile')
#writer.addFeature(geo)
#del(writer)
#iface.addVectorLayer(loc,'','ogr')
