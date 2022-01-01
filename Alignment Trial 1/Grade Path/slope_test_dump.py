#import pickle
ele=QgsProject.instance().mapLayersByName('Elevation_TM_1000')[0]
stp=QgsProject.instance().mapLayersByName('stp_tm')[0]
etp=QgsProject.instance().mapLayersByName('etp_tm')[0]
rfe=RasterF(ele)
#extent=[rfe.extent.xMinimum(),rfe.extent.yMinimum(),rfe.extent.xMaximum(),rfe.extent.yMaximum()]
blocke=rfe.get_block(1)
#mate,oute=rfe.block2matrix(blocke)
ss=rfe.features_to_tuples(list(stp.getFeatures()),blocke)
es=rfe.features_to_tuples(list(etp.getFeatures()),blocke)
#pickle.dump([rfe.xres,rfe.yres,extent, mate, ss[0][0],es[0][0]], open("C:\\Users\\SANJEEV BASHYAL\\Documents\\QGIS\\Grade Path\\mate.dat", "wb"))