import datetime
import json
import urllib
import urllib2

from django.core.management.base import BaseCommand

from app_modules.endpoints.models import Location, WeatherLog


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        location = Location.objects.all()
        print 'Cleaning Database'

        for item in WeatherLog.objects.all():
            if item:
                print 'Deleting Weather Log: ' + item.title + ' ' + item.location.name
                item.delete()

        print 'Database Cleaned'
        print '..................................'
        print 'Starting Import Forecast'
        counter = 0
        for item in location:
            started = datetime.datetime.now()
            baseurl = "https://query.yahooapis.com/v1/public/yql?"
            yql_query = 'select * from weather.forecast where woeid in ' \
                        '(select woeid from geo.places(1) where text="{city}")' \
                .format(city=str(item.name + ', ' + item.country_code))

            yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
            result = urllib2.urlopen(yql_url).read()
            data = json.loads(result)
            if data['query']['results'] and data['query']['results']['channel']:
                weather = WeatherLog()
                weather.location = item
                weather.title = data['query']['results']['channel']['item']['title']
                weather.pressure = data['query']['results']['channel']['atmosphere']['pressure']
                weather.rising = data['query']['results']['channel']['atmosphere']['rising']
                weather.visibility = data['query']['results']['channel']['atmosphere']['visibility']
                weather.humidity = int(data['query']['results']['channel']['atmosphere']['humidity'])
                weather.date = data['query']['results']['channel']['item']['pubDate']
                weather.text = data['query']['results']['channel']['item']['condition']['text']
                weather.temp = int(data['query']['results']['channel']['item']['condition']['temp'])
                weather.city = data['query']['results']['channel']['location']['city']
                weather.region = data['query']['results']['channel']['location']['region']
                weather.country = data['query']['results']['channel']['location']['country']
                weather.sunset = data['query']['results']['channel']['astronomy']['sunset']
                weather.sunrise = data['query']['results']['channel']['astronomy']['sunrise']
                weather.wind_direction = data['query']['results']['channel']['wind']['direction']
                weather.wind_speed = data['query']['results']['channel']['wind']['speed']
                weather.wind_chill = data['query']['results']['channel']['wind']['chill']
                weather.forecast = data['query']['results']['channel']['item']['forecast']
                weather.save()
                counter += 1
                print 'Saving...... '
                print str(counter) + '. '
                location_saved = {
                    'New Id': weather.location.id,
                    'Name': weather.location.name,
                    'WOEID': weather.location.woeid
                }
                print json.dumps(location_saved, indent=3)
                finished = datetime.datetime.now()
                print 'Completed In' + format(float((finished - started).total_seconds()), '.2f')
            else:
                counter += 1
                print 'ERROR...... '
                print 'There was an error getting the forecast, Due to the location not returning data'
                print '....................................................................'
                print 'Cleaning Database'
                print 'Deleting: ' + item.name + ' ' + item.woeid
                item.delete()
                print 'Database Cleaned'
                print '....................................................................'
                finished = datetime.datetime.now()
                print 'Completed In' + format(float((finished - started).total_seconds()), '.2f')
            print str(item.name + ', ' + item.country_code)
