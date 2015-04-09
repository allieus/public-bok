import re
import requests
from bs4 import BeautifulSoup
import lxml.etree as ET


class KitaCrawler(object):
    def __init__(self):
        self.init()

    def init(self):
        html = requests.get('http://stat.kita.net/stat/kts/prod/ProdItemImpExpList.screen').text

        try:
            this_yy = re.search('var\s+thisYY\s+=\s+\"(.+?)\"', html).group(1)
            last_yy = re.search('var\s+lastYY\s+=\s+\"(.+?)\"', html).group(1)
        except AttributeError:
            raise ValueError('not found thisYY/lastYY')

        matched = re.search(r'initdata.Cols = \[(.*?)\]', html, re.DOTALL | re.MULTILINE)
        self.header_cols = []
        if matched:
            headers_js = matched.group(1)
            headers_js = headers_js.replace('lastYY+\"', u'\"{}'.format(last_yy))
            headers_js = headers_js.replace('thisYY+\"', u'\"{}'.format(this_yy))
            self.header_cols = re.findall(r'Header\s*:\s*\"(.+?)\"', headers_js)

        if not self.header_cols:
            raise ValueError('not found header_cols')

        soup = BeautifulSoup(html)
        self.initial_form_data = {}
        tags = soup.select('form[name=form1] input') + soup.select('form[name=form1] select')
        for tag in tags:
            self.initial_form_data[tag['name']] = tag.get('value', '')

        self.initial_form_data.update({
            'event_udap': 'Search',
            'searchType': 'SHEET',
            'sheet_col_length': len(self.header_cols),
            'search_gbn': 'Prod',       # Prod_Ctr(지역/국가 검색), Prod(지역검색)
            's_measure': '1000',        # 금액단위 : 1(US$), 1000(천불), 1000000(백만불)

            's_year': '2015',           # 년도
            's_month': '02',            # 월
            's_cond_gb': 'HS',          # HS(HSK), MTI(MTI), SITC(SITC)
            's_cond_unit': '6',         # 품목단위 : 0(전단위), 2(2단위), 4(4단위), 6(6단위), 10(10단위)
            's_field': 'AMT',           # 화면선택 : AMT(금액), WGT(중량), QTY(수량)
            's_monthsum_gb': '2',       # 선택 : 1(당월), 2(누계)
            's_sort': 'THIS_EXP_AMT',   # 정렬기준
            's_language': 'kor_name',   # kor_name(한글), eng_name(영문)
            'pie_legend': 'Exp',        # Exp(수출), Imp(수입)
        })
        self.initial_form_data.update({
            'p_cond_gb': self.initial_form_data['s_cond_gb'],
            'p_prod_cd': self.initial_form_data['s_prod_code'],
            'p_prod_nm': self.initial_form_data['s_prod_name'],
        })

    def get_page(self, page=1, max=100):
        form_data = self.initial_form_data.copy()
        form_data.update({
            'pageNum': page,
            'listCount': max,
        })
        r = requests.post('http://stat.kita.net/stat/kts/prod/ProdItemImpExpListWorker.screen', data=form_data)
        xml = r.text.strip().encode(r.encoding)
        doc = ET.fromstring(xml)
        rows = []
        for tr in doc.find('DATA').findall('TR'):
            row = [td.text for td in tr.findall('TD')]
            rows.append(row)
        return rows

