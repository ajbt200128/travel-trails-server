import json

import requests

# set a name for search
search_name = "Lincoln Memorial"

# set bounding box coordinates
lat_min = 38.88030972164946
long_min = -77.0560455322265
lat_max = 38.90529438572799
long_max = -77.01982498168944


"""
Returns a list of images (250) at a lat, lon
Requires Flickr API key
"""


def flickr_search(api_key, lat, lon):
    photo_search_query = (
        "https://www.flickr.com/services/rest/"
        "?method=flickr.photos.search&api_key={}&lat={}&lon={}&"
        "format=json&nojsoncallback=1"
    )

    photo_search_query = photo_search_query.format(api_key, lat, lon)
    print(photo_search_query)

    photo_ids = []
    photo_urls = []

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
                url_query = (
                    "https://www.flickr.com/services/rest/"
                    "?method=flickr.photos.getSizes&api_key={}&photo_id={}"
                    "&format=json&nojsoncallback=1"
                )
                url_query = url_query.format(api_key, id)

                response = requests.get(url_query)
                url_response = response.json()
                # get the medium sized image (6)
                photo_urls.append(url_response["sizes"]["size"][6]["source"])

    return photo_urls


# create an HTML page to display images
def create_image_gallery(photo_urls):
    # open the gallery page template and read as string
    with open("gallery_template.html", "r") as gallery_template:
        gallery_html = gallery_template.read()

        image_div = """
        <div class="responsive">
        <div class="gallery">
            <a target="_blank" href="img_mountains.jpg">
            <img src="{source}" alt="{alt}" width="600" height="400">
            </a>
            <div class="desc">{desc}</div>
        </div>
        </div>
        """

        divs = ""
        for url in photo_urls:
            divs += image_div.format(source=url, alt="alt", desc="desc")

        gallery_html = gallery_html.format(
            description="test", responsive_image_divs=divs
        )
        with open("image_gallery.html", "w") as image_gallery:
            image_gallery.write(gallery_html)

        print("created image gallery")


# read API key from file
with open("api_keys.json") as f:
    keys = json.load(f)
    if "flickr_api_key" in keys:
        flickr_api_key = str(keys["flickr_api_key"])

# coordinates of Lincoln Memorial
lat = "38.889248"
lon = "-77.050636"

# get photo urls at coordinates
# photo_urls = flickr_search(flickr_api_key, lat, lon)

# create_image_gallery(photo_urls)
photo_urls = [
    "https://live.staticflickr.com/65535/52276735605_b57fd06bc1.jpg",
    "https://live.staticflickr.com/65535/52266453747_0c6f249ea1.jpg",
    "https://live.staticflickr.com/65535/52267237160_ea7410c3de.jpg",
    "https://live.staticflickr.com/65535/52265774557_5f34b8303f.jpg",
    "https://live.staticflickr.com/65535/52266741736_641dbb0394.jpg",
    "https://live.staticflickr.com/65535/52266757223_cbf1cd75e5.jpg",
    "https://live.staticflickr.com/65535/52260987403_f8a60ffa3b.jpg",
    "https://live.staticflickr.com/65535/52260128385_90e629b841.jpg",
    "https://live.staticflickr.com/65535/52257338106_fedfbaac80.jpg",
]
print(photo_urls)

create_image_gallery(photo_urls)
