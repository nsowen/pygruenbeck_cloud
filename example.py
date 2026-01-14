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
                username="xxx",
                password="yyy",
            ) as gruenbeck:
                gruenbeck.logger = _LOGGER

                devices = await gruenbeck.get_devices()
                if len(devices) <= 0:
                    _LOGGER.warning("No devices found!")
                    return

                # Use first Device
                await gruenbeck.set_device(devices[0])

                await gruenbeck.off_sd()
                await gruenbeck.leave_sd()

                # Update parameter values for Device
                async def update_parameter_value(parameter_name: str, new_value: Any):
                    # Get Params
                    cur_device = await gruenbeck.get_device_infos_parameters()
                    old_value = getattr(cur_device.parameters, parameter_name)
                    print(f"Old value for {parameter_name} is: {old_value}")

                    # Set new value
                    new_value = {parameter_name: new_value}

                    # Update value
                    cur_device = await gruenbeck.update_device_infos_parameters(
                        new_value
                    )
                    print(
                        f"Value changed for {parameter_name} to: {getattr(cur_device.parameters, parameter_name)}"
                    )

                    input(f"Press enter to restore {old_value}...")
                    # Restore old value
                    new_value = {parameter_name: old_value}
                    cur_device = await gruenbeck.update_device_infos_parameters(
                        new_value
                    )
                    print(
                        f"Restored value for {parameter_name} is: {getattr(cur_device.parameters, parameter_name)}"
                    )

                # await update_parameter_value("regeneration_mode", 1)

                # Listener
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

                _LOGGER.info("Get parameters...")
                await gruenbeck.get_device_infos_parameters()
                await asyncio.sleep(0.5)
                _LOGGER.info("Refresh realtime...")
                await gruenbeck.refresh_sd()
                await asyncio.sleep(0.5)
                _LOGGER.info("Enter realtime...")
                await gruenbeck.enter_sd()
                await asyncio.sleep(0.5)

                count = 0

                while count < 100:
                    await gruenbeck.update_sd()
                    #_LOGGER.debug(f"Device after update: {device.realtime.to_dict()}")
                    #_LOGGER.debug(await gruenbeck.get_device_salt_measurements())
                    #_LOGGER.debug("Wait 60 seconds in main thread...")
                    await asyncio.sleep(1)
                    count += 1

                await gruenbeck.off_sd()
                await gruenbeck.leave_sd()

                #_LOGGER.info("Start listener task...")
                #task = asyncio.create_task(listen())
                #while self.unsub == False:
                #    # Get Device information every 360 seconds
                #    _LOGGER.debug("Wait 360 seconds in main thread...")
                #    await asyncio.sleep(60)##

                #    await gruenbeck.get_device_infos()
                #    device = await gruenbeck.get_device_infos_parameters()
                #    _LOGGER.debug(f"Device after update: {device}")
                #    await gruenbeck.enter_sd()
                #    await gruenbeck.refresh_sd()

        except PyGruenbeckCloudConnectionError as ex:
            _LOGGER.error(ex)
        except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
            #await gruenbeck.disconnect()
            #_LOGGER.info("Stopping Task")
            #task.cancel()
            _LOGGER.info("Quitting!")
        finally:
            _LOGGER.debug("Got finish signal, wait for disconnect...")
            await gruenbeck.off_sd()
            await gruenbeck.leave_sd()


asyncio.run(TestGruenbeck().init())
