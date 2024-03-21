"""Platform for basestation integration."""
from __future__ import annotations

import logging

from .basestation import BasestationInstance
import voluptuous as vol

from .basestation import BasestationInstance

from pprint import pformat

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (PLATFORM_SCHEMA, LightEntity)
from homeassistant.const import CONF_NAME, CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger("basestation")

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_MAC): cv.string,
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Godox Light platform."""
    # Add devices
    _LOGGER.info(pformat(config))
    
    light = {
        "name": config[CONF_NAME],
        "mac": config[CONF_MAC]
    }
    
    add_entities([BasestationLight(light)])

class BasestationLight(LightEntity):
    """Representation of an Basestation"""

    def __init__(self, light) -> None:
        """Initialize an GodoxLight."""
        _LOGGER.info(pformat(light))
        self._light = BasestationInstance(light["mac"])
        self._name = light["name"]
        self._state = None

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the basestation to turn on."""
        
        await self._light.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the basestation to turn off."""
        await self._light.turn_off()

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._light.is_on