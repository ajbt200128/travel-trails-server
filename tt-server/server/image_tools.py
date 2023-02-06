import requests


def flickr_search(api_key, parameters):
    """
    Returns a list of images (250) at a lat, lon
    Requires Flickr API key
    """

    # extract query parameters if they exist, otherwise resort to default (lincoln)
    lat = str(38.889248)
    lon = str(-77.050636)
    radius = 0.1
    tag = ""
    if "latitude" in parameters:
        lat = str(parameters["latitude"])
    if "lonitude" in parameters:
        lon = str(parameters["longitude"])
    if "radius" in parameters:
        radius = str(parameters["radius"])
    if "tag" in parameters:
        tag = str(parameters["tag"])

    photo_search_query = (
        "https://www.flickr.com/services/rest/"
        "?method=flickr.photos.search&api_key={}&lat={}&lon={}&"
        "radius={}&radius_units=mi&text={}&"
        "format=json&nojsoncallback=1"
    )

    photo_search_query = photo_search_query.format(api_key, lat, lon, radius, tag)

    photo_ids = []
    photo_urls = []

    # do photo search at lat, lon
    response = requests.get(photo_search_query)
    photo_search_response = response.json()

    # check if valid response
    if photo_search_response["stat"] == "fail":
        print(photo_search_response["message"])
    elif photo_search_response["stat"] == "ok":
        # check if a positive number of images
        if photo_search_response["photos"]["total"] > 0:

            # retrieve image ids
            print(
                "Retrieved {} photos".format(
                    len(photo_search_response["photos"]["photo"])
                )
            )
            for photo in photo_search_response["photos"]["photo"]:
                photo_ids.append(str(photo["id"]))

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
def create_image_gallery(photo_urls, parameters):
    # open the gallery page template and read as string
    with open("gallery_template.txt", "r") as gallery_template:
        html_gallery = gallery_template.read()

        figure = """
        <figure>
            <a href="{href}">
                <img title="{title}" src="{src}">
            </a>
            <figcaption>{figcaption}</figcaption>
        </figure>
        """

        gallery = ""
        for url in photo_urls:
            gallery += figure.format(
                href=url, title=url, src=url, figcaption="Description"
            )

        html_gallery = html_gallery.format(
            title="Flickr Gallery",
            description="Generated with query {}".format(str(parameters)),
            gallery=gallery,
        )

        return html_gallery