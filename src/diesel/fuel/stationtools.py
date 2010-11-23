from urllib2 import urlopen, HTTPError, URLError
from BeautifulSoup import BeautifulSoup

def searchQuery(location, num_results):
    search_url = 'http://local.yahooapis.com/LocalSearchService/V3/localSearch?appid=1rnOAGjV34FSCwQczSLF_c68OT7Axcx2SHRhkggI3_GKoksidy.GucjpgqNR0gI-&query=gas&'
    search_url += '&category=96925722'
    search_url += '&sort=distance'
    search_url += '&location=' + location.strip()
    search_url += '&results=' + num_results
    return doQuery(search_url)

def doQuery(url):
    results = []
    try:
        print url
        data = urlopen(url).read()
        soup = BeautifulSoup(data)
        #print soup.prettify()
        #results_xml = soup.findAll('result')
        for result in soup.findAll('result'):
            #print result
            #title = result.find('title', limit=1)
            #address = result.find('address', limit=1)
            #city = result.find('city', limit=1)
            #state = result.find('state', limit=1)
            #phone = result.find('phone', limit=1)
            #distance = result.find('distance', limit=1)
            title = result.find('title').find(text=True)
            address = result.find('address').find(text=True)
            city = result.find('city').find(text=True)
            state = result.find('state').find(text=True)
            phone = result.find('phone').find(text=True)
            distance = result.find('distance').find(text=True)
            results.append({"title": str(title) , 
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