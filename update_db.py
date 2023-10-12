import pymysql
import schedule
import time
import requests
import json
from datetime import datetime
import people_count_predict as pcp

conn = pymysql.connect(host="ishs.co.kr", user="root", password="ishs123!", db="kcf", charset="utf8")
curs = conn.cursor()


def update_db():
    global conn, curs
    for place in pcp.AREA_NM:
        host = f"http://openapi.seoul.go.kr:8088/4e574f4441796f7537316758474875/json/citydata_ppltn/1/5/{pcp.AREA_CD[pcp.AREA_NM.index(place)]}"
        res = requests.get(host)
        data = json.loads(res.text)
        AREA_PPLTN_MIN = data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MIN']
        AREA_PPLTN_MAX = data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MAX']
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        curs.execute(f"INSERT INTO people VALUES ('{place}', '{t}', {AREA_PPLTN_MIN}, {AREA_PPLTN_MAX})")
        conn.commit()


if __name__ == '__main__':
    schedule.every(5).minutes.do(update_db)
    while True:
        schedule.run_pending()
        time.sleep(1)
