import asyncio
import logging
import json
import sys

from pywizlight import PilotBuilder, wizlight


async def dispatch(setup):
    for bulb in setup:
        logger.info(f"Dispatching bulb with IP {bulb['ip']}")
        asyncio.create_task(control(ip=bulb['ip'], sequence=bulb['sequence']))


async def control(ip, sequence):
    bulb = wizlight(ip)
    for a in sequence:
        rgb = (a[0], a[1], a[2])
        logger.info(f"Turning light {ip} to color {rgb} at speed {a[3]}")
        await bulb.turn_on(PilotBuilder(rgb=rgb, speed=a[3]))


def setup_logger():
    global logger
    logger = logging.getLogger("CSL Logger")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


if __name__ == '__main__':
    setup_logger()
    logger.info("Reading scene file...")
    with open(sys.argv[1]) as setup:
        obj_setup = json.load(setup)
    asyncio.run(dispatch(obj_setup))

