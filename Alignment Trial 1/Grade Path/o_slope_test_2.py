# import pickle
import copy
# gr_map,sp,ep,srd_map,srn_map,sru_map=pickle.load(open(r'/workspace/template-python-flask/QGIS/o_gr_sp_ep_srd_srn_sru_20.dat','rb'))
# sp=np.array(sp)
# ep=np.array(ep)
# gr=Grid(gr_map)
# srd=Grid(srd_map)
# srn=Grid(srn_map)
# sru=Grid(sru_map)

csrd=copy.deepcopy(srd)
csrn=copy.deepcopy(srn)
csru=copy.deepcopy(sru)


grd=Grid(np.full([gr.h,gr.w],np.inf)) #stores least distances
gru=Grid(csru.map) #unvisited nodes as True
grp=Grid(np.full([gr.h,gr.w],None)) #save path in form of points list
# grn=Grid(np.full([gr.h,gr.w],False)) #nodes to get neighbours from

# sp=np.array(ss[0][0]);tsp=np.array(rfe._row_col_to_point_list(sp)) 
# ep=np.array(es[0][0]);tep=np.array(rfe._row_col_to_point_list(ep)) 

grd.insert(0,sp)
gru.insert(None,sp)
grp.insert(sp,sp)
# grn.insert(True,sp)
get_nei=np.array([sp])

snei=csru.neighbors_ext(sp)
for point in snei:
    ppd=csrd.value(point)
    nein=csrn.value(point)
    pindex=np.where((nein== sp).all(1))[0]
    if pindex.size==0:
        continue
    ppd=np.delete(ppd,pindex)
    nein=np.delete(nein,pindex,axis=0)
    if nein.size==0:
        get_nei=np.delete(get_nei,np.where((get_nei==point).all(1)),axis=0)
        csru.insert(None,point)
    csrd.insert(ppd,point)
    csrn.insert(nein,point)

collect=np.array([sp])
i=1
psp=sp
while (sp!=ep).any():
    print(i)
    c_length=[]
    c_pp=[]
    c_pp_array=csrn.values(get_nei)
    c_pp=np.array([z[0] for z in c_pp_array])
    c_length_array=csrd.values(get_nei)
    c_length=np.array([z[0] for z in c_length_array])
    lpd=grd.values(get_nei)
    total_ppd=lpd+c_length
        
    index=np.argmin(total_ppd)
    pp=c_pp[index]
    grd.insert(c_length[index],pp)
    gru.insert(None,pp)
    grp.insert(get_nei[index],pp)
    if csrn.value(pp).size!=0:
        get_nei=np.insert(get_nei,len(get_nei),pp,axis=0)
    
    snei=csru.neighbors_ext(pp)
    for point in snei:
        ppd=csrd.value(point)
        nein=csrn.value(point)
        pindex=np.where((nein== pp).all(1))[0]
        if pindex.size==0:
            continue
        ppd=np.delete(ppd,pindex)
        nein=np.delete(nein,pindex,axis=0)
        if nein.size==0:
            get_nei=np.delete(get_nei,np.where((get_nei==point).all(1)),axis=0)
            csru.insert(None,point)
        csrd.insert(ppd,point)
        csrn.insert(nein,point)
    
    psp=sp
    sp=pp
    # collect=np.insert(collect,len(collect),pp,axis=0)
    
    i=i+1
    if i>1000000:
        break;
        

pickle.dump([grp.map,grd.map],open(r'/workspace/template-python-flask/QGIS/o_grp_grd_20_1000000.dat','wb'))
        


        
        

    
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
