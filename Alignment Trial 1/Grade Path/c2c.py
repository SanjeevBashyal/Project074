lc = QgsProject.instance().mapLayersByName('dem contour')[0]
a=QgsFeatureRequest()
a.setFilterExpression("elev=1200")
fts=lc.getFeatures(a)
c=0
for feat in fts:
    geom=feat.geometry()
    print(geom)
    c=c+1
#    break
feat.attribute("id")
feat.attribute("elev")
print(c)