# from cgitb import html
# from http import cookies
import pip._vendor.requests 
import requests
# from requests_html import HTMLSession


url_base = "https://selvbetjening.ewii.com"
url_login = url_base + "/Login"
url_consumption = url_base + "/api/consumption"
data_login = {
    "scController": "Auth",

    "scAction": "EmailLogin",
    "Email": "",
    "Password": "",
}

url_datapoints = url_consumption + "/hours"
params_datapoints = {
    'monthOfYear': '2',
    'dayOfMonth': '27',
    'installationNumber': '114780', # in
    'consumerNumber': '2',
    'counterId': '1',
    'type': '2',
    # EL
    'meterId': '4',
    'utility': '0',
    'unit': 'KWH',
    'factoryNumber': '56048087',
    # Vand
    # 'meterId': '204',
    # 'utility': '10',
    # 'unit': 'm3',
    # 'factoryNumber': '69343604'
}

# cookies_1 = {
#     "selvbetjening#lang": "da",
#     'CookieAccept': 'Allowed',
#     'ASP.NET_SessionId': 'us5qwfmruob25xzt1tjmhgpn',
#     'SC_ANALYTICS_GLOBAL_COOKIE': '22ec83d0a32e4f79a5764afad2427bac|True',
#     'CookieInformationConsent': '%7B%22website_uuid%22%3A%22c77fa841-89d1-4c34-b8d6-20cc6a105fe4%22%2C%22timestamp%22%3A%222022-03-11T06%3A28%3A51.767Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fselvbetjening.ewii.com%2FLogin%3FreturnID%3D%257bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%257d%22%2C%22consent_website%22%3A%22EWII%22%2C%22consent_domain%22%3A%22selvbetjening.ewii.com%22%2C%22user_uid%22%3A%2212544d7f-108d-4e39-9caf-67699f4b3503%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.51%20Safari%2F537.36%22%7D',
#     '_ga': 'GA1.3.922015228.1646980132',
#     '_gid': 'GA1.3.1919670786.1646980132',
#     'SNS': '1',
#     'cuvid': 'cdf382510f6440d781a40bbb414932b5',
#     '917d1132-5173-4d4c-99cf-5782ba3b055c': '10',
#     '_sn_m': '{"r":{"n":1,"r":"selvbetjening.ewii"}}',
#     '_sn_n': '{"cs":{"3f7e":{"t":{"i":1,"c":"3f7e04db-d3cb-4124-b323-ed8c235062a83,1,10,20"},"i":[1678714908664,1],"c":1}},"ssc":1,"a":{"i":"ce6eaa11-0e3d-48ee-bfd3-dd48bf9a9567"}}',
#     'cusid': '1647184158116',
#     '_sn_a': '{"a":{"s":1647183786421,"l":"https://ewii.com/Login?logout","e":1647181299428},"v":"fd36d6f4-40b9-460f-90d5-f7be3f1455c1","g":{"sc":{"3f7e04db-d3cb-4124-b323-ed8c235062a8":1}}}',
#     'TREFOR:LastPageItemID': '{0F167ACB-70A7-4E30-8DC7-4EF9B36B2B01}',
#     '_dc_gtm_UA-3382835-26': '1',
#     'cuvon': '1647185724705',
# }

# headers = {
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"macOS"',
#     'Upgrade-Insecure-Requests': '1',
#     'Origin': 'https://selvbetjening.ewii.com',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-User': '?1',
#     'Sec-Fetch-Dest': 'document',
#     'Referer': 'https://selvbetjening.ewii.com/Login?logout',
#     'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
# }

data = {
  'scController': 'Auth',
  'scAction': 'EmailLogin',
  'Email': 'j.olesen@vindinggaard.dk',
  'Password': 'fuzbyk-fyrbyK-2jeppy'
}

params = (
    ('utility', 'Electricity'),
)

class Ewii:
    """
    Primary exported interface for ewii.dk API wrapper.
    """

    def __init__(self, email, password):
        self._email = email
        self._password = password
        ## Assume people only have a single metering device.
        ## Feel free to expand the code to find all metering devices
        ## and iterate over them.
        ## Must be a string - see where it is used.
        self._asset_id = "1"
        self._installation_id = "1"
        # self._session = HTMLSession()
        self._session = requests.session()
        self._has_electricity_meter = False
        self._has_heat_meter = False

    def login(self):

        data_login["Email"] = self._email
        data_login["Password"] = self._password
        # print(self._session.c25ookies.get_dict())
        # self._session.cookies["ASP.NET_SessionId"]= get.cookies["ASP.NET_SessionId"]
        # post = self._session.post(url_login, data=data_login, allow_redirects=False)
        # self._session.headers = headers
        # self._session.cookies.add_cookie_header(cookies_1)
        # get = self._session.get(url_login)
        get_cookies = self._session.get('https://policy.app.cookieinformation.com/cookiesharingiframe.html')
        login = self._session.post(url_login, data=data, allow_redirects=False)
        # print(post.html.absolute_links)
        # post.html.render()
        # self._session.cookies["SNS"] = '1'
        # print(self._session.cookies.get_dict())

        # post = self._session.post(url_login, data=data_login)

        # cookie = post.cookies.get_dict()
        # print("headers ", get.headers)
        # print("headers ", post.headers)
        # print("cookies ", requests.utils.dict_from_cookiejar(self._session.cookies))
        # print("html ", post.text)

        success = login.text.__contains__("Mit overblik")
        # post.html.find()

        return success

    def detect_meters(self):

        # Water
        # https://selvbetjening.ewii.com/api/consumption/meters?utility=Water
        # print(self._session.cookies.get_dict())
        # angular_resource = self._session.get('https://selvbetjening.ewii.com/Scripts/vendor/angular/modules/angular-resource.js')        
        # angular_sanitizer = self._session.get('https://selvbetjening.ewii.com/Scripts/vendor/angular/modules/angular-sanitize.js')
        # angular_min = self._session.get('https://selvbetjening.ewii.com/Scripts/vendor/angular/angular.min.js')
        # angular_locale = self._session.get('https://selvbetjening.ewii.com/Scripts/vendor/angular/i18n/angular-locale_da-dk.js')
        # app = self._session.get('https://selvbetjening.ewii.com/Scripts/brand/selvbetjening/app.js')
        self._session.headers["Content-Type"] = "application/json;charset=UTF-8"
        data_adr = 'false'
        getAdressPicker = self._session.post('https://selvbetjening.ewii.com/api/product/GetAddressPickerViewModel', data=data_adr)
        # print(getAdressPicker.content)
        dict = self._session.get("https://selvbetjening.ewii.com/api/dictionary?keys=TREFOR.Selvbetjening.Installation.AddressPicker.Groups.HistoricElements")
        noti = self._session.get("https://selvbetjening.ewii.com/api/notifications")
        email = self._session.get("https://selvbetjening.ewii.com/api/selvbetjening/verifyEmail")
        cabl = self._session.get('https://policy.app.cookieinformation.com/cookie-data/selvbetjening.ewii.com/cabl.json')
        # da_js = self._session.get('https://policy.app.cookieinformation.com/c80db3/selvbetjening.ewii.com/da.js')
        
        # chart = self._session.get("https://selvbetjening.ewii.com/Scripts/app/angular/consumption/chart-teaser.html")

        # self._session.headers["Content-Type"] = "application/json;charset=UTF-8"
        data1 = '{"Id":0,"Active":true,"Address":{"PostalCode":"7100","City":"Vejle","Street":"Sk\xF8n Valborgs Vej","StreetCode":"2192","Number":"2","Letter":"","MunicipalityCode":"630","Floor":"","Side":"","Location":null,"Aftagenummer":null},"Installations":[{"InstallationNumber":"114780","ConsumerNumber":"2","SubDebitorNumber":"1","PaymentMethod":"PBS","CompanyNumber":"1","Address":{"PostalCode":"7100","City":"Vejle","Street":"Sk\xF8n Valborgs Vej","StreetCode":"2192","Number":"2","Letter":"","MunicipalityCode":"630","Floor":"","Side":"","Location":null,"Aftagenummer":null},"Active":true,"SamleInstallation":false,"SupplyTypes":[0,10],"MoveInDate":"2015-02-14T00:00:00","HasAgreement":false,"AgreementType":null,"AlternatePayer":false}],"IsDummyHistoricElement":false,"UniqueAddress":true,"DisplayString":"Sk\xF8n Valborgs Vej 2, 7100 Vejle"}'
        setAddressPicker = self._session.post("https://selvbetjening.ewii.com/api/product/SetSelectedAddressPickerElement", data=data1)
        
        self._session.headers.__delitem__("Content-Type")
        self._session.headers["Accept"] = "application/json, text/plain, */*"
        self._session.cookies["CookieAccept"] = "Allowed"
        self._session.cookies["CookieInformationConsent"] = "%7B%22website_uuid%22%3A%22c77fa841-89d1-4c34-b8d6-20cc6a105fe4%22%2C%22timestamp%22%3A%222022-03-11T06%3A28%3A51.767Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fselvbetjening.ewii.com%2FLogin%3FreturnID%3D%257bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%257d%22%2C%22consent_website%22%3A%22EWII%22%2C%22consent_domain%22%3A%22selvbetjening.ewii.com%22%2C%22user_uid%22%3A%2212544d7f-108d-4e39-9caf-67699f4b3503%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.51%20Safari%2F537.36%22%7D"
        self._session.cookies["_sn_a"] = '{"a":{"s":1647183786421,"l":"https://ewii.com/","e":1647181299428},"v":"fd36d6f4-40b9-460f-90d5-f7be3f1455c1","g":{"sc":{"3f7e04db-d3cb-4124-b323-ed8c235062a8":1}}}'

        # self._session.headers = headers
        # self._session.cookies["_sn_a"] = '{"a":{"s":1647183786421,"l":"https://ewii.com/","e":1647181299428},"v":"fd36d6f4-40b9-460f-90d5-f7be3f1455c1","g":{"sc":{"3f7e04db-d3cb-4124-b323-ed8c235062a8":1}}}'
        products = self._session.post("https://selvbetjening.ewii.com/api/product/GetInstallationProducts")

        # meter = self._session.get(
        #     # url_consumption + "/meters?utility=Water",
        #     'https://selvbetjening.ewii.com/api/consumption/meters?utility=Electricity'
        #     # headers=headers
        #     # cookies=cookies
        # )

        cabl = self._session.get('https://policy.app.cookieinformation.com/cookie-data/selvbetjening.ewii.com/cabl.json')
        cookieFrame = self._session.get("https://policy.app.cookieinformation.com/cookiesharingiframe.html")

        # params_el = (
        #     ('utility', 'Electricity'),
        # )

        # meter = self._session.get("https://selvbetjening.ewii.com/api/consumption/meters", params=params_el)

        params_u = (
            ('utility', '0'),
            ('installationNumber', '114780'),
        )

        # self._session.headers["Content-Type"] = "application/json, text/plain, */*"
        sumConsumption = self._session.get('https://selvbetjening.ewii.com/api/consumption/sum', params=params_u)

        payload_json = self._session.get(url_consumption + "/meters?utility=Heat").json
        # data = self._session.get('https://selvbetjening.ewii.com/api/selvbetjening/verifyEmail')

        params = (
            ('monthOfYear', '1'),
            ('installationNumber', '114780'),
            ('consumerNumber', '2'),
            ('meterId', '204'),
            ('counterId', '1'),
            ('type', '2'),
            ('utility', '10'),
            ('unit', 'm3'),
            ('factoryNumber', '69343604'),
        )

        consumption_days = self._session.get('https://selvbetjening.ewii.com/api/consumption/days', headers=headers, params=params, cookies=cookies)

        response = self._session.get('https://selvbetjening.ewii.com/Forsyning/Vand')

        el = self._session.get("https://selvbetjening.ewii.com/Forsyning/El")

        meter = self._session.get(
            # url_consumption + "/meters?utility=Water",
            'https://selvbetjening.ewii.com/api/consumption/meters?utility=Water'
            # headers=headers
            # cookies=cookies
        )

        response = self._session.post('https://selvbetjening.ewii.com/api/product/GetInstallationProducts')
        # response = requests.get('https://selvbetjening.ewii.com/api/consumption/meters?utility=Electricity', cookies=self._session.cookies)
        # [{"Installation":{"InstallationNumber":"114780","ConsumerNumber":"2"},"MeterId":204,
        # "CounterId":1,"ReadingType":2,"Utility":10,"Unit":"m3","FactoryNumber":"69343604",
        # "Status":"aktiv","Lokalnr":"69343604","ProductionDirection":2,"NetDirection":""},
        # {"Installation":{"InstallationNumber":"114780","ConsumerNumber":"2"},"MeterId":203,
        # "CounterId":1,"ReadingType":2,"Utility":10,"Unit":"m3","FactoryNumber":"66197036",
        # "Status":"inaktiv","Lokalnr":"66197036","ProductionDirection":2,"NetDirection":""}]
        # https://selvbetjening.ewii.com/api/consumption/meters?utility=Electricity

        datapoints = self._session.get(url_datapoints, params=params_datapoints)
        # result_json = req.json()

        params = (
            ('utility', '10'),
            ('installationNumber', '114780'),
        )
        sum = self._session.get('https://selvbetjening.ewii.com/api/consumption/sum', params=params)
        # Electricity
        # https://selvbetjening.ewii.com/api/consumption/meters?utility=Electricity
        payload_json = requests.get(
            url_consumption + "/meters?utility=Electricity"
        ).json

        # [{"Installation":{"InstallationNumber":"114780","ConsumerNumber":"2"},"MeterId":4,
        # "CounterId":1,"ReadingType":2,"Utility":0,"Unit":"KWH","FactoryNumber":"56048087",
        # "Status":"aktiv","Lokalnr":"56048087","ProductionDirection":2,"NetDirection":""},
        # {"Installation":{"InstallationNumber":"114780","ConsumerNumber":"2"},"MeterId":3,"
        # CounterId":1,"ReadingType":2,"Utility":0,"Unit":"kWh","FactoryNumber":"11072726",
        # "Status":"inaktiv","Lokalnr":"11072726","ProductionDirection":2,"NetDirection":""}]

        # https://selvbetjening.ewii.com/api/consumption/meters?utility=Heat
        # Heat
        payload_json = self._session.get(url_consumption + "/meters?utility=Heat").json
        # {"Message":"17F708D501A"}

        # Not present
        # {"Message":"17F708D501A"}
        return False

if __name__ == "__main__":
    ewii = Ewii("j.olesen@vindinggaard.dk", "fuzbyk-fyrbyK-2jeppy")
    ewii.login()
    ewii.detect_meters()