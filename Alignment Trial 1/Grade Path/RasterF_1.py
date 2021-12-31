#import pickle
from math import floor

class RasterF:
    def __init__(self, raster_layer):
        self.ly = raster_layer
        self.xres = raster_layer.rasterUnitsPerPixelX()
        self.yres = raster_layer.rasterUnitsPerPixelY()
        self.provider=raster_layer.dataProvider();
        self.extent=self.provider.extent();
    
    def get_block(self,band):
        block=self.provider.block(band,self.extent,self.ly.width(),self.ly.height())
        return block
    
    def block2matrix(self,block):
        contains_negative = False
        matrix = [[None if block.isNoData(i, j) else block.value(i, j) for j in range(block.width())]
                  for i in range(block.height())]

    #    for l in matrix:
    #        for v in l:
    #            if v is not None:
    #                if v < 0:
    #                    contains_negative = True

        return matrix, contains_negative
        
    def create_points_from_path(self, min_cost_path):
        path_points = list(
            map(lambda row_col: self._row_col_to_point(row_col), min_cost_path))
        return path_points
        
    def create_points_from_path_list(self, min_cost_path):
        path_points = list(
            map(lambda row_col: self._row_col_to_point_list(row_col), min_cost_path))
        return path_points

    def _point_to_row_col(self,pointxy):

        col = floor((pointxy.x() - self.extent.xMinimum()) / self.xres)
        row = floor((self.extent.yMaximum() - pointxy.y()) / self.yres)

        return row, col
        
    def _row_col_to_point(self,row_col):

        x = (row_col[1] + 0.5) * self.xres + self.extent.xMinimum()
        y = self.extent.yMaximum() - (row_col[0] + 0.5) * self.yres
        return QgsPoint(x, y)
        
    def _row_col_to_point_list(self,row_col):

        x = (row_col[1] + 0.5) * self.xres + self.extent.xMinimum()
        y = self.extent.yMaximum() - (row_col[0] + 0.5) * self.yres
        return [x,y]
        
    def features_to_tuples(self,point_features,block=None):
        row_cols = []

        # if extent.isNull() or extent.isEmpty:
        #     return list(col_rows)

        for point_feature in point_features:
            if point_feature.hasGeometry():

                point_geom = point_feature.geometry()
                if point_geom.wkbType() == QgsWkbTypes.MultiPoint:
                    multi_points = point_geom.asMultiPoint()
                    for pointxy in multi_points:
                        if self.extent.contains(pointxy):
                            row_col = self._point_to_row_col(pointxy)
                            row_cols.append((row_col, pointxy, point_feature.id()))

                elif point_geom.wkbType() == QgsWkbTypes.Point:
                    pointxy = point_geom.asPoint()
                    if self.extent.contains(pointxy):
                        row_col = self._point_to_row_col(pointxy)
                        if block is not None:
                            value=block.value(row_col[0],row_col[1])
                            row_cols.append((row_col,value, pointxy, point_feature.id()))
                        else:
                            row_cols.append((row_col, pointxy, point_feature.id()))

        return row_cols
    
    @staticmethod
    def create_path_feature_from_points(path_points,id):
        polyline = QgsGeometry.fromPolyline(path_points)
        feature = QgsFeature()
        feature.setGeometry(polyline)
        feature.setId(id)
        return feature
        



#get data
#aspect = QgsProject.instance().mapLayersByName('hshade_nagarkot')[0]
#slope=QgsProject.instance().mapLayersByName('slope')[0]
#ele=QgsProject.instance().mapLayersByName('Elevation_TM')[0]
#stp=QgsProject.instance().mapLayersByName('stp_tm')[0]
#etp=QgsProject.instance().mapLayersByName('etp_tm')[0]
#rf=RasterF(aspect)
#rfs=RasterF(slope)
#block=rf.get_block(1)
#blocks=rfs.get_block(1)
##mat,out=rf.block2matrix(block)
##mats,outs=rfs.block2matrix(blocks)
##pickle.dump(mat, open("C:\\Users\\SANJEEV BASHYAL\\Documents\\QGIS\\Grade Path\\mat.dat", "wb"))
#ss=rf.features_to_tuples(list(stp.getFeatures()),block)
#es=rf.features_to_tuples(list(etp.getFeatures()),block)
##del(block,blocks)

