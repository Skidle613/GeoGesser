def picture_of_object(toponym_to_find):
    # Возвращает контент картинки, который надо записать в файл
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    lower_corner = toponym['boundedBy']['Envelope']['lowerCorner'].split()
    upper_corner = toponym['boundedBy']['Envelope']['upperCorner'].split()
    delta1 = abs(float(upper_corner[0]) - float(lower_corner[0]))
    delta2 = abs(float(upper_corner[1]) - float(upper_corner[1]))
    map_params = {
        'll': ",".join([toponym_longitude, toponym_lattitude]),
        'spn': ",".join([delta1, delta2]),
        'l': 'map'
    }
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    return response.content
    
