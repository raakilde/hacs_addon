import requests

# copied from curl
cookies = {
    'CookieAccept': 'Allowed',
    'SC_ANALYTICS_GLOBAL_COOKIE': 'e6bc59d905fe42c0a9847ba056fa04e1|True',
    'CookieInformationConsent': '%7B%22website_uuid%22%3A%22c77fa841-89d1-4c34-b8d6-20cc6a105fe4%22%2C%22timestamp%22%3A%222022-02-23T21%3A36%3A29.214Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fselvbetjening.ewii.com%2FAccepter-adgangsdeling%3Fverifyemail%3Draakilde1%40gmail.com%26customerRelation%3D5ecb80f7-ef94-ec11-b400-000d3a2b1f47%26customerRelationVerificationCode%3D446684%26verificationCode%3D500921%26exists%3D0%22%2C%22consent_website%22%3A%22EWII%22%2C%22consent_domain%22%3A%22selvbetjening.ewii.com%22%2C%22user_uid%22%3A%2208db1d5d-8a7e-4375-92d2-b8c4ad0f8bc2%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F98.0.4758.102%20Safari%2F537.36%22%7D',
    '_ga': 'GA1.3.2131963661.1645652189',
    'cuvid': 'c0e5fc50a33a4aab814516e2097a69fb',
    'selvbetjening#lang': 'da',
    'ASP.NET_SessionId': 'yl3kgufkoqy53ohm3w4ksjl4',
    'SNS': '1',
    '917d1132-5173-4d4c-99cf-5782ba3b055c': '10',
    '_gid': 'GA1.3.246384406.1645854749',
    '_sn_m': '{"r":{"n":0,"r":"ewii"}}',
    'cusid': '1645861557821',
    'TREFOR:LastPageItemID': '{0F167ACB-70A7-4E30-8DC7-4EF9B36B2B01}',
    'cuvon': '1645862323849',
    '_sn_n': '{"cs":{"67cc":{"t":{"i":1,"c":"67ccd84c-ff17-4b01-a0b2-fa335846ecd11,1,4,20"},"i":[1677398333259,1],"c":1},"3f7e":{"t":{"i":1,"c":"3f7e04db-d3cb-4124-b323-ed8c235062a82,1,7,20"},"i":[1677394470014,0]}},"ssc":1,"a":{"i":"a8558021-a9c7-43ff-a43e-c73132c7a318"}}',
    '_sn_a': '{"a":{"s":1645858410769,"l":"https://ewii.com/Login?logout","e":1645860477215},"v":"ce14499f-de37-44f3-8b3d-9c9a193c7741"}',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://selvbetjening.ewii.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://selvbetjening.ewii.com/Login?logout',
    'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
}

url_login = 'https://selvbetjening.ewii.com/Login'
data_login = {
    'scController': 'Auth',
    'scAction': 'EmailLogin',
    # Set user/pass
    'Email': 'j.olesen@vindinggaard.dk',
    'Password': 'pass'
}

# urlCSV = https://selvbetjening.ewii.com/api/consumption/csv?installationNumber=114780&consumerNumber=2&meterId=4&counterId=1&type=2&utility=0&unit=KWH&factoryNumber=56048087
#          https://selvbetjening.ewii.com/api/consumption/csv?installationNumber=114780&consumerNumber=2&meterId=204&counterId=1&type=2&utility=10&unit=m3&factoryNumber=69343604
url_csv = 'https://selvbetjening.ewii.com/api/consumption/csv'
params_csv = {
    'installationNumber': '114780',
    'consumerNumber': '1',
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

# Todo
# Detect Water
# Detect Heat
# Detect Power
# Handle hourly (EL) and daily (FJVR/Vand)

# response = requests.post('https://selvbetjening.ewii.com/Login', headers=headers, cookies=cookies, data=data)
# print("Status Code:", response.status_code)
# print(response.headers)
# print(response.text)   #or whatever else you want to do with the request data!

with requests.Session() as session:
    post = session.post(url_login, headers=headers, cookies=cookies, data=data_login)
    req = session.get(url_csv, headers=headers, cookies=cookies, params=params_csv)

    url_content = req.content
    csv_file = open('downloaded.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()
    # print(r.request)
    # print(r.text)   #or whatever else you want to do with the request data!