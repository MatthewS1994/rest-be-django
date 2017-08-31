import datetime
import json
import urllib
import urllib2

from django.core.management.base import BaseCommand

from app_modules.endpoints.models import Location

places = [
    'Cape Town',
]
baseurl = "https://query.yahooapis.com/v1/public/yql?"


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        print 'Cleaning Database'

        for item in Location.objects.all():
            if item:
                print 'Deleting: ' + item.name + ' ' + item.woeid
                item.delete()

        print 'Database Cleaned'
        print '..................................'
        print 'Starting Import Geo Locations'
        counter = 0
        for item in places:
            started = datetime.datetime.now()
            yql_query = "select * from geo.places where text='{city}' limit 1".format(city=item)
            yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
            result = urllib2.urlopen(yql_url).read()
            data = json.loads(result)
            location = Location()
            location.name = data['query']['results']['place']['name']
            location.lang = data['query']['results']['place']['lang']
            location.popRank = data['query']['results']['place']['popRank']
            location.woeid = data['query']['results']['place']['woeid']
            location.uri = data['query']['results']['place']['uri']

            location.admin1_content = data['query']['results']['place']['admin1']['content']
            location.admin1_woeid = data['query']['results']['place']['admin1']
            location.admin1_type = data['query']['results']['place']['admin1']

            location.admin2_content = data['query']['results']['place']['admin2']
            location.admin2_woeid = data['query']['results']['place']['admin2']
            location.admin2_type = data['query']['results']['place']['admin2']

            location.admin3_content = data['query']['results']['place']['admin3']
            location.admin3_woeid = data['query']['results']['place']['admin3']
            location.admin3_type = data['query']['results']['place']['admin3']

            location.latitude = data['query']['results']['place']['centroid']['latitude']
            location.longitude = data['query']['results']['place']['centroid']['longitude']

            if data['query']['results']['place']['locality1']:
                location.locality_content = data['query']['results']['place']['locality1']['content']
                location.locality_woeid = data['query']['results']['place']['locality1']['woeid']
                location.locality_type = data['query']['results']['place']['locality1']['type']

            location.country_content = data['query']['results']['place']['country']['content']
            location.country_woeid = data['query']['results']['place']['country']['woeid']
            location.country_code = data['query']['results']['place']['country']['code']
            location.country_type = data['query']['results']['place']['country']['type']

            location.northEast_latitude = data['query']['results']['place']['boundingBox']['northEast']['latitude']
            location.northEast_longitude = data['query']['results']['place']['boundingBox']['northEast']['longitude']

            location.southWest_latitude = data['query']['results']['place']['boundingBox']['southWest']['latitude']
            location.southWest_longitude = data['query']['results']['place']['boundingBox']['southWest']['longitude']

            location.save()
            counter += 1
            print 'Saving...... '
            print str(counter) + '. '
            location_saved = {
                'New Id': location.id,
                'Name': location.name,
                'WOEID': location.woeid
            }
            print json.dumps(location_saved, indent=3)
            finished = datetime.datetime.now()
            print 'Completed In' + format(float((finished - started).total_seconds()), '.2f')

        print '########################################################################'
        print '------------------------------------------------------------------------'
        print '  _____   _____       ___  ___   _____   _       _____   _____   _____  '
        print ' /  ___| /  _  \     /   |/   | |  _  \ | |     | ____| |_   _| | ____| '
        print ' | |     | | | |    / /|   /| | | |_| | | |     | |__     | |   | |__   '
        print ' | |     | | | |   / / |__/ | | |  ___/ | |     |  __|    | |   |  __|  '
        print ' | |___  | |_| |  / /       | | | |     | |___  | |___    | |   | |___  '
        print ' \_____| \_____/ /_/        |_| |_|     |_____| |_____|   |_|   |_____| '
        print '------------------------------------------------------------------------'
        print '########################################################################'
