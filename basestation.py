from bleak import BleakClient, BleakScanner, BleakError
import logging

# UUID and command constants
v1_Power_UUID = "0000cb00-0000-1000-8000-00805f9b34fb"
v1_Power_Char = "0000cb01-0000-1000-8000-00805f9b34fb"
CMD_ON = b"\x12\x00\x00\x28\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
CMD_OFF = b"\x12\x01\x00\x28\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
v2_Power_UUID = "00001523-1212-efde-1523-785feabcd124"
v2_Power_Char = "00001525-1212-efde-1523-785feabcd124"
CMD_ON_V2 = b"\x01"
CMD_OFF_V2 = b"\x00"

PWR_CHARACTERISTIC = "00001525-1212-EFDE-1523-785FEABCD124"

LOGGER = logging.getLogger(__name__)

async def discover():
    """Discover Bluetooth LE devices."""
    devices = await BleakScanner.discover()
    LOGGER.debug(f"Discovered devices: {[{'address': device.address, 'name': device.name} for device in devices]}")
    basestations = [device for device in devices if device.name and (device.name.startswith("HTC BS ") or device.name.startswith("LHB-"))]
    for bs in basestations:
        LOGGER.debug(f"Found Base Station: {bs.name}")
    return basestations

class BasestationInstance:
    def __init__(self, mac: str) -> None:
        self._mac = mac
        self._device = BleakClient(self._mac)
        self._is_on = None
        self._connected = None

    async def _send(self, command):
        if not self._connected:
            LOGGER.debug("Connecting to device...")
            await self.connect()

        try:
            if command:  # True for ON
                try:
                    await self._device.write_gatt_char(v2_Power_Char, CMD_ON_V2, response=True)
                except BleakError:
                    await self._device.write_gatt_char(v1_Power_Char, CMD_ON, response=True)
            else:  # False for OFF
                try:
                    await self._device.write_gatt_char(v2_Power_Char, CMD_OFF_V2, response=True)
                except BleakError:
                    await self._device.write_gatt_char(v1_Power_Char, CMD_OFF, response=True)
            LOGGER.info(f"Command {'ON' if command else 'OFF'} sent successfully.")
        except BleakError as e:
            LOGGER.error(f"Failed to send command: {e}")

        await self.disconnect()

    @property
    def mac(self):
        return self._mac

    @property
    def is_on(self):
        return self._is_on
    
    async def turn_on(self):
        await self._send(True)
        self._is_on = True

    async def turn_off(self):
        await self._send(False)
        self._is_on = False

    async def connect(self):
        if not self._connected:
            await self._device.connect()
            self._connected = True
            LOGGER.debug(f"Connected to {self._device.address}")

    async def disconnect(self):
        if self._connected:
            await self._device.disconnect()
            self._connected = False
            LOGGER.debug(f"Disconnected from {self._device.address}")
    
    async def read_state(self):
        if not self._connected:
            await self.connect()

        if self._connected:  # Ensure the device is connected before attempting to read
            try:
                state = await self._device.read_gatt_char(PWR_CHARACTERISTIC)
                self._is_on = state != CMD_OFF_V2
            except BleakError as e:
                LOGGER.error(f"Error reading state from base station {self._mac}: {e}")
        else:
            LOGGER.error(f"Failed to connect to base station {self._mac}")

        await self.disconnect()
