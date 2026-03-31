# pylint: skip-file
"""Demo file for testing."""
import asyncio
import logging
from typing import Any

from pygruenbeck_cloud import PyGruenbeckCloud
from pygruenbeck_cloud.exceptions import PyGruenbeckCloudConnectionError
from pygruenbeck_cloud.models import Device

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
)
_LOGGER = logging.getLogger(__name__)


class TestGruenbeck:
    unsub: bool = False

    def callback_func(self, data: Device):
        """Callback function."""
        _LOGGER.info(f"Callback data: {data}")

    async def init(self):
        """Demo function for testing."""
        try:
            async with PyGruenbeckCloud(
                username="<USERNAME>",
                password="<PASSWORD>",
            ) as gruenbeck:
                gruenbeck.logger = _LOGGER

                devices = await gruenbeck.get_devices()
                if len(devices) <= 0:
                    _LOGGER.warning("No devices found!")
                    return

                # Use first Device
                await gruenbeck.set_device(devices[0])

                if gruenbeck.device.is_softliq_se():
                    # SE-series: use per-poll cycle (refresh → enter → update → leave → off).
                    # Do NOT hold the realtime session open across polls — the server drops
                    # it after ~10-15 min and updates silently stop.
                    _LOGGER.info("SE-series device detected, using polling mode...")
                    await gruenbeck.get_device_infos_parameters()

                    count = 0
                    while count < 5:
                        _LOGGER.info("Polling device (cycle %d)...", count + 1)
                        device = await gruenbeck.poll_sd()
                        _LOGGER.debug("Device after poll: %s", device.realtime.to_dict())
                        await asyncio.sleep(60)
                        count += 1
                else:
                    # SL/SD-series: use WebSocket listener
                    _LOGGER.info("SL/SD-series device detected, using WebSocket mode...")

                    async def listen():
                        try:
                            await gruenbeck.connect()
                        except Exception as ex:
                            _LOGGER.error(ex)
                            self.unsub = True
                            return

                        try:
                            await gruenbeck.listen(callback=self.callback_func)
                        except Exception as ex:
                            _LOGGER.error(ex)

                        await gruenbeck.disconnect()
                        self.unsub = True

                    _LOGGER.info("Start listener task...")
                    task = asyncio.create_task(listen())
                    while not self.unsub:
                        _LOGGER.debug("Wait 360 seconds in main thread...")
                        await asyncio.sleep(360)
                        await gruenbeck.get_device_infos()
                        device = await gruenbeck.get_device_infos_parameters()
                        _LOGGER.debug("Device after update: %s", device)
                        await gruenbeck.enter_sd()
                        await gruenbeck.refresh_sd()

        except PyGruenbeckCloudConnectionError as ex:
            _LOGGER.error(ex)
        except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
            _LOGGER.info("Quitting!")
        finally:
            _LOGGER.debug("Got finish signal, wait for disconnect...")
            if gruenbeck.device and not gruenbeck.device.is_softliq_se():
                await gruenbeck.disconnect()


asyncio.run(TestGruenbeck().init())
