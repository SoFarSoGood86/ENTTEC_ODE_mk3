from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ENTTECConnectionSensor(client)])

class ENTTECConnectionSensor(BinarySensorEntity):
    def __init__(self, client):
        self._client = client
    @property
    def name(self):
        return 'ENTTEC ODE mk3 - ArtNet connected'

    @property
    def is_on(self):
        return self._client.connected

    @property
    def unique_id(self):
        return 'enttec_ode_mk3_connected'
