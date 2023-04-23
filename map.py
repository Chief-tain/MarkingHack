import os
import folium
from folium import plugins, FeatureGroup
from folium.plugins import MarkerCluster

from database import DbAdvanced


class Map(object):

    def __init__(self):

        self.map = folium.Map(width=1300,
                             height=810,
                             location=[65, 83],
                             tiles='openstreetmap',
                             zoom_start=4,
                             min_zoom=1,
                             max_zoom=14)

        plugins.Geocoder().add_to(self.map)

        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(
            position="topright",
            separator=" | ",
            prefix="Coordinates:",
            lat_formatter=fmtr,
            lng_formatter=fmtr).add_to(self.map)

        minimap = plugins.MiniMap()
        self.map.add_child(minimap)

        plugins.Fullscreen().add_to(self.map)

        plugins.MeasureControl(position='topright',
                               primary_length_unit='meters',
                               secondary_length_unit='miles',
                               primary_area_unit='sqmeters',
                               secondary_area_unit='acres').add_to(self.map)

        folium.TileLayer('Stamen Toner').add_to(self.map)
        folium.TileLayer('Stamen Terrain').add_to(self.map)
        folium.TileLayer('Stamen Watercolor').add_to(self.map)
        folium.TileLayer('openstreetmap').add_to(self.map)
        folium.TileLayer('cartodbpositron').add_to(self.map)
        folium.TileLayer('cartodbdark_matter').add_to(self.map)

        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite',
            overlay=False,
            control=True
        ).add_to(self.map)

        plugins.Draw().add_to(self.map)

        self.marker_cluster = MarkerCluster(name='Clusters').add_to(self.map)
        self.marker_points = FeatureGroup(name='All markers', show=False).add_to(self.map)

        folium.LayerControl().add_to(self.map)

    def add_points(self):
        self.db = DbAdvanced()
        self.db.torg_points()

        for element in self.db.draw_info:
            folium.Marker(location=[element[1], element[2]],
                          popup=element[0],
                          tooltip=element[0],
                          icon=folium.Icon(color='orange', icon="info-sign")).add_to(self.marker_cluster)
            folium.Marker(location=[element[1], element[2]],
                          popup=element[0],
                          tooltip=element[0],
                          icon=folium.Icon(color='orange', icon="info-sign")).add_to(self.marker_points)

        map_name = 'marking_hack.html'
        self.map.save(map_name)

    def add_gtin_points(self, gtin):
        self.gtin_db = DbAdvanced()
        self.gtin_db.create_vvod_gtin_map(gtin)

        for key, value in self.gtin_db.gtin_draw_info_final.items():
            folium.Marker(location=[key[1], key[2]],
                          popup=value,
                          tooltip=key[0] + ' - ' + str(len(value)) + ' событие(й)',
                          icon=folium.Icon(color='orange', icon="info-sign")).add_to(self.marker_points)
            folium.Marker(location=[key[1], key[2]],
                          popup=value,
                          tooltip=key[0] + ' - ' + str(len(value)) + ' событие(й)',
                          icon=folium.Icon(color='orange', icon="info-sign")).add_to(self.marker_cluster)

            folium.Circle(location=(key[1], key[2]),
                            radius=30000*len(value), color='orange',
                            fill_opacity=0.5,
                            fill_color='orange').add_to(self.marker_points)
            folium.Circle(location=(key[1], key[2]),
                            radius=30000 * len(value), color='orange',
                            fill_opacity=0.5,
                            fill_color='orange').add_to(self.marker_cluster)

        gtin_map_name = 'gtin_marking_hack.html'
        self.map.save(gtin_map_name)

    def add_gtin_points_vivod(self, gtin):
        self.gtin_db_vivod = DbAdvanced()
        self.gtin_db_vivod.create_vivod_gtin_map(gtin)

        for key, value in self.gtin_db_vivod.gtin_draw_info_vivod_final.items():
            folium.Marker(location=[key[1], key[2]],
                          popup=value,
                          tooltip=key[0] + ' - ' + str(len(value)) + ' событие(й)',
                          icon=folium.Icon(color='green', icon="info-sign")).add_to(self.marker_points)
            folium.Marker(location=[key[1], key[2]],
                          popup=value,
                          tooltip=key[0] + ' - ' + str(len(value)) + ' событие(й)',
                          icon=folium.Icon(color='green', icon="info-sign")).add_to(self.marker_cluster)

            folium.Circle(location=(key[1], key[2]),
                          radius=3000 * len(value), color='green',
                          fill_opacity=0.5,
                          fill_color='green').add_to(self.marker_points)
            folium.Circle(location=(key[1], key[2]),
                          radius=3000 * len(value), color='green',
                          fill_opacity=0.5,
                          fill_color='green').add_to(self.marker_cluster)

        gtin_map_name = 'gtin_marking_hack_vivod.html'
        self.map.save(gtin_map_name)

    def add_gtin_points_total(self, gtin):
        self.total_db = DbAdvanced()
        self.total_db.create_vvod_gtin_map(gtin)
        self.total_db.create_vivod_gtin_map(gtin)

        for key, value in self.total_db.gtin_draw_info_final.items():
            folium.Marker(location=[key[1], key[2]],
                          popup=value,
                          tooltip=key[0] + ' - ' + str(len(value)) + ' событие(й)',
                          icon=folium.Icon(color='orange', icon="info-sign")).add_to(self.marker_points)
            folium.Marker(location=[key[1], key[2]],
                          popup=value,
                          tooltip=key[0] + ' - ' + str(len(value)) + ' событие(й)',
                          icon=folium.Icon(color='orange', icon="info-sign")).add_to(self.marker_cluster)

            folium.Circle(location=(key[1], key[2]),
                          radius=30000 * len(value), color='orange',
                          fill_opacity=0.5,
                          fill_color='orange').add_to(self.marker_points)
            folium.Circle(location=(key[1], key[2]),
                          radius=30000 * len(value), color='orange',
                          fill_opacity=0.5,
                          fill_color='orange').add_to(self.marker_cluster)

        for key, value in self.total_db.gtin_draw_info_vivod_final.items():
            folium.Marker(location=[key[1], key[2]],
                          popup=value,
                          tooltip=key[0] + ' - ' + str(len(value)) + ' событие(й)',
                          icon=folium.Icon(color='green', icon="info-sign")).add_to(self.marker_points)
            folium.Marker(location=[key[1], key[2]],
                          popup=value,
                          tooltip=key[0] + ' - ' + str(len(value)) + ' событие(й)',
                          icon=folium.Icon(color='green', icon="info-sign")).add_to(self.marker_cluster)

            folium.Circle(location=(key[1], key[2]),
                          radius=3000 * len(value), color='green',
                          fill_opacity=0.5,
                          fill_color='green').add_to(self.marker_points)
            folium.Circle(location=(key[1], key[2]),
                          radius=3000 * len(value), color='green',
                          fill_opacity=0.5,
                          fill_color='green').add_to(self.marker_cluster)

        total_map_name = 'marking_hack_total.html'
        self.map.save(total_map_name)

    def routes(self, gtin):
        self.route_db = DbAdvanced()
        self.route_db.route(gtin)

        for route in self.route_db.paths:
            plugins.AntPath([[route[1], route[2]], [route[5], route[6]]]).add_to(self.map)

            folium.Marker(location=[route[1], route[2]],
                          tooltip=route[0],
                          icon=folium.Icon(color='green', icon="info-sign")).add_to(self.marker_points)
            folium.Marker(location=[route[1], route[2]],
                          tooltip=route[0],
                          icon=folium.Icon(color='green', icon="info-sign")).add_to(self.marker_cluster)
            folium.Marker(location=[route[5], route[6]],
                          tooltip=route[4],
                          icon=folium.Icon(color='orange', icon="info-sign")).add_to(self.marker_points)
            folium.Marker(location=[route[5], route[6]],
                          tooltip=route[4],
                          icon=folium.Icon(color='orange', icon="info-sign")).add_to(self.marker_cluster)

        route_map_name = 'marking_hack_route.html'
        self.map.save(route_map_name)
