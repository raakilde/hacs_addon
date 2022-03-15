# from cgitb import html
# from http import cookies
from email import header
from http import cookies
import json
from httpx import head
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

# header1 = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36',
#     'Referer': 'https://selvbetjening.ewii.com',
#     'Origin' : 'https://selvbetjening.ewii.com',
#     'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
#     'Connection': 'keep-alive',
#     'Cache-Control' : 'max-age=0',
#     'Upgrade-Insecure-Requests' : '1',
#     'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Content-Type' : 'application/x-www-form-urlencoded',
#     'Host' : 'selvbetjening.ewii.com',
#     'Cookie': 'selvbetjening#lang=da; CookieAccept=Allowed; ASP.NET_SessionId=us5qwfmruob25xzt1tjmhgpn; SC_ANALYTICS_GLOBAL_COOKIE=22ec83d0a32e4f79a5764afad2427bac|True; CookieInformationConsent=%7B%22website_uuid%22%3A%22c77fa841-89d1-4c34-b8d6-20cc6a105fe4%22%2C%22timestamp%22%3A%222022-03-11T06%3A28%3A51.767Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fselvbetjening.ewii.com%2FLogin%3FreturnID%3D%257bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%257d%22%2C%22consent_website%22%3A%22EWII%22%2C%22consent_domain%22%3A%22selvbetjening.ewii.com%22%2C%22user_uid%22%3A%2212544d7f-108d-4e39-9caf-67699f4b3503%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.51%20Safari%2F537.36%22%7D; _ga=GA1.3.922015228.1646980132; _gid=GA1.3.1919670786.1646980132; SNS=1; cuvid=cdf382510f6440d781a40bbb414932b5; 917d1132-5173-4d4c-99cf-5782ba3b055c=10; _sn_m={"r":{"n":1,"r":"selvbetjening.ewii"}}; _sn_n={"cs":{"3f7e":{"t":{"i":1,"c":"3f7e04db-d3cb-4124-b323-ed8c235062a83,1,10,20"},"i":[1678714908664,1],"c":1}},"ssc":1,"a":{"i":"b91e4360-c6c5-47bf-9189-542bb6cdeab0"}}; _dc_gtm_UA-3382835-26=1; cusid=1647197434506; cuvon=1647197434506; cusid=1647197434506; _sn_a={"a":{"s":1647197430976,"l":"https://ewii.com/Login?returnID=%7bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%7d","e":1647193105862},"v":"fd36d6f4-40b9-460f-90d5-f7be3f1455c1","g":{"sc":{"3f7e04db-d3cb-4124-b323-ed8c235062a8":1}}}; .ASPXAUTH=57B06A0181AAF2C028D0579CF6E17D11BFF316A322B982B729591182A0B99E051E6E6EEF5520034AE1800C5340CD882E3C3D35E3AD975886D85510B94B5D1A450BD2987CB1AD9A26D67BD84A2EEEB693195907B4B8A20532EB76A59F40D3E48A98A8B82FEFFBBAD5BC889D399A048DAEEA9460A61CB9AA67DE0EEF7268FC50E3295ABC51CFE121CB77490FD253C991EBF68C67DA186F18C382E0FC828E86EAD570BF5D2F9DFCAF45D61D44B05D6AEF0063E0EBD08FE688336BA19FBAEA77CE82; TREFOR:LastPageItemID={DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}; CookieAccept=Allowed; .ASPXAUTH=93081F47033083745CC8B6B83AFCD602B38343455C2FA28380C4A34EF768656F5185346928D75D480AF11F3E860841C76E58AB75D87B5C02B4E30D8D1801A9CB2D13B47E0E7F0D4581DF0110DCA5485601160926E7414323A5298B1355293C1531AB7F10BE3E592E4D8A885E994C46C953772281701CB1BB352EDA2329BC961BB7A07815EF13480C7A273DF5240CF6E9175A463961B63099DF79AA7BAEAB4D5F1763CA80A4669520233EDD0928786CC34662664403311F2FCC25CA6FA38A79A6; ASP.NET_SessionId=njzvllcsuzj1v1q4yabvn4nc; SC_ANALYTICS_GLOBAL_COOKIE=22ec83d0a32e4f79a5764afad2427bac|True; TREFOR:LastPageItemID={DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}; selvbetjening#lang=da'
# }

# cookies1 = {
#     'CookieAccept': 'Allowed',
#     '.ASPXAUTH': '60597688487E7422A4CFDB2E6CA050BB409C120F44B5A40EF8874C65172C0B88E8F0777A428CE80FEB7A68668AC7B26895ACA59017EE02B2EE8C8362ECDCE27D8091F32E74DD4869F31696A515AF1B19A1E26F4C0331FFEE7DAAB7111F853328FC09F239EABFA6036F1A4F17A84B89772630D84BF08500B53584E37CDAF81DE4928D08FCF110A8BD87B39688F1FE8AE8376893E3BCBAB37EA148A7681647307F3C519887352E38BF6780C7B072DAF40E558325A57D51A97C6AFE8EC1AE88DBA0',
#     'ASP.NET_SessionId': 'njzvllcsuzj1v1q4yabvn4nc',
#     'SC_ANALYTICS_GLOBAL_COOKIE': '22ec83d0a32e4f79a5764afad2427bac|True',
#     'TREFOR:LastPageItemID': '{DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}',
#     'selvbetjening#lang': 'da',
# }

data_login = {
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

        url_login = "https://selvbetjening.ewii.com/Login"
        payload_login='scController=Auth&scAction=EmailLogin&Email=j.olesen@vindinggaard.dk&Password=fuzbyk-fyrbyK-2jeppy'
        headers_login = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        response_login = self._session.post(url_login, headers=headers_login, data=payload_login.encode('utf-8'), allow_redirects=True)

        url_get_data = "https://selvbetjening.ewii.com/api/product/GetAddressPickerViewModel"
        payload_get_data = "false"
        headers_get_data = {
            'Content-Type': 'application/json;charset=UTF-8',
        }
        response_get_data = self._session.post(url_get_data, headers=headers_get_data, data=payload_get_data.encode('utf-8'))


        url_set_data = "https://selvbetjening.ewii.com/api/product/SetSelectedAddressPickerElement"

        payload_set_data = "{\"Id\":0,\"Active\":true,\"Address\":{\"PostalCode\":\"7100\",\"City\":\"Vejle\",\"Street\":\"Skøn Valborgs Vej\",\"StreetCode\":\"2192\",\"Number\":\"2\",\"Letter\":\"\",\"MunicipalityCode\":\"630\",\"Floor\":\"\",\"Side\":\"\",\"Location\":null,\"Aftagenummer\":null},\"Installations\":[{\"InstallationNumber\":\"114780\",\"ConsumerNumber\":\"2\",\"SubDebitorNumber\":\"1\",\"PaymentMethod\":\"PBS\",\"CompanyNumber\":\"1\",\"Address\":{\"PostalCode\":\"7100\",\"City\":\"Vejle\",\"Street\":\"Skøn Valborgs Vej\",\"StreetCode\":\"2192\",\"Number\":\"2\",\"Letter\":\"\",\"MunicipalityCode\":\"630\",\"Floor\":\"\",\"Side\":\"\",\"Location\":null,\"Aftagenummer\":null},\"Active\":true,\"SamleInstallation\":false,\"SupplyTypes\":[0,10],\"MoveInDate\":\"2015-02-14T00:00:00\",\"HasAgreement\":false,\"AgreementType\":null,\"AlternatePayer\":false}],\"IsDummyHistoricElement\":false,\"UniqueAddress\":true,\"DisplayString\":\"Skøn Valborgs Vej 2, 7100 Vejle\"}"
        headers_set_data = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        response_set_data = self._session.post(url_set_data, headers=headers_set_data, data=payload_set_data.encode('utf-8'))

        url_get_install = "https://selvbetjening.ewii.com/api/product/GetInstallationProducts"
        payload_get_install ={}
        headers_get_install = {
        }
        response_get_install = self._session.post(url_get_install, headers=headers_get_install, data=payload_get_install)
        # print(json.dumps(json.loads(response_get_install.content), indent=2))

        response_water = self._session.get("https://selvbetjening.ewii.com/api/consumption/meters?utility=Water")
        response_electricity = self._session.get("https://selvbetjening.ewii.com/api/consumption/meters?utility=Electricity")
        response_heat = self._session.get("https://selvbetjening.ewii.com/api/consumption/meters?utility=Heat")

        print(json.dumps(json.loads(response_electricity.content), indent=2))

        params = ( # el
            ('installationNumber', '114780'),
            ('consumerNumber', '2'),
            ('meterId', '4'),
            ('counterId', '1'),
            ('type', '2'),
            ('utility', '0'),
            ('unit', 'KWH'),
            ('factoryNumber', '56048087'),
        )
        response_data_el = self._session.get('https://selvbetjening.ewii.com/api/consumption/origin', params=params)

        print(json.dumps(json.loads(response_water.content), indent=2))

        params = (
            ('installationNumber', '114780'),
            ('consumerNumber', '2'),
            ('meterId', '204'),
            ('counterId', '1'),
            ('type', '2'),
            ('utility', '10'),
            ('unit', 'm3'),
            ('factoryNumber', '69343604'),
        )

        response_data_water = requests.get('https://selvbetjening.ewii.com/api/consumption/origin', params=params)

        return success

    def detect_meters(self):

        headers_adr = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'selvbetjening#lang=da; CookieAccept=Allowed; ASP.NET_SessionId=us5qwfmruob25xzt1tjmhgpn; SC_ANALYTICS_GLOBAL_COOKIE=22ec83d0a32e4f79a5764afad2427bac|True; CookieInformationConsent=%7B%22website_uuid%22%3A%22c77fa841-89d1-4c34-b8d6-20cc6a105fe4%22%2C%22timestamp%22%3A%222022-03-11T06%3A28%3A51.767Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fselvbetjening.ewii.com%2FLogin%3FreturnID%3D%257bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%257d%22%2C%22consent_website%22%3A%22EWII%22%2C%22consent_domain%22%3A%22selvbetjening.ewii.com%22%2C%22user_uid%22%3A%2212544d7f-108d-4e39-9caf-67699f4b3503%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.51%20Safari%2F537.36%22%7D; _ga=GA1.3.922015228.1646980132; _gid=GA1.3.1919670786.1646980132; SNS=1; cuvid=cdf382510f6440d781a40bbb414932b5; 917d1132-5173-4d4c-99cf-5782ba3b055c=10; _sn_m={"r":{"n":1,"r":"selvbetjening.ewii"}}; _sn_n={"cs":{"3f7e":{"t":{"i":1,"c":"3f7e04db-d3cb-4124-b323-ed8c235062a83,1,10,20"},"i":[1678714908664,1],"c":1}},"ssc":1,"a":{"i":"b91e4360-c6c5-47bf-9189-542bb6cdeab0"}}; _dc_gtm_UA-3382835-26=1; cusid=1647197434506; cuvon=1647197434506; cusid=1647197434506; _sn_a={"a":{"s":1647197430976,"l":"https://ewii.com/Login?returnID=%7bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%7d","e":1647193105862},"v":"fd36d6f4-40b9-460f-90d5-f7be3f1455c1","g":{"sc":{"3f7e04db-d3cb-4124-b323-ed8c235062a8":1}}}; .ASPXAUTH=57B06A0181AAF2C028D0579CF6E17D11BFF316A322B982B729591182A0B99E051E6E6EEF5520034AE1800C5340CD882E3C3D35E3AD975886D85510B94B5D1A450BD2987CB1AD9A26D67BD84A2EEEB693195907B4B8A20532EB76A59F40D3E48A98A8B82FEFFBBAD5BC889D399A048DAEEA9460A61CB9AA67DE0EEF7268FC50E3295ABC51CFE121CB77490FD253C991EBF68C67DA186F18C382E0FC828E86EAD570BF5D2F9DFCAF45D61D44B05D6AEF0063E0EBD08FE688336BA19FBAEA77CE82; TREFOR:LastPageItemID={DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}; CookieAccept=Allowed; .ASPXAUTH=5A63AD27DFF79020EB2977FBE7A3906E89B7B2A24F72E387F15C2056483D5C8EA8B4AC57254B877627040023A6B90EFEFEFADE3EB135AC4557F8DBA9ED35F521CE3B1C88B951585AB2C3EF087E8A73376F980AD43358A0114B988B5D7415BD0F7932A2B7E61910D45DFE1A76119EEDA865F8476FFB2D1FD1EDF95C0964130E0A41E5EE956A2D96A761BF07CFF046D62F5985DBB10CBBC6F61E856D3D9714C3098C189EDF3E2094B1298242748E4244319E10AAF84EED57C1BAC30FAF64F1EABE; ASP.NET_SessionId=njzvllcsuzj1v1q4yabvn4nc; SC_ANALYTICS_GLOBAL_COOKIE=22ec83d0a32e4f79a5764afad2427bac|True; TREFOR:LastPageItemID={DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}; selvbetjening#lang=da'
        }
        data_adr = "false"
        getAdressPicker = self._session.post('https://selvbetjening.ewii.com/api/product/GetAddressPickerViewModel', 
            data=data_adr, headers=headers_adr)
            # , cookies=cookies1)
       
        headers_adress_picker = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'selvbetjening#lang=da; CookieAccept=Allowed; ASP.NET_SessionId=us5qwfmruob25xzt1tjmhgpn; SC_ANALYTICS_GLOBAL_COOKIE=22ec83d0a32e4f79a5764afad2427bac|True; CookieInformationConsent=%7B%22website_uuid%22%3A%22c77fa841-89d1-4c34-b8d6-20cc6a105fe4%22%2C%22timestamp%22%3A%222022-03-11T06%3A28%3A51.767Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fselvbetjening.ewii.com%2FLogin%3FreturnID%3D%257bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%257d%22%2C%22consent_website%22%3A%22EWII%22%2C%22consent_domain%22%3A%22selvbetjening.ewii.com%22%2C%22user_uid%22%3A%2212544d7f-108d-4e39-9caf-67699f4b3503%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.51%20Safari%2F537.36%22%7D; _ga=GA1.3.922015228.1646980132; _gid=GA1.3.1919670786.1646980132; SNS=1; cuvid=cdf382510f6440d781a40bbb414932b5; 917d1132-5173-4d4c-99cf-5782ba3b055c=10; _sn_m={"r":{"n":1,"r":"selvbetjening.ewii"}}; _sn_n={"cs":{"3f7e":{"t":{"i":1,"c":"3f7e04db-d3cb-4124-b323-ed8c235062a83,1,10,20"},"i":[1678714908664,1],"c":1}},"ssc":1,"a":{"i":"b91e4360-c6c5-47bf-9189-542bb6cdeab0"}}; _dc_gtm_UA-3382835-26=1; cusid=1647197434506; cuvon=1647197434506; cusid=1647197434506; _sn_a={"a":{"s":1647197430976,"l":"https://ewii.com/Login?returnID=%7bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%7d","e":1647193105862},"v":"fd36d6f4-40b9-460f-90d5-f7be3f1455c1","g":{"sc":{"3f7e04db-d3cb-4124-b323-ed8c235062a8":1}}}; .ASPXAUTH=57B06A0181AAF2C028D0579CF6E17D11BFF316A322B982B729591182A0B99E051E6E6EEF5520034AE1800C5340CD882E3C3D35E3AD975886D85510B94B5D1A450BD2987CB1AD9A26D67BD84A2EEEB693195907B4B8A20532EB76A59F40D3E48A98A8B82FEFFBBAD5BC889D399A048DAEEA9460A61CB9AA67DE0EEF7268FC50E3295ABC51CFE121CB77490FD253C991EBF68C67DA186F18C382E0FC828E86EAD570BF5D2F9DFCAF45D61D44B05D6AEF0063E0EBD08FE688336BA19FBAEA77CE82; TREFOR:LastPageItemID={DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}; CookieAccept=Allowed; .ASPXAUTH=5A63AD27DFF79020EB2977FBE7A3906E89B7B2A24F72E387F15C2056483D5C8EA8B4AC57254B877627040023A6B90EFEFEFADE3EB135AC4557F8DBA9ED35F521CE3B1C88B951585AB2C3EF087E8A73376F980AD43358A0114B988B5D7415BD0F7932A2B7E61910D45DFE1A76119EEDA865F8476FFB2D1FD1EDF95C0964130E0A41E5EE956A2D96A761BF07CFF046D62F5985DBB10CBBC6F61E856D3D9714C3098C189EDF3E2094B1298242748E4244319E10AAF84EED57C1BAC30FAF64F1EABE; ASP.NET_SessionId=njzvllcsuzj1v1q4yabvn4nc; SC_ANALYTICS_GLOBAL_COOKIE=22ec83d0a32e4f79a5764afad2427bac|True; TREFOR:LastPageItemID={DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}; selvbetjening#lang=da'
        }

        data_address_picker = '{"Id":0,"Active":true,"Address":{"PostalCode":"7100","City":"Vejle","Street":"Sk\xF8n Valborgs Vej","StreetCode":"2192","Number":"2","Letter":"","MunicipalityCode":"630","Floor":"","Side":"","Location":null,"Aftagenummer":null},"Installations":[{"InstallationNumber":"114780","ConsumerNumber":"2","SubDebitorNumber":"1","PaymentMethod":"PBS","CompanyNumber":"1","Address":{"PostalCode":"7100","City":"Vejle","Street":"Sk\xF8n Valborgs Vej","StreetCode":"2192","Number":"2","Letter":"","MunicipalityCode":"630","Floor":"","Side":"","Location":null,"Aftagenummer":null},"Active":true,"SamleInstallation":false,"SupplyTypes":[0,10],"MoveInDate":"2015-02-14T00:00:00","HasAgreement":false,"AgreementType":null,"AlternatePayer":false}],"IsDummyHistoricElement":false,"UniqueAddress":true,"DisplayString":"Sk\xF8n Valborgs Vej 2, 7100 Vejle"}'
        setAddressPicker = self._session.post("https://selvbetjening.ewii.com/api/product/SetSelectedAddressPickerElement", 
            data=data_address_picker, headers=headers_adress_picker)
            # , cookies=cookies1)
        
        header1.__delitem__("Content-Type")
        headers_product = {
            'Cookie': 'selvbetjening#lang=da; CookieAccept=Allowed; ASP.NET_SessionId=us5qwfmruob25xzt1tjmhgpn; SC_ANALYTICS_GLOBAL_COOKIE=22ec83d0a32e4f79a5764afad2427bac|True; CookieInformationConsent=%7B%22website_uuid%22%3A%22c77fa841-89d1-4c34-b8d6-20cc6a105fe4%22%2C%22timestamp%22%3A%222022-03-11T06%3A28%3A51.767Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fselvbetjening.ewii.com%2FLogin%3FreturnID%3D%257bDB4774A7-3C4B-4FAF-BBFC-1F46BD77F540%257d%22%2C%22consent_website%22%3A%22EWII%22%2C%22consent_domain%22%3A%22selvbetjening.ewii.com%22%2C%22user_uid%22%3A%2212544d7f-108d-4e39-9caf-67699f4b3503%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F99.0.4844.51%20Safari%2F537.36%22%7D; _ga=GA1.3.922015228.1646980132; _gid=GA1.3.1919670786.1646980132; SNS=1; cuvid=cdf382510f6440d781a40bbb414932b5; 917d1132-5173-4d4c-99cf-5782ba3b055c=10; _sn_m={"r":{"n":1,"r":"selvbetjening.ewii"}}; _sn_n={"cs":{"3f7e":{"t":{"i":1,"c":"3f7e04db-d3cb-4124-b323-ed8c235062a83,1,10,20"},"i":[1678714908664,1],"c":1}},"ssc":1,"a":{"i":"b91e4360-c6c5-47bf-9189-542bb6cdeab0"}}; _dc_gtm_UA-3382835-26=1; cusid=1647197434506; cusid=1647197434506; .ASPXAUTH=57B06A0181AAF2C028D0579CF6E17D11BFF316A322B982B729591182A0B99E051E6E6EEF5520034AE1800C5340CD882E3C3D35E3AD975886D85510B94B5D1A450BD2987CB1AD9A26D67BD84A2EEEB693195907B4B8A20532EB76A59F40D3E48A98A8B82FEFFBBAD5BC889D399A048DAEEA9460A61CB9AA67DE0EEF7268FC50E3295ABC51CFE121CB77490FD253C991EBF68C67DA186F18C382E0FC828E86EAD570BF5D2F9DFCAF45D61D44B05D6AEF0063E0EBD08FE688336BA19FBAEA77CE82; TREFOR:LastPageItemID={DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}; cuvon=1647197445729; _sn_a={"a":{"s":1647197430976,"l":"https://ewii.com/","e":1647193105862},"v":"fd36d6f4-40b9-460f-90d5-f7be3f1455c1","g":{"sc":{"3f7e04db-d3cb-4124-b323-ed8c235062a8":1}}}; CookieAccept=Allowed; .ASPXAUTH=B332F7AAAC4C9F178D1207AFB852B25D63F09EA5CA35D30614D7EFA16264AE7B4D41AFD64E8D4F613DEC55F1BFFE1476C2DD90C903511C145C5663EBB059CF4C6FDBBDC5264D6713ADEAD4AA80D9EE12E5B98E3BD0BF8D1EF460117CCDA32A4E0E65E033E2072F31FF9C2C89FC45FA0FDA1782B71B02DF494CC37A4E1C9C83033A29A335C859603C39F2DF40F4E0F24DD09C47769E5A3C5B7BE2007215E139C1E57397B9F65438130E818DECF52BFFF57A6BF68341B3B35E9787FAFF7B06C21A; ASP.NET_SessionId=njzvllcsuzj1v1q4yabvn4nc; SC_ANALYTICS_GLOBAL_COOKIE=22ec83d0a32e4f79a5764afad2427bac|True; TREFOR:LastPageItemID={DB4774A7-3C4B-4FAF-BBFC-1F46BD77F540}; selvbetjening#lang=da'
        }
        products = self._session.post("https://selvbetjening.ewii.com/api/product/GetInstallationProducts", 
            headers=headers_product)
            # , cookies=cookies1)
        
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