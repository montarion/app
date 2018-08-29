import json, requests, sys, traceback
from time import sleep

class location:
    def __init__(self):
        self.i = 0

    def search(self, latitude, longtitude):
        url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + latitude + ',' + longtitude + '&sensor=true'
        #---needed conversion---#
        r = requests.get(url)
        test1 = r.text
        test = str(test1)
        string = json.loads(str(test))
        try:
            result = string['results'][0]["formatted_address"]
            components = string['results'][0]["address_components"]
            for _ in components:
                for key, value in _.items():
                    if key == 'types' and 'locality' in value:
                        city = _['long_name']
                        return city
        except:
            traceback.print_exc()
            print("error! this is the url I used \n" + str(url) + "\nAnd these are the coordinates \n" + str(latitude), ',', str(longtitude))
            #print("retrying in 5 seconds!")
            self.i += 1
            print(self.i)
            sleep(5)
            self.search(latitude, longtitude)
            
