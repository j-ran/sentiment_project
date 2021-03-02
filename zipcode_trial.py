import json
import urllib.request

import os
API_KEY = os.environ['GOOGLE_API_KEY']
GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def geocode(address):
    # Join the parts of the URL together into one string.
    params = urllib.parse.urlencode({"address": address, "key": API_KEY,})
    url = f"{GEOCODE_BASE_URL}?{params}"

    result = json.load(urllib.request.urlopen(url))

    if result["status"] in ["OK", "ZERO_RESULTS"]:
        return result["results"]

    raise Exception(result["error_message"])


if __name__ == "__main__":
    # below here only runs if the whole file is called;
    # if, for instance, I just call the filename into another file, 
    # then the following lines will not run
    results = geocode(address="43214")
    print(json.dumps([s["formatted_address"] for s in results], indent=2))

# Output:

# [
#   "Columbus, OH, USA"
# ]

##### NOTES FROM KAT (Katrina Huber-Juma) ON HOW TO PARSE JSON OBJECT #####
# response is an object
# response has a method called .json() that returns a dictionary
# that dictionary has two keys: results and status
    # results has a list of dictionaries (except there is only one in this case)
        # that dictionary is response.json()['results'][0][]


# response_dict = response.json()
# results = response_dict['results']
# for result in results:  
#   address_components = result['address_components'] # is the list that starts on line 51
#   for component in address_components:
#       print(component['short_name'])
        # to get to 'OH' go to the third component and the key called 'short_name'
#       print(address_components[3]['short_name'])


{
   "results" : [       # respoonse.json()['results'] is the list that opens here
      {    # this is the start of respoonse.json()['results'][0] the zeroth item in results
         "address_components" : [
            {
               "long_name" : "43214",
               "short_name" : "43214",
               "types" : [ "postal_code" ]
            },
            {
               "long_name" : "Columbus",
               "short_name" : "Columbus",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Franklin County",
               "short_name" : "Franklin County",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Ohio",
               "short_name" : "OH",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "United States",
               "short_name" : "US",
               "types" : [ "country", "political" ]
            }
         ],
         "formatted_address" : "Columbus, OH 43214, USA",
         "geometry" : {
            "bounds" : {
               "northeast" : {
                  "lat" : 40.07677,
                  "lng" : -82.9971889
               },
               "southwest" : {
                  "lat" : 40.02884290000001,
                  "lng" : -83.04652489999999
               }
            },
            "location" : {
               "lat" : 40.0480476,
               "lng" : -83.025396
            },
            "location_type" : "APPROXIMATE",
            "viewport" : {
               "northeast" : {
                  "lat" : 40.07677,
                  "lng" : -82.9971889
               },
               "southwest" : {
                  "lat" : 40.02884290000001,
                  "lng" : -83.04652489999999
               }
            }
         },
         "place_id" : "ChIJT66Ab0SMOIgRjsbe8wmUzig",
         "types" : [ "postal_code" ]
      }
   ],
   "status" : "OK"
}
