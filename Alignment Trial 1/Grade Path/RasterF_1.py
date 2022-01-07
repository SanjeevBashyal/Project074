# import pickle
from math import floor


class RasterF:
    def __init__(self, raster_layer):
        self.ly = raster_layer
        self.xres = raster_layer.rasterUnitsPerPixelX()
        self.yres = raster_layer.rasterUnitsPerPixelY()
        self.provider = raster_layer.dataProvider()
        self.extent = self.provider.extent()

    def get_block(self, band):
        return self.provider.block(band, self.extent, self.ly.width(), self.ly.height())

    def block2matrix(self, block):
        contains_negative = False
        matrix = [
            [
                None if block.isNoData(i, j) else block.value(i, j)
                for j in range(block.width())
            ]
            for i in range(block.height())
        ]

        #    for l in matrix:
        #        for v in l:
        #            if v is not None:
        #                if v < 0:
        #                    contains_negative = True

        return matrix, contains_negative

    def ij_to_point(self, ij):
        x = (ij[1] + 0.5) * self.xres + self.extent.xMinimum()
        y = self.extent.yMaximum() - (ij[0] + 0.5) * self.yres
        return QgsPoint(x, y)

    def ijs_to_points(self, ijs):
        points = list(map(lambda ij: self.ij_to_point(ij), ijs))
        return points

    def ij_to_xy(self, ij):
        x = (ij[1] + 0.5) * self.xres + self.extent.xMinimum()
        y = self.extent.yMaximum() - (ij[0] + 0.5) * self.yres
        return [x, y]

    def ijs_to_xys(self, ijs):
        xys = list(map(lambda ij: self.ij_to_xy(ij), ijs))
        return xys

    def point_to_ij(self, point):
        j = floor((point.x() - self.extent.xMinimum()) / self.xres)
        i = floor((self.extent.yMaximum() - point.y()) / self.yres)
        return i, j

    def features_to_ij_and_info(self, point_features, block=None):
        ijs_and_info = []

        # if extent.isNull() or extent.isEmpty:
        #     return list(col_rows)

        for point_feature in point_features:
            if point_feature.hasGeometry():

                point_geom = point_feature.geometry()
                if point_geom.wkbType() == QgsWkbTypes.Point:
                    point = point_geom.asPoint()
                    if self.extent.contains(point):
                        ij = self.point_to_ij(point)
                        if block is not None:
                            value = block.value(ij[0], ij[1])
                            ijs_and_info.append((ij, value, point, point_feature.id()))
                        else:
                            ijs_and_info.append((ij, None, point, point_feature.id()))

                elif point_geom.wkbType() == QgsWkbTypes.MultiPoint:
                    multi_points = point_geom.asMultiPoint()
                    for point in multi_points:
                        if self.extent.contains(point):
                            ij = self.point_to_ij(point)
                            ijs_and_info.append((ij, point, point_feature.id()))

        return ijs_and_info

    @staticmethod
    def create_path_feature_from_points(path_points, fid):
        polyline = QgsGeometry.fromPolyline(path_points)
        feature = QgsFeature()
        feature.setGeometry(polyline)
        feature.setId(fid)
        return feature


# get data
# aspect = QgsProject.instance().mapLayersByName('hshade_nagarkot')[0]
# slope=QgsProject.instance().mapLayersByName('slope')[0]
# ele=QgsProject.instance().mapLayersByName('Elevation_TM')[0]
# stp=QgsProject.instance().mapLayersByName('stp_tm')[0]
# etp=QgsProject.instance().mapLayersByName('etp_tm')[0]
# rf=RasterF(aspect)
# rfs=RasterF(slope)
# block=rf.get_block(1)
# blocks=rfs.get_block(1)
##mat,out=rf.block2matrix(block)
##mats,outs=rfs.block2matrix(blocks)
##pickle.dump(mat, open("C:\\Users\\SANJEEV BASHYAL\\Documents\\QGIS\\Grade Path\\mat.dat", "wb"))
# ss=rf.features_to_tuples(list(stp.getFeatures()),block)
# es=rf.features_to_tuples(list(etp.getFeatures()),block)
##del(block,blocks)
