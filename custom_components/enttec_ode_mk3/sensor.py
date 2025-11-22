from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ENTTECActivitySensor(client)])

class ENTTECActivitySensor(SensorEntity):
    def __init__(self, client):
        self._client = client
    @property
    def name(self):
        return 'ENTTEC ODE mk3 - Last packet timestamp'

    @property
    def state(self):
        return self._client.last_packet_time

    @property
    def unique_id(self):
        return 'enttec_ode_mk3_last_packet'
