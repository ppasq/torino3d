import json
import psycopg2
import urllib

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

class Home(View):
    """Render home page"""

    def get(self, request, *args, **kwargs):

        bbox_wkt = urllib.unquote(request.GET.get('bbox_wkt'))
        print bbox_wkt

        # Database connection
        conn = psycopg2.connect("host=hostname dbname=postgres user=username password=pwd")
        
        # Database cursor
        cur = conn.cursor()
        # Query
        cur.execute('SELECT row_to_json(fc) FROM ( SELECT \'FeatureCollection\' As type, \
         array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type, \
          ST_AsGeoJSON(ST_Transform(lg.the_geom,4326))::json As geometry, \
          row_to_json((SELECT l FROM (SELECT height) As l)) As properties FROM \
           torino_buildings As lg WHERE ST_Within(lg.the_geom, \
            ST_Transform(ST_GeomFromText(%s,4326),4326)) LIMIT 100000) As f )  \
            As fc;',[bbox_wkt])
        array = cur.fetchall()

        # ST_Transform can be removed since no transformation is needed

        # Format JSON data
        jsondata = json.dumps(array[0])
        # Hack to remove Ptthon list brackets
        jsondata = jsondata[1:-1]
        # Remove escaped strings
        # jsondata = jsondata.replace("\\","")
        # Print the data
        return HttpResponse(jsondata)