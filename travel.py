# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import geocoder
import folium
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Store


def detail(addr):
    r = requests.get(addr)
    content = r.content.decode('cp950')
    soup = BeautifulSoup(content, "html.parser")
    all_td = soup.find_all('td', align='right')

    res = [None] * 3

    for td in all_td:
        if td.get_text() == '縣市名稱':
            res[0] = td.find_next_sibling('td').get_text().strip().replace('\\xa0', ' ')
        if td.get_text() == '鄉鎮名稱':
            res[1] = td.find_next_sibling('td').get_text().strip().replace('\\xa0', ' ')
        # if td.get_text() == '行業別':
        #     res[2] = td.find_next_sibling('td').get_text().strip().replace('\\xa0', ' ')
        if td.get_text() == '行業細項分類':
            res[2] = td.find_next_sibling('td').get_text().strip().replace('\\xa0', ' ')

    return res


def traverse(addr, map_nccc, session):
    retailer = requests.get(addr)
    content_big5 = retailer.content.decode('cp950')
    soup = BeautifulSoup(content_big5, "html.parser")
    table = soup.find('table', bgcolor='#fafaf5')

    all_tr = table.tr.find_all('tr', valign='top')
    for i, each in enumerate(all_tr):
        item = each.find_all('td')

        name = item[0].get_text().strip()
        main = item[1].get_text().strip()
        phone = item[2].get_text().strip()
        address = item[3].get_text().strip()
        href = 'http://travel.nccc.com.tw'+item[5].a['href']
        city, town, sub = detail(href)

        print(i+1, name, phone, city, town, address, main, sub)
        retailer = Store(name=name, phone=phone, address=address, city=city, town=town,
                         main=main, sub=sub)

        latlon = locator(address)
        if latlon is not None:
            folium.Marker(location=latlon, popup=name).add_to(map_nccc)
            map_nccc.location = latlon
            map_nccc.save('nccc.html')

            print('\t' + str(latlon))

            retailer.lat = latlon[0]
            retailer.lon = latlon[1]

            res = session.query(Store).filter_by(name=name).all()
            if res is None:
                res.lat = latlon[0]
                res.lon = latlon[1]
                session.commit()
                print('update latlon', res)
                continue

        session.add(retailer)
    session.commit()

    next_a = table.previous_element.previous_element.previous_element
    next_href = 'http://travel.nccc.com.tw'+next_a['href']
    print(next_href)
    if next_a.get_text() == '下一頁':
        traverse(next_href, map_nccc, session)


def locator(place):
    g = geocoder.google(place)
    if len(g.latlng) is 0:
        return

    return g.latlng


def travel(location):
    addr = 'http://travel.nccc.com.tw/NASApp/NTC/servlet/com.du.mvc.Entry' \
           'Servlet?Action=RetailerList&Type=GetFull&Request=NULL_NULL_NULL_' \
           +location+ \
           '_NULL_NULL_NULL_NULL_NULL_0_1_20_99999'
    print(addr)

    try:
        map_nccc = folium.Map(zoom_start=13, tiles='CartoDB positron')
        session = connect_db()

        traverse(addr, map_nccc, session)
    except IndexError as e:
        print(e)
    except AttributeError as e:
        print(e)


def connect_db():
    engine = create_engine('sqlite:///nccc.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    location = '025'
    # location = '002'

    travel(location)


