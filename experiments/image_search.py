import json

from image_tools import create_image_gallery, flickr_search

# lincoln memorial
lincoln = {
    "lat": 38.889248,
    "lon": -77.050636,
    "radius": 0.1,  # miles
    "tag": "lincoln",
    "title": "Lincoln Memorial",
    "save": "image_gallery_lincoln.html",
}

# hippo
hippo = {
    "lat": 38.899534358379164,
    "lon": -77.04674263500051,
    "radius": 0.01,  # miles
    "tag": "hippo",
    "title": "River Horse Statue",
    "save": "image_gallery_hippo.html",
}


if __name__ == "__main__":

    # read API key from file
    with open("api_keys.json") as f:
        keys = json.load(f)
        if "flickr_api_key" in keys:
            flickr_api_key = str(keys["flickr_api_key"])

    # get photo urls at coordinates
    photo_urls = flickr_search(
        api_key=flickr_api_key, parameters=hippo
    )  # parameters = lincoln, hippo

    # extract image ids
    # use these static urls for testing without the api
    create_image_gallery(photo_urls, parameters=hippo)  # parameters = lincoln, hippo
