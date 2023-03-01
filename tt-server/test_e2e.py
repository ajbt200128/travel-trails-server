import requests
from faker import Faker

URL = "http://localhost:8080"


def ping():
    r = requests.get(URL + "/ping")
    assert r.status_code == 200
    assert r.json() == {"message": "pong"}


def gen_location():
    points = [Faker().latlng() for _ in range(3)]
    points = list(map(lambda x: [float(x[0]), float(x[1])], points))
    location = {
        "name": Faker().word(),
        "description": Faker().sentence(),
        "points": points,
    }
    return dict(location)


def make_location():
    location = gen_location()
    r = requests.post(URL + "/location", json=location)
    print(r.json())
    assert r.status_code == 201
    return r.json()


def get_location(location_id):
    r = requests.get(URL + f"/location/{location_id}")
    assert r.status_code == 200
    return r.json()


def delete_location(location_id):
    r = requests.delete(URL + f"/location/{location_id}")
    assert r.status_code == 200


def get_locations():
    r = requests.get(URL + "/locations")
    assert r.status_code == 200
    return r.json()


def get_nearby_locations(lat, lon, radius):
    r = requests.get(URL + f"/locations/nearby?lat={lat}&lon={lon}&radius={radius}")
    assert r.status_code == 200
    return r.json()


def get_images(location_id):
    r = requests.get(URL + f"/location/{location_id}/images")
    assert r.status_code == 200
    return r.json()


def get_image(image_id):
    r = requests.get(URL + f"/image/{image_id}")
    assert r.status_code == 200
    content = r.content
    return content


def upload_image(location_id):
    r = requests.post(
        URL + f"/upload_image/{location_id}", files={"file": open("image.png", "rb")}
    )
    assert r.status_code == 201
    return r.json()


def delete_image(image_id):
    r = requests.delete(URL + f"/image/{image_id}")
    assert r.status_code == 200


def get_image_data(image_id):
    r = requests.get(URL + f"/image/{image_id}/data")
    assert r.status_code == 200
    return r.json()

def create_user():
    user = {
        "username": Faker().user_name(),
        "name": Faker().name(),
        "profile_picture": Faker().image_url(),
    }
    r = requests.post(URL + "/user", json=user)
    assert r.status_code == 201
    return r.json()

def get_user(user_id):
    r = requests.get(URL + f"/user/{user_id}")
    assert r.status_code == 200
    return r.json()

def get_user_visits(user_id):
    r = requests.get(URL + f"/user/{user_id}/visits")
    assert r.status_code == 200
    return r.json()

def create_visit(user_id, location_id):
    r = requests.post(URL + f"/user/{user_id}/visit/{location_id}")
    assert r.status_code == 201
    return r.json()


if __name__ == "__main__":
    print("Checking server is up")
    try:
        ping()
    except Exception as e:
        print("Server is down")
        raise e

    print("Test make location")
    location = make_location()
    location_id = location["id"]
    print(location)

    print("Test get location")
    location = get_location(location_id)

    print("Test get locations")
    locations = get_locations()
    assert location in locations

    print("Test upload image")
    image = upload_image(location_id)
    image_id = image["id"]

    print("Test get image")
    image = get_image(image_id)
    assert image == open("image.png", "rb").read()

    print("Test get image data")
    image_data = get_image_data(image_id)
    assert image_data["location_id"] == location_id

    print("Test get images")
    images = get_images(location_id)
    assert image_data in images

    print("Test get nearby")
    nearby = get_nearby_locations(
        location["geometry"]["coordinates"][0][0][0],
        location["geometry"]["coordinates"][0][0][1],
        1000,
    )
    assert location in nearby

    print("Test create user")
    user = create_user()
    user_id = user["username"]
    assert user == get_user(user_id)

    print("Test create visit")
    visit = create_visit(user_id, location_id)
    assert visit in get_user_visits(user_id)


