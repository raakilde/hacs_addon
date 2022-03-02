from aiohttp import request
from async_timeout import timeout
import requests

# copied from curl
url_login = 'https://selvbetjening.ewii.com/Login'
data_login = {
    'scController': 'Auth',
    'scAction': 'EmailLogin',
    # Set user/pass
    'Email': 'j.olesen@vindinggaard.dk',
    'Password': 'ithooriLoo123'
}

# https://selvbetjening.ewii.com/api/consumption/hours?monthOfYear=2&dayOfMonth=28&installationNumber=114780&consumerNumber=2&meterId=4&counterId=1&type=2&utility=0&unit=KWH&factoryNumber=56048087
#

# urlCSV = https://selvbetjening.ewii.com/api/consumption/csv?installationNumber=114780&consumerNumber=2&meterId=4&counterId=1&type=2&utility=0&unit=KWH&factoryNumber=56048087
#          https://selvbetjening.ewii.com/api/consumption/csv?installationNumber=114780&consumerNumber=2&meterId=204&counterId=1&type=2&utility=10&unit=m3&factoryNumber=69343604
url_csv = 'https://selvbetjening.ewii.com/api/consumption/csv'
params_csv = {
    'installationNumber': '114780', # in
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
base_url = 'https://selvbetjening.ewii.com'
url_login = base_url + '/Login'
data_login = {
    'scController': 'Auth',
    'scAction': 'EmailLogin',
    # Set user/pass
    'Email': 'j.olesen@vindinggaard.dk',
    'Password': 'pass'
}

#

# urlCSV = https://selvbetjening.ewii.com/api/consumption/csv?installationNumber=114780&consumerNumber=2&meterId=4&counterId=1&type=2&utility=0&unit=KWH&factoryNumber=56048087
#          https://selvbetjening.ewii.com/api/consumption/csv?installationNumber=114780&consumerNumber=2&meterId=204&counterId=1&type=2&utility=10&unit=m3&factoryNumber=69343604
# url_f = 'https://selvbetjening.ewii.com/api/consumption/hours?monthOfYear=2&dayOfMonth=28&installationNumber=114780&consumerNumber=2&meterId=4&counterId=1&type=2&utility=0&unit=KWH&factoryNumber=56048087'
url_datapoints = base_url + '/api/consumption/hours'
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

# Todo
# Detect Water
# Detect Heat
# Detect Power
# Handle hourly (EL) and daily (FJVR/Vand)

# response = requests.post('https://selvbetjening.ewii.com/Login', headers=headers, cookies=cookies, data=data)
# print("Status Code:", response.status_code)
# print(response.headers)
# print(response.text)   #or whatever else you want to do with the request data!

session1 = requests.session()
post = session1.post(url_login, data=data_login)
req = session1.get(url_datapoints, params=params_datapoints)

with requests.Session() as session:
    post = session.post(url_login, data=data_login)
    req = session.get(url_datapoints, params=params_datapoints)

    result_json = req.json()
    result_json = result_json
    # req = session.get(url_csv, headers=headers, cookies=cookies, params=params_csv)
    # url_content = req.content
    # csv_file = open('downloaded.csv', 'wb')

    # csv_file.write(url_content)
    # csv_file.close()
    # print(r.request)
    # print(r.text)   #or whatever else you want to do with the request data!