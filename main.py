# -*- coding: utf-8 -*-
from travel import travel


def main():
    CityCode = ("002", "001", "003", "007", "005", "006", "008", "009", "011", "015", "012", "013", "014", "016", "018", "020", "028", "004", "022", "021", "029", "023", "025", "024", "026", "027")
    CityList = ("基隆市", "台北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "台中市", "彰化縣", "雲林縣", "南投縣", "嘉義市", "嘉義縣", "台南市", "高雄市", "屏東縣", "屏東縣琉球鄉離島", "宜蘭縣", "花蓮縣", "台東縣", "台東縣綠島、蘭嶼", "澎湖縣", "連江縣", "金門縣", "南海諸島", "釣魚台列嶼")

    for code, city in zip(CityCode, CityList):
        print(code, city)
        travel(code)

if __name__ == '__main__':
    main()

