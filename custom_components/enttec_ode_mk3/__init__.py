from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .artnet_client import ArtNetClient
from .const import DOMAIN, DEFAULT_PORT, CONF_HOST, CONF_PORT, CONF_UNIVERSE
import logging

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ['light', 'sensor', 'binary_sensor']

async def async_setup(hass: HomeAssistant, config: ConfigType):
    # Optional YAML config support
    conf = config.get(DOMAIN)
    if not conf:
        return True
    host = conf.get(CONF_HOST)
    port = conf.get(CONF_PORT, DEFAULT_PORT)
    universe = conf.get(CONF_UNIVERSE, 0)
    client = ArtNetClient(host, port, universe)
    await client.connect(hass)
    hass.data.setdefault(DOMAIN, {})['default'] = client
    return True

async def async_setup_entry(hass, entry):
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    universe = entry.data.get(CONF_UNIVERSE, 0)
    client = ArtNetClient(host, port, universe)
    await client.connect(hass)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    client = hass.data[DOMAIN].pop(entry.entry_id)
    await client.disconnect()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
