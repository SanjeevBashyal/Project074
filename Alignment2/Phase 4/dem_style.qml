<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" version="3.16.15-Hannover" styleCategories="AllStyleCategories" maxScale="0" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal mode="0" fetchMode="0" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour" enabled="false"/>
    </provider>
    <rasterrenderer opacity="1" classificationMin="369.9853821" alphaBand="-1" classificationMax="1228.7043457" type="singlebandpseudocolor" band="1" nodataColor="">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" clip="0" maximumValue="1228.7043457" minimumValue="369.98538209999998" classificationMode="2" labelPrecision="4">
          <colorramp name="[source]" type="gradient">
            <prop v="90,157,255,255" k="color1"/>
            <prop v="255,255,255,255" k="color2"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="0.333;48,177,41,255:0.666;214,83,35,255" k="stops"/>
          </colorramp>
          <item label="369.9854" alpha="255" value="369.9853820800781" color="#5a9dff"/>
          <item label="465.3986" alpha="255" value="465.3986002604167" color="#4ca4b8"/>
          <item label="560.8118" alpha="255" value="560.8118184407552" color="#3eaa70"/>
          <item label="656.2250" alpha="255" value="656.2250366210938" color="#30b129"/>
          <item label="751.6383" alpha="255" value="751.6382548014324" color="#689227"/>
          <item label="847.0515" alpha="255" value="847.0514729817709" color="#9f7225"/>
          <item label="942.4647" alpha="255" value="942.4646911621094" color="#d65323"/>
          <item label="1037.8779" alpha="255" value="1037.877909342448" color="#e48d6d"/>
          <item label="1133.2911" alpha="255" value="1133.2911275227866" color="#f1c6b6"/>
          <item label="1228.7043" alpha="255" value="1228.704345703125" color="#ffffff"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" gamma="1" contrast="0"/>
    <huesaturation colorizeBlue="128" saturation="0" colorizeGreen="128" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
