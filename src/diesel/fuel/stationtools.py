from django.core.exceptions import ObjectDoesNotExist
from urllib2 import urlopen, HTTPError, URLError
from BeautifulSoup import BeautifulSoup
from diesel.fuel.models import Station, FuelPrice
from urllib import quote_plus
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse
from matplotlib import pyplot


def searchQuery(location, num_results, centane_filter=None):
    search_url = 'http://local.yahooapis.com/LocalSearchService/V3/localSearch?appid=1rnOAGjV34FSCwQczSLF_c68OT7Axcx2SHRhkggI3_GKoksidy.GucjpgqNR0gI-&query=gas&'
    search_url += '&category=96925722'
    search_url += '&sort=distance'
    search_url += '&location=' + quote_plus(location.strip())
    search_url += '&results=' + num_results
    results = doQuery(search_url)
    return processResults(results, centane_filter)

def doQuery(url):
    results = []
    try:
        print url
        data = urlopen(url).read()
        soup = BeautifulSoup(data)
        #print soup.prettify()
        #results_xml = soup.findAll('result')
        for result in soup.findAll('result'):
            name = result.find('title').find(text=True)
            address = result.find('address').find(text=True)
            city = result.find('city').find(text=True)
            state = result.find('state').find(text=True)
            phone = result.find('phone').find(text=True)
            distance = result.find('distance').find(text=True)
            results.append({"name": str(name) , 
                            "address": str(address), 
                            "city": str(city), 
                            "state": str(state),
                            "phone": str(phone),
                            "distance": str(distance)
                            }
                            )
    except HTTPError, e:
        print "HTTP error: %d" % e.code
    except URLError, e:
        print "Network error: %s" % e.reason.args[1]
    return results

def processResults(queryResults, centane_filter=None):
    stationList = []
    for result in queryResults:
        station = None
        #see if this station is being tracked already
        try:
            station = Station.objects.get(address=result['address'])
            print 'already existing station: ' + station.name
            station.name = result['name']
            station.city = result['city']
            station.state = result['state']
            station.phone = result['phone']
            result['has_separate_pumps'] = station.has_separate_diesel_pumps
            result['diesel_grade'] = station.diesel_grade
            result['current_price'] = station.current_price()
            result['pk'] = station.id
        except ObjectDoesNotExist:
            #create new
            station = Station.objects.create()
            print 'creating new station: ' + result['name']
            station.name = result['name']
            station.address = result['address']
            station.city = result['city']
            station.state = result['state']
            station.phone = result['phone']
            result['has_separate_pumps'] = '-'
            result['diesel_grade'] = '-'
            result['current_price'] = '-'
            result['pk'] = station.id
        station.save()
        if station:
            if centane_filter:
                if station.diesel_grade == centane_filter:
                    stationList.append(result)
            else:
                stationList.append(result)
    return stationList

def buildPriceGraph(id):
    prices = FuelPrice.objects.filter(station=id).order_by('created')
    y = []
    x = []
    for price in prices:
        y.append(price.price)
        x.append(price.created)
    fig=Figure()
    ax=fig.add_subplot(111)

    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvasAgg(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    pyplot.close(fig)
    return response