"""
All model classes for pyewii
"""


class RawMeterData:
    """
    Class representing JSON meter data
    """

    def __init__(self, meter_type, measurement_data, is_valid):
        self._meter_type = meter_type
        self._measurement_data = measurement_data
        self._is_valid = is_valid

    @property
    def meter_type(self):
        return self._meter_type

    @meter_type.setter
    def meter_type(self, meter_type):
        self._meter_type = meter_type

    @property
    def measurement_data(self):
        return self._measurement_data

    @measurement_data.setter
    def measurement_data(self, measurement_data):
        self._measurement_data = measurement_data

    @property
    def is_valid(self):
        return self._is_valid

    @is_valid.setter
    def is_valid(self, is_valid):
        self._is_valid = is_valid


class TimeSeries:
    """
    Class representing a parsed time series data for a single day.
    """

    def __init__(self, is_valid, data_date, metering_data, detailed_status=None):
        self._is_valid = is_valid
        self._data_date = data_date
        self._metering_data = metering_data
        self._detailed_status = detailed_status

    @property
    def is_valid(self):
        return self._is_valid

    @property
    def detailed_status(self):
        return self._detailed_status

    @property
    def data_date(self):
        return self._data_date

    @property
    def data_points(self):
        return self._metering_data

    def data_points_append(self, metering_data):
        self._metering_data.append(metering_data)

    def get_data_point(self, data_point):
        """Legal data points to ask for are:
        ['temp-forward']
        ['temp-return']
        ['temp-exp-return']
        ['temp-cooling']
        ['energy-start']
        ['energy-end']
        ['energy-used']
        ['energy-exp-used']
        ['energy-exp-end']
        ['water-start']
        ['water-end']
        ['water-used']
        ['water-exp-used']
        ['water-exp-end']
        """
        return self._metering_data[data_point]
