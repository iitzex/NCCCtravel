# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import geocoder
import folium
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Store


def detail(ADDR):
    r = requests.get(ADDR)
    content_big5 = r.content.decode('cp950').encode('utf-8')
    soup = BeautifulSoup(content_big5, "html.parser")
    menu = soup.find_all('table', bgcolor='#FAFAF5')
    all_tr = menu[0].find_all('tr')

    main_addr = ''
    sub_addr =''

    for tr in all_tr:
        td = tr.find_all('td')
        if td[0].get_text() == '縣市名稱' and len(td) > 1:
            main_addr = td[1].get_text()
        if td[0].get_text() == '鄉鎮名稱' and len(td) > 1:
            sub_addr = td[1].get_text()

    return main_addr, sub_addr


def traverse(ADDR, map_osm, session):
    retailer = requests.get(ADDR)
    content_big5 = retailer.content.decode('cp950').encode('utf-8')
    soup = BeautifulSoup(content_big5, "html.parser")
    menu = soup.find_all('table', bgcolor='#fafaf5')

    all_tr = menu[0].tr.find_all('tr', valign='top')
    for i, each in enumerate(all_tr):
        item = each.find_all('td')

        name = item[0].get_text().strip()
        phone = item[2].get_text().strip()
        address = item[3].get_text().strip()
        link = item[5].a
        href = 'http://travel.nccc.com.tw'+link['href']
        # print href
        main, sub = detail(href)
        main = main.strip().replace('\\xa0', ' ')
        sub = sub.strip().replace('\\xa0', ' ')

        # print(i+1, name, phone, category, main, sub, address)
        print(i+1, name, address)
        retailer = Store(name=name, phone=phone, address=address, category=main, sub=sub)

        latlon = locator(address)
        if latlon is not None:
            folium.Marker(location=latlon, popup=name).add_to(map_osm)
            map_osm.location = latlon
            map_osm.save('nccc.html')

            print('\t' + str(latlon))
            retailer.lat = latlon[0]
            retailer.lon = latlon[1]

        session.add(retailer)
    session.commit()

    next_a = menu[0].previous_element.previous_element.previous_element
    next_href = 'http://travel.nccc.com.tw'+next_a['href']
    print(next_href)
    tag = next_a.get_text()
    if tag == '下一頁':
        traverse(next_href, map_osm, session)


def locator(place):
    # g = geocoder.google(place)
    g = geocoder.google(place)
    g = geocoder.google('Mountain View, CA')
    print(g.latlng)
    if len(g.latlng) is 0:
        return

    return g.latlng


def travel(location):
    ADDR = 'http://travel.nccc.com.tw/NASApp/NTC/servlet/com.du.mvc.Entry' \
           'Servlet?Action=RetailerList&Type=GetFull&Request=NULL_NULL_NULL_' \
           +location+ \
           '_NULL_NULL_NULL_NULL_NULL_0_1_20_99999'
    print(ADDR)

    try:
        map_osm = folium.Map(zoom_start=13, tiles='CartoDB positron')
        engine = create_engine('sqlite:///nccc.db', echo=True)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        traverse(ADDR, map_osm, session)
    except IndexError as e:
        print(e)
        pass


if __name__ == '__main__':
    location = '025'
    location = '002'

    # travel(location)
    locator('基隆市仁愛區和明里仁一路２９５號１樓')
