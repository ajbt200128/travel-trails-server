import requests

# set a name for search
search_name = "Lincoln Memorial"

# set bounding box coordinates
lat_min = 38.88030972164946
long_min = -77.0560455322265
lat_max = 38.90529438572799
long_max = -77.01982498168944


def flickr_search():
    api_key = "bca0e9bd7c87fb57ef34c3a5aaf90afb"
    lat = "38.889248"
    lon = "-77.050636"
    photo_search_query = """https://www.flickr.com/services/rest/
    ?method=flickr.photos.search&api_key={}&lat={}&lon={}&
    format=json&nojsoncallback=1"""

    photo_search_query = photo_search_query.format(api_key, lat, lon)

    photo_ids = []

    # do photo search at lat, lon
    response = requests.get(photo_search_query)
    photo_search_response = response.json()
    # print(photo_search_response)

    # check if valid response
    if photo_search_response["stat"] == "fail":
        print(photo_search_response["message"])
    elif photo_search_response["stat"] == "ok":
        # check if a positive number of images
        if photo_search_response["photos"]["total"] > 0:

            # retrieve image ids
            print(len(photo_search_response["photos"]["photo"]))
            for photo in photo_search_response["photos"]["photo"]:
                photo_ids.append(str(photo["id"]))

            print(photo_ids)
            # query for image urls
            for id in photo_ids:
                url_query = """https://www.flickr.com/services/rest/
                ?method=flickr.photos.getSizes&api_key={}&photo_id={}
                &format=json&nojsoncallback=1"""
                url_query = url_query.format(api_key, id)

                response = requests.get(url_query)
                url_response = response.json()
                # get the medium sized image (6)
                print(url_response["sizes"]["size"][6]["source"])


flickr_search()
