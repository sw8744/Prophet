import schedule
import time
import requests
import json
from datetime import datetime
import people_count_predict as pcp


def update_place():
    data = {
        "API_KEY": "HelloWorld",
        "place_data": []
    }
    for place in pcp.AREA_NM:
        host = f"http://openapi.seoul.go.kr:8088/4e574f4441796f7537316758474875/json/citydata_ppltn/1/5/{pcp.AREA_CD[pcp.AREA_NM.index(place)]}"
        res = requests.get(host)
        ppl_data = json.loads(res.text)
        AREA_PPLTN_MIN = ppl_data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MIN']
        AREA_PPLTN_MAX = ppl_data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MAX']
        place_data = {
            "name": place,
            "ppl_min": int(AREA_PPLTN_MIN),
            "ppl_max": int(AREA_PPLTN_MAX)
        }
        data['place_data'].append(place_data)
    res = requests.post("http://localhost:8000/update", json=data)
    print(res.text)


def register_place(place):
    lat, lng = get_lat_lng(place)
    size = pcp.AREA_SIZE[pcp.AREA_NM.index(place)]
    host = f"http://app.ishs.co.kr:5000/register"
    data = {
        "API_KEY": "HelloWorld",
        "place_data": [
            {
                "name": place,
                "lat": lat,
                "lng": lng,
                "width": int(size ** 0.5) if size > 0 else 0,
                "height": int(size ** 0.5) if size > 0 else 0
            }
        ]
    }
    res = requests.patch(host, json=data)
    print(res.text)


def register_all():
    for place in pcp.AREA_NM:
        register_place(place)


def get_lat_lng(place):
    address = str(pcp.ADDRESS[pcp.AREA_NM.index(place)]).split("/")[1].replace("\"", "").replace(",", "")
    host = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "qv9swowmcw",
        "X-NCP-APIGW-API-KEY": "AtlzDVhNTZA7Ecin4rwoxQCbKqr8m0B3CYUYyGMU"
    }
    res = requests.get(host, headers=headers)
    data = json.loads(res.text)
    print(data)
    return data['addresses'][0]['y'], data['addresses'][0]['x']


def update():
    update_place()
    schedule.every(5).minutes.do(update_place)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    for place in pcp.AREA_NM:
        register_place(place)
