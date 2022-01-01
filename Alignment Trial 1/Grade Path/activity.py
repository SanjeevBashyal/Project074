import numpy as np
import math as m

class Grid:
        def __init__(self, matrix):
            self.map = np.array(matrix)
            self.check=1
            self.h = len(matrix)
            self.w = len(matrix[0])
            self.manhattan_boundry = None
            self.curr_boundry = None

        def _in_bounds(self, id):
            x, y = id
            return 0 <= x < self.h and 0 <= y < self.w

        def _passable(self, id):
            x, y = id
            return self.map[x][y] is not None

        def is_valid(self, id):
            return self._in_bounds(id) and self._passable(id)

        def neighbors(self, id):
            x, y = id
            results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1),
                       (x + 1, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1)]
            results = list(filter(self.is_valid, results))
            return np.array(results)
            
        def neighbors_ext(self, id):
            x, y = id
            results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1),
                       (x + 1, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1),
                       (x+2,y+1),(x+1,y+2),(x-1,y+2),(x-2,y+1),(x-2,y-1),(x-1,y-2),(x+1,y-2),(x+2,y-1)]
            results = list(filter(self.is_valid, results))
            return np.array(results)
            
        def values(self, id):
            return self.map[id[:,0],id[:,1]]
            
        def value(self, id):
            return self.map[id[0],id[1]]
            
        def insert(self,value,id):
            self.map[id[0],id[1]]=value
            
        def update_less_than(self,values,ids):
            vals=self.values(ids)
            ids=ids[np.where(values<vals)]
            list(map(lambda n,m:self.insert(m,n),values[ids],ids))

        @staticmethod
        def manhattan_distance(id1, id2):
            x1, y1 = id1
            x2, y2 = id2
            return abs(x1 - x2) + abs(y1 - y2)

        @staticmethod
        def min_manhattan(curr_node, end_nodes):
            return min(map(lambda node: Grid.manhattan_distance(curr_node, node), end_nodes))

        @staticmethod
        def max_manhattan(curr_node, end_nodes):
            return max(map(lambda node: Grid.manhattan_distance(curr_node, node), end_nodes))

        @staticmethod
        def all_manhattan(curr_node, end_nodes):
            return {end_node: Grid.manhattan_distance(curr_node, end_node) for end_node in end_nodes}

        def simple_cost(self, cur, nex):
            cx, cy = cur
            nx, ny = nex
            currV = self.map[cx][cy]
            offsetV = self.map[nx][ny]
            if cx == nx or cy == ny:
                return (currV + offsetV) / 2
            else:
                return m.sqrt(2) * (currV + offsetV) / 2

import pickle
# import copy
gr_map,sp,ep,srd_map,srn_map,sru_map=pickle.load(open(r'C:/Users/SANJEEV BASHYAL/Documents/QGIS/Grade Path/o_gr_sp_ep_srd_srn_sru_20.dat','rb'))
sp=np.array(sp)
osp=sp.copy()
ep=np.array(ep)
gr=Grid(gr_map)
csrd=Grid(srd_map)
csrn=Grid(srn_map)
csru=Grid(sru_map)

del(srd_map,srn_map,sru_map,gr_map)

# csrd=copy.deepcopy(srd)
# csrn=copy.deepcopy(srn)
# csru=copy.deepcopy(sru)


grd=Grid(np.full([gr.h,gr.w],np.inf)) #stores least distances
# gru=Grid(csru.map) #unvisited nodes as True
grp=Grid(np.full([gr.h,gr.w],None)) #save path in form of points list
# grn=Grid(np.full([gr.h,gr.w],False)) #nodes to get neighbours from

# sp=np.array(ss[0][0]);tsp=np.array(rfe._row_col_to_point_list(sp)) 
# ep=np.array(es[0][0]);tep=np.array(rfe._row_col_to_point_list(ep)) 

grd.insert(0,sp)
# gru.insert(None,sp)
grp.insert(sp,sp)
# grn.insert(True,sp)
get_nei=np.array([sp])
if csrn.value(sp).size!=0:
    c_pp=np.array([csrn.value(sp)[0]])
    c_length=np.array([csrd.value(sp)[0]+grd.value(sp)])
else:
    print("Starting point has no neighbors")
    exit(0)


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
        index0=np.where((get_nei==point).all(1))[0]
        get_nei=np.delete(get_nei,index0,axis=0)
        c_pp=np.delete(c_pp,index0,axis=0)
        c_length=np.delete(c_length,index0,axis=0)
        csru.insert(None,point)
    csrd.insert(ppd,point)
    csrn.insert(nein,point)

# collect=np.array([sp])
i=1
psp=sp
while (sp!=ep).any():
    # print(i)
    # if i==9999:
    #     print("Here")
    index=np.argmin(c_length)
    pp=c_pp[index].copy()
    grd.insert(c_length[index],pp)
    # gru.insert(None,pp)
    grp.insert(get_nei[index],pp)
    if csrn.value(pp).size!=0:
        get_nei=np.insert(get_nei,len(get_nei),pp,axis=0)
        c_pp=np.insert(c_pp,len(c_pp),csrn.value(pp)[0],axis=0)
        c_length=np.insert(c_length,len(c_length),csrd.value(pp)[0]+grd.value(pp),axis=0)


    while True:
        c_pp_array=csrn.value(get_nei[index])
        c_length_array=csrd.value(get_nei[index])
        if len(c_pp_array)>1:
            c_pp[index]=c_pp_array[1]
            c_length[index]=c_length_array[1]+grd.value(get_nei[index])
        else:
            csru.insert(None,get_nei[index])
            get_nei=np.delete(get_nei,index,axis=0)
            c_pp=np.delete(c_pp,index,axis=0)
            c_length=np.delete(c_length,index,axis=0)
        indexes=np.where((c_pp== pp).all(1))[0]
        if indexes.size==0:
            break
        else:
            index=indexes[0]




    

    
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
            index0=np.where((get_nei==point).all(1))[0]
            get_nei=np.delete(get_nei,index0,axis=0)
            c_pp=np.delete(c_pp,index0,axis=0)
            c_length=np.delete(c_length,index0,axis=0)
            csru.insert(None,point)
        csrd.insert(ppd,point)
        csrn.insert(nein,point)
    
    psp=sp
    sp=pp
    # collect=np.insert(collect,len(collect),pp,axis=0)
    
    i=i+1
    if i>10000:
        break;
        
# np.savez('mat.npz', sp=osp, ep=ep, grp=grp.map, grd=grd.map )
# pickle.dump([sp,ep,grp.map,grd.map],open(r'C:/Users/SANJEEV BASHYAL/Documents/QGIS/Grade Path/o_sp_ep_grp_grd_20_1000000.dat','wb'))
        


        
        

    
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
