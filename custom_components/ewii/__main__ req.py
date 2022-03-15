# from cgitb import html
# from http import cookies
from email import header
from http import cookies
import json
from urllib import response
from httpx import head
import pip._vendor.requests 
import requests
# from requests_html import HTMLSession


url_base = "https://selvbetjening.ewii.com"
url_login = url_base + "/Login"
url_get_address = url_base + "/api/product/GetAddressPickerViewModel"
url_set_address = url_base + "/api/product/SetSelectedAddressPickerElement"
url_get_install = url_base + "/api/product/GetInstallationProducts"

# Login
data_login = {
    "scController": "Auth",
    "scAction": "EmailLogin",
    "Email": "",
    "Password": "",
}
headers_login = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

# Get Address
payload_get_address = "false"
headers_get_address = {
    'Content-Type': 'application/json;charset=UTF-8',
}

# Set Address
# payload_set_address = ""
headers_set_address = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
}

# Get Installation Product
payload_get_install = ""
headers_get_install = ""

class Ewii:
    """
    Primary exported interface for ewii.dk API wrapper.
    """

    def __init__(self, email, password):
        self._email = email
        self._password = password
        self._session = requests.session()
        self._meters = []

    def login_and_prime(self):

        # Login
        data_login["Email"] = self._email
        data_login["Password"] = self._password 
        response_login = self._session.post(url_login, headers=headers_login, data=data_login, allow_redirects=True)

        # Get address 
        response_get_address = self._session.post(url_get_address, headers=headers_get_address, data=payload_get_address.encode('utf-8'))
        # print(json.dumps(json.loads(response_get_address.content), indent=2))

        # Set address element
        json_get_address = json.loads(response_get_address.content)
        elements = json_get_address['Elements']
        index = json_get_address['SelectedId']
        payload_set_address = json.dumps(elements[index])
        response_set_address = self._session.post(url_set_address, headers=headers_set_address, data=payload_set_address.encode('utf-8'))

        # Get Installation Product       
        response_get_install = self._session.post(url_get_install, headers=headers_get_install, data=payload_get_install)
        json_get_install = json.loads(response_get_install.content)
        elements = json_get_install['Elements']

        # Detect installation
        for product in elements:
            self._meter_types.append(product['ProductTypeName'])
            

        # response_water = self._session.get("https://selvbetjening.ewii.com/api/consumption/meters?utility=Water")
        # response_electricity = self._session.get("https://selvbetjening.ewii.com/api/consumption/meters?utility=Electricity")
        # response_heat = self._session.get("https://selvbetjening.ewii.com/api/consumption/meters?utility=Heat")

        
        # print(json.dumps(json.loads(response_electricity.content), indent=2))

        # params = ( # el
        #     ('installationNumber', '114780'),
        #     ('consumerNumber', '2'),
        #     ('meterId', '4'),
        #     ('counterId', '1'),
        #     ('type', '2'),
        #     ('utility', '0'),
        #     ('unit', 'KWH'),
        #     ('factoryNumber', '56048087'),
        # )
        # response_data_el = self._session.get('https://selvbetjening.ewii.com/api/consumption/origin', params=params)

        # print(json.dumps(json.loads(response_water.content), indent=2))

        # params = (
        #     ('installationNumber', '114780'),
        #     ('consumerNumber', '2'),
        #     ('meterId', '204'),
        #     ('counterId', '1'),
        #     ('type', '2'),
        #     ('utility', '10'),
        #     ('unit', 'm3'),
        #     ('factoryNumber', '69343604'),
        # )

        # response_data_water = self._session.get('https://selvbetjening.ewii.com/api/consumption/origin', params=params)

        return  response_login.status_code ==  200 and \
                response_get_address.status_code ==  200 and \
                response_set_address.status_code ==  204 and \
                response_get_install.status_code ==  200

    def detect_meters(self):

        for type in self._meter_types:
            # Get type
            

            
        return False

if __name__ == "__main__":
    ewii = Ewii("j.olesen@vindinggaard.dk", "fuzbyk-fyrbyK-2jeppy")
    ewii.login_and_prime()
    ewii.detect_meters()