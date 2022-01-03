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
import copy
gr_map,sp,ep,srd_map,srn_map,sru_map=pickle.load(open(r'C:/Users/SANJEEV BASHYAL/Documents/QGIS/Grade Path/o_gr_sp_ep_srd_srn_sru_20.dat','rb'))
sp=np.array(sp)
ep=np.array(ep)
gr=Grid(gr_map)
srd=Grid(srd_map)
srn=Grid(srn_map)
sru=Grid(sru_map)

csrd=copy.deepcopy(srd)
csrn=copy.deepcopy(srn)
csru=copy.deepcopy(sru)


grd=Grid(np.full([gr.h,gr.w],np.inf)) #stores least distances
gru=Grid(csru.map) #unvisited nodes as True
grp=Grid(np.full([gr.h,gr.w],None)) #save path in form of points list
grn=Grid(np.full([gr.h,gr.w],False)) #nodes to get neighbours from

# sp=np.array(ss[0][0]);tsp=np.array(rfe._row_col_to_point_list(sp)) 
# ep=np.array(es[0][0]);tep=np.array(rfe._row_col_to_point_list(ep)) 

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
    if i>10000:
        break;
        
print(grp.value(pp))
# pickle.dump([grp.map,grd.map],open(r'/workspace/template-python-flask/QGIS/o_grp_grd_20_1000000.dat','wb'))
        


        
        

    
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
