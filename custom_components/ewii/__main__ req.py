# from cgitb import html
# from http import cookies
from email import header
from http import cookies
import json
from urllib import response
from httpx import head
import pip._vendor.requests 
import requests

url_base = "https://selvbetjening.ewii.com"
url_login = url_base + "/Login"
url_get_address = url_base + "/api/product/GetAddressPickerViewModel"
url_set_address = url_base + "/api/product/SetSelectedAddressPickerElement"
url_get_install = url_base + "/api/product/GetInstallationProducts"
url_meter =url_base + "/api/consumption/meters?utility="

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
        self._meters_type = []
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
            self._meters_type.append(product['ProductTypeName'])
            response = self._session.get(url_meter + product['ProductTypeName'])
            self._meters.append(json.loads(response.content))

        return  response_login.status_code          ==  200 and \
                response_get_address.status_code    ==  200 and \
                response_set_address.status_code    ==  204 and \
                response_get_install.status_code    ==  200

    def generate_report(self, meter_json_data):
        params = (
            ('monthOfYear', '1'),
            ('installationNumber', meter_json_data["Installation"]["InstallationNumber"]),
            ('consumerNumber', meter_json_data["Installation"]["ConsumerNumber"]),
            ('meterId', meter_json_data["MeterId"]),
            ('counterId', meter_json_data["CounterId"]),
            ('type', meter_json_data["ReadingType"]),
            ('utility', meter_json_data["Utility"]),
            ('unit', meter_json_data["Unit"]),
            ('factoryNumber', meter_json_data["FactoryNumber"]),
        )
        
        consumption_days = self._session.get('https://selvbetjening.ewii.com/api/consumption/days', params=params)
        return json.loads(consumption_days.content)

    def process_data(self, json_data_to_process, meter_type):
        # Handle heat
        # Handle water
        # Handle electricity
        print(json_data_to_process)

    def generate_reports(self):
        i = 0
        for meter in self._meters:
            # The first one is normally the active one
            measurements = self.generate_report(meter[0])
            self.process_data(measurements, self._meters_type[i])
            i += 1
            
        

if __name__ == "__main__":
    ewii = Ewii("j.olesen@vindinggaard.dk", "fuzbyk-fyrbyK-2jeppy")
    ewii.login_and_prime()
    ewii.generate_reports()
    # ewii.detect_meters()