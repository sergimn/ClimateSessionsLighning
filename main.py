import asyncio
import logging
import json
import os
import sys

from pywizlight import PilotBuilder, wizlight


async def dispatch(setup):
    for bulb in setup:
        logger.info(f"Dispatching bulb with IP {bulb['ip']}")
        await control(ip=bulb['ip'], sequence=bulb['sequence'])
        # TODO: Add support for multiple bulbs at the same time. Using "asyncio.create_task()" seems to break the UDP
        #       packet transmission. I need to investigate "asyncio" further


async def control(ip, sequence):
    bulb = wizlight(ip)
    for a in sequence:
        rgb = (a[0], a[1], a[2])
        logger.info(f"Turning light {ip} to color {rgb} at speed {a[3]}")
        await bulb.turn_on(PilotBuilder(rgb=rgb, speed=a[3]))


def setup_logger():
    if not os.environ.setdefault('LOG_LEVEL', "ERROR") in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        deb_level = logging.ERROR
    else:
        if os.environ['LOG_LEVEL'] == "DEBUG": deb_level = logging.DEBUG
        if os.environ['LOG_LEVEL'] == "INFO": deb_level = logging.INFO
        if os.environ['LOG_LEVEL'] == "WARNING": deb_level = logging.WARNING
        if os.environ['LOG_LEVEL'] == "ERROR": deb_level = logging.ERROR
        if os.environ['LOG_LEVEL'] == "CRITICAL": deb_level = logging.CRITICAL

    global logger
    logger = logging.getLogger("CSL Logger")
    logger.setLevel(deb_level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


if __name__ == '__main__':
    setup_logger()
    logger.debug("Reading scene file...")
    with open(sys.argv[1]) as setup:
        obj_setup = json.load(setup)
    asyncio.run(dispatch(obj_setup))
