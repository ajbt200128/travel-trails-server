import json

from image_tools import create_image_gallery, flickr_search

# lincoln memorial
lincoln = {
    "latitude": 38.889248,
    "longitude": -77.050636,
    "radius": 0.1,  # miles
    "tag": "lincoln",
    "title": "Lincoln Memorial",
    "save": "image_gallery_lincoln.html",
}

# hippo
hippo = {
    "latitude": 38.899534358379164,
    "longitude": -77.04674263500051,
    "radius": 0.01,  # miles
    "tag": "hippo",
    "title": "River Horse Statue",
    "save": "image_gallery_hippo.html",
}


if __name__ == "__main__":
    parameters=hippo # lincoln, hippo

    try:
        # read API key from file
        with open("api_keys.json") as f:
            keys = json.load(f)
            if "flickr_api_key" in keys:
                flickr_api_key = str(keys["flickr_api_key"])
            else:
                raise ValueError("flickr_api_key not found in file")
    except Exception as e:
        raise e

    print(flickr_api_key)
    quit()
    # get photo urls at coordinates
    photo_urls = flickr_search(
        api_key=flickr_api_key, parameters=parameters
    )

    # extract image ids
    html_gallery = create_image_gallery(photo_urls, parameters=parameters)
    saveas = str(parameters["save"])
    with open(saveas, "w") as image_gallery:
        image_gallery.write(html_gallery)
        print("Created {}".format(saveas))


