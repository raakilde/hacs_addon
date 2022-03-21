from argparse import ArgumentError
from asyncio import exceptions
from datetime import datetime
import json
import logging
import requests
import logging
from models import TimeSeries
from models import RawMeterData



_LOGGER = logging.getLogger(__name__)

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

    def read_latest_measurement(self, meter_json_data):
        _LOGGER.debug(f"Read latest measurement")
        params = (
            ('monthOfYear', datetime.now().month),
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

        if consumption_days.status_code != 200:
            _LOGGER.debug(f"Read latest measurement failed with status {consumption_days.status_code}")
            return ""

        return json.loads(consumption_days.content)

    def process_data(self, meter_type, json_data_to_process):
        _LOGGER.debug(f"Process report for {meter_type}")
        metering_data = {}

        if meter_type == "Electricity":
            print(f"{meter_type}: Process data")
        elif meter_type == "Heat":
            print(f"{meter_type}: Process data")
        else:
            raise NotImplementedError(f"Not implemented {meter_type} with data {json_data_to_process}")

        # Handle heat
        # Handle water
        # Handle electricity
        raw_response = RawMeterData(meter_type, json_data_to_process, (json_data_to_process != ""))

        return raw_response

    # def _parse_result(self, result):
    #     '''
    #     Parse result from API call. This is a JSON dict.
    #     '''
    #     _LOGGER.debug(f"Parsing results")
    #     parsed_result = {}

    #     metering_data = {}
    #     metering_data['year_start'] = result['AarStart']
    #     metering_data['year_end']   = result['AarSlut']
    #     for fl in result['ForbrugsLinjer']['TForbrugsLinje']:
    #         metering_data['temp-forward'] = self._stof(fl['Tempfrem'])
    #         metering_data['temp-return'] = self._stof(fl['TempRetur'])
    #         metering_data['temp-exp-return'] = self._stof(fl['Forv_Retur'])
    #         metering_data['temp-cooling'] = self._stof(fl['Afkoling'])
    #         for reading in fl['TForbrugsTaellevaerk']:
    #             unit = reading['Enhed_Txt']
    #             if reading['IndexNavn'] == "ENG1":
    #                 #_LOGGER.debug(f"Energy use unit is: {unit}")
    #                 multiplier = 1
    #                 if unit == "MWh":
    #                     multiplier = 1000
    #                 metering_data['energy-start'] = self._stof(reading['Start']) * multiplier
    #                 metering_data['energy-end'] = self._stof(reading['Slut']) * multiplier
    #                 metering_data['energy-used'] = self._stof(reading['Forbrug']) * multiplier
    #                 metering_data['energy-exp-used'] = self._stof(fl['ForventetForbrugENG1']) * multiplier
    #                 metering_data['energy-exp-end'] = self._stof(fl['ForventetAflaesningENG1']) * multiplier
    #             elif reading['IndexNavn'] == "M3":
    #                 metering_data['water-start'] = self._stof(reading['Start'])
    #                 metering_data['water-end'] = self._stof(reading['Slut'])
    #                 metering_data['water-used'] = self._stof(reading['Forbrug'])
    #                 metering_data['water-exp-used'] = self._stof(fl['ForventetForbrugM3'])
    #                 metering_data['water-exp-end'] = self._stof(fl['ForventetAflaesningM3'])
    #             else:
    #                 metering_data['extra-start'] = self._stof(reading['Start'])
    #                 metering_data['extra-end'] = self._stof(reading['Slut'])
    #                 metering_data['extra-used'] = self._stof(reading['Forbrug'])

    #     # Because we are fetching data from the full year (or so far)
    #     # The date is generated internally to be todays day of course.
    #     date = datetime.now()

    def read_latest_measurements(self):
        reports = []
        i = 0
        _LOGGER.debug(f"Generate repots")
        #  _LOGGER.debug(f"Getting latest data")

        for meter in self._meters:
            # The first one is normally the active one
            raw_measurements = self.read_latest_measurement(meter[0])
            reports.append(self.process_data(self._meters_type[i], raw_measurements))
            i += 1
            
        return reports