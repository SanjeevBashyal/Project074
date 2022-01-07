import pickle
from pathlib import Path

path = str(Path.home()) + "\\Desktop\\Project074"
Path(path).mkdir(parents=True, exist_ok=True)
ele = QgsProject.instance().mapLayersByName("Elevation_TM_1000")[0]
stp = QgsProject.instance().mapLayersByName("stp_tm")[0]
etp = QgsProject.instance().mapLayersByName("etp_tm")[0]
rfe = RasterF(ele)
blocke = rfe.get_block(1)
# mate,oute=rfe.block2matrix(blocke)
ss = rfe.features_to_ij_and_info(list(stp.getFeatures()), blocke)
es = rfe.features_to_ij_and_info(list(etp.getFeatures()), blocke)

gd = 20  # design grade
ad = 10  # slope scaling in weightage

# gr=Grid(mate);del(mate)
gr_ele = Grid(rfe.block2matrix(blocke)[0])
gr_n = Grid(np.full([gr_ele.h, gr_ele.w], None))  # stores neighbouring points
gr_d = Grid(np.full([gr_ele.h, gr_ele.w], None))  # stores distances to gr_n
gr_u = Grid(np.full([gr_ele.h, gr_ele.w], None))  # stores if useful node
for i in range(gr_ele.h):
    for j in range(gr_ele.w):
        ij = np.array([i, j])
        if not gr_ele.is_valid(ij):
            continue

        nei = gr_ele.neighbors_ext(ij)
        if nei.size == 0:
            continue

        xy0 = np.array(rfe.ij_to_xy(ij))
        nei_xys = np.array(rfe.ijs_to_xys(nei))
        xy_diff = nei_xys - xy0
        xy_dist = np.linalg.norm(xy_diff, axis=1)

        e_xy0 = gr_ele.value(ij)
        e_nei = gr_ele.values(nei)
        e_diff = e_nei - e_xy0

        slope = e_diff / xy_dist * 100

        dslope_index = np.where(np.abs(slope) < gd)[0]
        if dslope_index.size == 0:
            continue
        modified_dist = xy_dist[dslope_index] * (
            1 + ad * np.abs(slope[dslope_index]) / 100
        )
        oxsl = modified_dist.argsort()

        gr_n.insert(nei[dslope_index][oxsl], ij)  # nei to dnei to sorted dnei
        gr_d.insert(modified_dist[oxsl], ij)
        gr_u.insert(True, ij)

pickle.dump(
    [gr_ele.map, ss[0][0], es[0][0], gr_d.map, gr_n.map, gr_u.map],
    open(path + "\\dump.dat", "wb"),
)
