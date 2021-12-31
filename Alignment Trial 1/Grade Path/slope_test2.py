#import pickle
#srd_map,srn_map,sru_map=pickle.load(open("C:\\Users\\SANJEEV BASHYAL\\Documents\\QGIS\\Grade Path\\srd_srn_sru_20.dat", "rb"))
#srd=Grid(srd_map)
#srn=Grid(srn_map)
#sru=Grid(sru_map)

#import copy
csrd=copy.deepcopy(srd)
csrn=copy.deepcopy(srn)
csru=copy.deepcopy(sru)

#srd=copy.deepcopy(csrd)
#srn=copy.deepcopy(csrn)
#sru=copy.deepcopy(csru)

#pickle.dump([gr.map,sp,ep], open("C:\\Users\\SANJEEV BASHYAL\\Documents\\QGIS\\Grade Path\\gr_sp_ep_1000.dat", "wb"))


grd=Grid(np.full([gr.h,gr.w],np.inf)) #stores least distances
gru=Grid(csru.map) #unvisited nodes as True
grp=Grid(np.full([gr.h,gr.w],None)) #save path in form of points list
grn=Grid(np.full([gr.h,gr.w],False)) #nodes to get neighbours from

sp=np.array(ss[0][0]);tsp=np.array(rfe._row_col_to_point_list(sp)) 
ep=np.array(es[0][0]);tep=np.array(rfe._row_col_to_point_list(ep)) 

grd.insert(0,sp)
gru.insert(None,sp)
grp.insert(np.array([sp]),sp)
grn.insert(True,sp)

snei=gru.neighbors_ext(sp)
for point in snei:
    ppd=csrd.value(point)
    nein=csrn.value(point)
    pindex=np.where((nein== sp).all(1))[0]
    if pindex.size==0:
        continue
    ppd2=np.delete(ppd,pindex)
    nein2=np.delete(nein,pindex,axis=0)
    csrd.insert(ppd2,point)
    csrn.insert(nein2,point)

collect=np.array([sp])
i=1
psp=sp
while (sp!=ep).any():
    c_length=[]
    c_pp=[]
    c_sp=[]
    get_nei=np.transpose((grn.map==True).nonzero())
    for point in get_nei:
        nei=csrn.value(point)
        if nei.size==0:
            grn.insert(False,point)
            csru.insert(None,point)
            continue
            
        ppd=csrd.value(point)
        lpd=grd.value(point)
        total_ppd=lpd+ppd
        index=np.argmin(total_ppd)
        c_length.append(total_ppd[index])
        c_pp.append(nei[index])
        c_sp.append(point)
        
    index=np.argmin(c_length)
    pp=c_pp[index]
    prev_path=grp.value(c_sp[index])
    new_path=np.insert(prev_path,len(prev_path),pp,axis=0)
    grd.insert(c_length[index],pp)
    gru.insert(None,pp)
    grp.insert(new_path,pp)
    grn.insert(True,pp)
    
    snei=csru.neighbors_ext(pp)
    for point in snei:
        ppd=csrd.value(point)
        nein=csrn.value(point)
        pindex=np.where((nein== pp).all(1))[0]
        if pindex.size==0:
            continue
        ppd=np.delete(ppd,pindex)
        nein=np.delete(nein,pindex,axis=0)
        csrd.insert(ppd,point)
        csrn.insert(nein,point)
        
    
    psp=sp
    sp=pp
    collect=np.insert(collect,len(collect),pp,axis=0)
    
    i=i+1
    if i>100000:
        break;
        
        
        
#        grd.update(wt,nei[xsl])
        
        

    
#points=rfe.create_points_from_path(grp.value(pp))
#geo=RasterF.create_path_feature_from_points(points,0)
#geo.setAttributes([1])
#loc=r'C:\Users\SANJEEV BASHYAL\Documents\QGIS\Test\aspect_path47.shp'
#fields=QgsFields()
#fields.append(QgsField('id',QVariant.Int))
#writer=QgsVectorFileWriter(loc,'UTF-8',fields,QgsWkbTypes.LineString,QgsCoordinateReferenceSystem('ESRI:102306'),'ESRI Shapefile')
#writer.addFeature(geo)
#del(writer)
#iface.addVectorLayer(loc,'','ogr')