from datetime import datetime, timedelta
import json
import logging
import requests
from .models import TimeSeries
from .models import RawMeterData

_LOGGER = logging.getLogger(__name__)

url_base = "https://selvbetjening.ewii.com"
url_login = url_base + "/Login"
url_get_address = url_base + "/api/product/GetAddressPickerViewModel"
url_set_address = url_base + "/api/product/SetSelectedAddressPickerElement"
url_get_install = url_base + "/api/product/GetInstallationProducts"
url_meter = url_base + "/api/consumption/meters?utility="

# Login
data_login = {
    "scController": "Auth",
    "scAction": "EmailLogin",
    "Email": "",
    "Password": "",
}
headers_login = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

# Get Address
payload_get_address = "false"
headers_get_address = {
    "Content-Type": "application/json;charset=UTF-8",
}

# Set Address
headers_set_address = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
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
        response_login = self._session.post(
            url_login, headers=headers_login, data=data_login, allow_redirects=True
        )

        # Get address
        response_get_address = self._session.post(
            url_get_address,
            headers=headers_get_address,
            data=payload_get_address.encode("utf-8"),
        )
        # print(json.dumps(json.loads(response_get_address.content), indent=2))

        # Set address element
        json_get_address = json.loads(response_get_address.content)
        elements = json_get_address["Elements"]
        index = json_get_address["SelectedId"]
        payload_set_address = json.dumps(elements[index])
        response_set_address = self._session.post(
            url_set_address,
            headers=headers_set_address,
            data=payload_set_address.encode("utf-8"),
        )

        # Get Installation Product
        response_get_install = self._session.post(
            url_get_install, headers=headers_get_install, data=payload_get_install
        )
        json_get_install = json.loads(response_get_install.content)
        elements = json_get_install["Elements"]

        # Detect installation
        for product in elements:
            # Must be owned by user and should not be Internet
            if product['Product']['CurrentlyOwned'] and product["ProductTypeName"] != 'Internet':
                self._meters_type.append(product["ProductTypeName"])
                response = self._session.get(url_meter + product["ProductTypeName"])
                self._meters.append(json.loads(response.content))

        return (
            response_login.status_code == 200
            and response_get_address.status_code == 200
            and response_set_address.status_code == 204
            and response_get_install.status_code == 200
        )

    def read_latest_measurement(self, meters_json_data, date_to_get):
        _LOGGER.debug(f"Read latest measurement")
        consumption_days_json_list = []

        for meter_json_data in meters_json_data:
            params = (
                ("monthOfYear", date_to_get.month),
                (
                    "installationNumber",
                    meter_json_data["Installation"]["InstallationNumber"],
                ),
                ("consumerNumber", meter_json_data["Installation"]["ConsumerNumber"]),
                ("meterId", meter_json_data["MeterId"]),
                ("counterId", meter_json_data["CounterId"]),
                ("type", meter_json_data["ReadingType"]),
                ("utility", meter_json_data["Utility"]),
                ("unit", meter_json_data["Unit"]),
                ("factoryNumber", meter_json_data["FactoryNumber"]),
            )

            consumption_days = self._session.get(
                "https://selvbetjening.ewii.com/api/consumption/days", params=params
            )

            _LOGGER.debug(
                f"Read latest measurement failed with status {consumption_days.status_code}"
            )
            if consumption_days.status_code != 200:
                _LOGGER.debug(
                    f"Read latest measurement failed with status {consumption_days.status_code}"
                )
                
            else 
                consumption_days_json_list.append(json.loads(consumption_days.content))

        return consumption_days_json_list

    def process_data(self, meter_type, json_data_to_process, date_to_get):
        _LOGGER.debug(f"Process report for {meter_type}")
        metering_data = dict()
        data_valid = False

        # Find index of year
        index_of_year = -1
        array_of_years = json_data_to_process[0]["Series"]
        for i in range(len(array_of_years)):
            if array_of_years[i]["Name"] == f"{date_to_get.year}":
                index_of_year = i

        if index_of_year == -1:
            # raise NotFoundErr(f"Index not found {json_data_to_process}")
            return metering_data

        # Handle Electricity
        if meter_type == "Electricity":
            _LOGGER.debug(f"{meter_type}: Process data")
            # Only one time table in electricity
            metering_data["electricity-usage"] = float(
                json_data_to_process[0]["Groups"][date_to_get.day - 1]["Values"][
                    index_of_year
                ]
            )
            metering_data["electricity-unit"] = json_data_to_process[0]["Unit"]
            data_valid = metering_data["electricity-usage"] != None
        # Handle Water
        elif meter_type == "Water":
            _LOGGER.debug(f"{meter_type}: Process data")
            # Only one time table in water
            metering_data["water-usage"] = float(
                json_data_to_process[0]["Groups"][date_to_get.day - 1]["Values"][
                    index_of_year
                ]
            )
            metering_data["water-unit"] = json_data_to_process[0]["Unit"]
            data_valid = metering_data["water-usage"] != None
        elif meter_type == "Heat":
            _LOGGER.debug(f"{meter_type}: Process data")
            # Must be 2 tables for heat MWh and m3
            metering_data["energy-usage"] = float(
                json_data_to_process[0]["Groups"][date_to_get.day - 1]["Values"][
                    index_of_year
                ]
            )
            metering_data["energy-usage-unit"] = json_data_to_process[0]["Unit"]

            metering_data["water-usage"] = float(
                json_data_to_process[1]["Groups"][date_to_get.day - 1]["Values"][
                    index_of_year
                ]
            )
            # Bug in time table always showing MWh
            metering_data["water-usage-unit"] = "m3"

            # Forbrug MWh divideret med forbrug m³) x 860.
            metering_data["water_temperature_cooling"] = (metering_data["energy-usage"] / metering_data["water-usage"]) * 860
            metering_data["energy-unit"] = "C"
            

            data_valid = metering_data["water-usage"] != None
        # Handle heat/other
        else:
            _LOGGER.debug(
                f"Not implemented {meter_type} with data {json_data_to_process}"
            )
            raise NotImplementedError(
                f"Not implemented {meter_type} with data {json_data_to_process}"
            )

        if data_valid is False:
            metering_data.clear()

        return metering_data

    def _find_active_meters(self, meter_types):
        active_meter_types = []
        for meter_type in meter_types:
            if meter_type["Status"] == 'aktiv':
                active_meter_types.append(meter_type)
        
        return active_meter_types

    def read_latest_measurements(self):
        i = 0
        reports = dict()
        _LOGGER.debug(f"Generate repots")
        #  _LOGGER.debug(f"Getting latest data")
        # Get yesterdays date
        date_to_get = datetime.now() - timedelta(days=1)
        time_series = TimeSeries(True, date_to_get, "", "")

        for meter in self._meters:
            # Find all active type meters
            active_meter_types = self._find_active_meters(meter)
            raw_measurements = self.read_latest_measurement(active_meter_types, date_to_get)
            measurements = self.process_data(
                self._meters_type[i], raw_measurements, date_to_get
            )
            if len(measurements) > 0:
                reports.update(measurements)
            i += 1

        time_series = TimeSeries((len(reports) > 0), date_to_get, reports)

        return time_series
