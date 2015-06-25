import json
import requests

def api_get_request(url):
    # In this exercise, you want to call the last.fm API to get a list of the

    # top artists in Spain.
    #
    # Once you've done this, return the name of the number 1 top artist in Spain.
    # url = "http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country=spain&api_key=e27b22bbd67942096e94f23d98014bed&format=json"
    data = requests.get(url).text
    data = json.loads(data)
    # print json.dumps(data, indent=4, sort_keys=False)

    top_artist = data["topartists"]["artist"][0]
    return top_artist['name']
    # return ... # return the top artist in Spain




print api_get_request("")