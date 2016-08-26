# -*- coding: utf-8 -*-
import sys
import urllib2
from bs4 import BeautifulSoup

reload(sys)  # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'


def detail(ADDR):
    content = urllib2.urlopen(ADDR).read()
    content_big5 = content.decode('cp950').encode('utf-8')
    soup = BeautifulSoup(content_big5, "html.parser")
    menu = soup.find_all('table', bgcolor='#FAFAF5')
    all_tr = menu[0].find_all('tr')

    main_addr = ''
    sub_addr =''

    for tr in all_tr:
        td = tr.find_all('td')
        if td[0].get_text() == u'縣市名稱' and len(td) > 1:
            main_addr = td[1].get_text()
        if td[0].get_text() == u'鄉鎮名稱' and len(td) > 1:
            sub_addr = td[1].get_text()

    return main_addr, sub_addr


def traverse(ADDR, f):
    content = urllib2.urlopen(ADDR).read()
    content_big5 = content.decode('cp950').encode('utf-8')
    soup = BeautifulSoup(content_big5, "html.parser")

    # print content
    menu = soup.find_all('table', bgcolor='#fafaf5')

    all_tr = menu[0].tr.find_all('tr', valign='top')
    for i, each in enumerate(all_tr):
        print i,
        print ' ',
        item = each.find_all('td')

        name = item[0].get_text().strip()
        category = item[1].get_text().strip()
        phone = item[2].get_text().strip()
        address = item[3].get_text().strip()
        link = item[5].a
        href = 'http://travel.nccc.com.tw'+link['href']
        # print href
        main, sub = detail(href)
        info = name + ', ' + phone + ', ' + category + ', ' + main + ', ' + sub \
               + ', ' + address + '\n'
        print name, phone, category, main, sub, address

        f.write(info)

    next_a = menu[0].previous_element.previous_element.previous_element
    next_href = 'http://travel.nccc.com.tw'+next_a['href']
    print next_href
    tag = next_a.get_text()
    if tag == u'下一頁':
        traverse(next_href, f)


def travel(location, end, name):
    f = open(name + u'.csv', 'a')

    ADDR = 'http://travel.nccc.com.tw/NASApp/NTC/servlet/com.du.mvc.Entry' \
           'Servlet?Action=RetailerList&Type=GetFull&Request=NULL_NULL_NULL_'\
           +location+\
           '_NULL_NULL_NULL_NULL_NULL_0_1_20_'+\
           end
    print ADDR
    traverse(ADDR, f)

if __name__ == '__main__':
    location = '025'
    end = '81'
    name = u'連江縣'

    travel(location, end, name)
