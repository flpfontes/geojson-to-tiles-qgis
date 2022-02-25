import sys
import os
sys.path.extend(['C:/OSGeo4W64/apps/qgis/python','C:/OSGeo4W64/apps/Python37/lib/site-packages'])
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'C:/OSGeo4W64/apps/Qt5/plugins'
os.environ['PATH'] += ';C:/OSGeo4W64/apps/qgis/bin;C:/OSGeo4W64/apps/Qt5/bin'
os.environ['PROJ_LIB'] = 'C:/OSGeo4W64/share/proj'



sys.path.append('C:/OSGeo4W64/apps/qgis/python')
sys.path.append('C:/OSGeo4W64/apps/qgis/python/plugins')
sys.path.append('C:/OSGeo4W64/apps/qgis/python/plugins/processing')

from qgis.core import QgsVectorLayer, QgsProject
from qgis.PyQt.QtGui import QColor
import processing
from processing.core.Processing import Processing

Processing.initialize()


def geojson_to_tile(lyr_point, lyr_polygon, min_zoom, max_zoom, output_dir):

    vlayer_polygon = QgsVectorLayer(lyr_polygon, "polygon", "ogr")
    vlayer_point = QgsVectorLayer(lyr_point, "point", "ogr")

    QgsProject.instance().addMapLayer(vlayer_polygon)
    QgsProject.instance().addMapLayer(vlayer_point)


    vlayer_polygon.renderer().symbol().setColor(QColor.fromRgb(50,50,250))
    vlayer_polygon.triggerRepaint()

    vlayer_point.renderer().symbol().setColor(QColor.fromRgb(255,0,255))
    vlayer_point.triggerRepaint()


    alg_params = {
        'BACKGROUND_COLOR': QColor(0, 0, 0, 0),
        'DPI': 96,
        'EXTENT': lyr_polygon,
        'METATILESIZE': 4,
        'OUTPUT_DIRECTORY': output_dir,
        'QUALITY': 75,
        'TILE_FORMAT': 0,
        'TILE_HEIGHT': 256,
        'TILE_WIDTH': 256,
        'TMS_CONVENTION': False,
        'ZOOM_MAX': max_zoom,
        'ZOOM_MIN': min_zoom
    }

    processing.run("qgis:tilesxyzdirectory", alg_params)


path_layer_point = sys.argv[1]
path_layer_polygon = sys.argv[2]
min_zoom = sys.argv[3]
max_zoom = sys.argv[4]
path  = sys.argv[5]


geojson_to_tile(path_layer_point, path_layer_polygon, min_zoom, max_zoom, path)