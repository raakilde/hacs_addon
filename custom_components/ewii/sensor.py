"""Platform for Ewii sensor integration."""
import logging
import datetime

from homeassistant.const import (
    TEMP_CELSIUS,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_GAS,
    ENERGY_KILO_WATT_HOUR,
    VOLUME_CUBIC_METERS,
)
from homeassistant.components.sensor import (
    SensorEntity,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL,
    STATE_CLASS_TOTAL_INCREASING,
)

# from homeassistant.helpers.entity import Entity
from custom_components.ewii.pyewii.ewii import Ewii
from custom_components.ewii.pyewii.models import TimeSeries

_LOGGER = logging.getLogger(__name__)
from .const import DOMAIN


async def async_setup_entry(hass, config, async_add_entities):
    """Set up the sensor platform."""

    hass_ewii = hass.data[DOMAIN][config.entry_id]

    ## Sensors so far
    # Year, Month, Day? We'll fetch data once per day.

    water_series = {"usage"}
    heat_series = {"forward", "return", "exp-return", "cooling"}
    electricity_series = {"usage"}
    sensors = []

    for s in water_series:
        sensors.append(EwiiEnergy(f"Ewii Water {s}", s, "water", hass_ewii))

    # for s in heat_series:
    #     sensors.append(EwiiEnergy(f"Ewii Heat Temperature {s}", s, "temp", hass_ewii))

    for s in electricity_series:
        sensors.append(EwiiEnergy(f"Ewii Electricity {s}", s, "electricity", hass_ewii))

    # TODO set on detected features

    # sensors.append(EwiiEnergy("", "", ewii))
    async_add_entities(sensors)


class EwiiEnergy(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name, sensor_point, sensor_type, client):
        """Initialize the sensor."""
        self._state = None
        self._data_date = None
        self._data = client

        self._attr_name = name

        self._sensor_value = f"{sensor_type}-{sensor_point}"
        self._attr_unique_id = f"ewii-{self._sensor_value}"
        if sensor_type == "electricity":
            self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
            self._attr_icon = "mdi:lightning-bolt-circle"
            self._attr_device_class = DEVICE_CLASS_ENERGY
            self._attr_state_class = STATE_CLASS_MEASUREMENT  # STATE_CLASS_TOTAL_INCREASING or STATE_CLASS_TOTAL
            # self._attr_last_reset = datetime.datetime(2000, 1, 1, 0, 0, 0) #JSON: "2000-01-01T00:00:00"
        elif sensor_type == "water":
            self._attr_native_unit_of_measurement = VOLUME_CUBIC_METERS
            self._attr_icon = "mdi:water"
            self._attr_state_class = STATE_CLASS_MEASUREMENT  # STATE_CLASS_TOTAL
            # Only gas can be measured in m3
            self._attr_device_class = DEVICE_CLASS_GAS
        else:
            self._attr_native_unit_of_measurement = TEMP_CELSIUS
            self._attr_icon = "mdi:thermometer"
            self._attr_device_class = DEVICE_CLASS_TEMPERATURE
            self._attr_state_class = STATE_CLASS_MEASUREMENT

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        attributes = dict()
        attributes["Metering date"] = self._data_date
        attributes["metering_date"] = self._data_date
        return attributes

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug(f"Setting status for {self._attr_name}")

        self._data.update()

        # self._data_date = self._data[0].data_date()
        self._data_date = self._data.get_data_date()
        self._attr_native_value = self._data.get_data(self._sensor_value)
        _LOGGER.debug(
            f"Done setting status for {self._attr_name} = {self._attr_native_value} {self._attr_native_unit_of_measurement}"
        )
