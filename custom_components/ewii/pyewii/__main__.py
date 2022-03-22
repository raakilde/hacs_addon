"""
Main for pyewii
"""
import argparse
from asyncio.log import logger
import logging
from xml.parsers.expat import model
from ewii import Ewii
from models import RawMeterData

_LOGGER = logging.getLogger(__name__)

def main():
    """
    Main method
    """
    parser = argparse.ArgumentParser("pyewii")
    parser.add_argument("--log", action="store", required=False)
    # parser.add_argument("--metering-point", action="store", required=False)

    args = parser.parse_args()

    _configureLogging(args)

    try:
        ewii = Ewii("j.olesen@vindinggaard.dk", "fuzbyk-fyrbyK-2jeppy")
        ewii.login_and_prime()
        measurements = ewii.read_latest_measurements()

        for measurement in measurements:
            # The first one is normally the active one
            if measurement.is_valid == True:
                print(f"{measurement.meter_type} is valid")
            else:
                _LOGGER.debug(f"Error getting data. Status: {measurement.is_valid}. Error: {measurement.detailed_status}")
    except Exception as e:
        _LOGGER.error(f"Exception occuered: {e.args[0]}")

def _configureLogging(args):
    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError("Invalid log level: %s" % args.log)

        logging.basicConfig(level=numeric_level)


if __name__ == "__main__":
    main()
