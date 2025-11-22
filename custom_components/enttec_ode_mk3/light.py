from homeassistant.components.light import LightEntity, COLOR_MODE_BRIGHTNESS
from homeassistant.const import ATTR_BRIGHTNESS
from .const import DOMAIN, MAX_CHANNELS

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]
    # Default expose first 16 channels as lights; can be extended
    count = entry.options.get('channel_count', 16)
    entities = [ENTTECChannelLight(client, i+1) for i in range(count)]
    async_add_entities(entities)

class ENTTECChannelLight(LightEntity):
    def __init__(self, client, channel):
        self._client = client
        self._channel = channel
        self._attr_name = f"ENTTEC ODE mk3 Channel {channel}"
        self._attr_unique_id = f"enttec_ode_mk3_channel_{channel}"

    @property
    def is_on(self):
        return self._client.get_channel(self._channel) > 0

    @property
    def brightness(self):
        return self._client.get_channel(self._channel)

    @property
    def supported_color_modes(self):
        return {COLOR_MODE_BRIGHTNESS}

    def turn_on(self, **kwargs):
        value = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._client.set_channel(self._channel, value)

    def turn_off(self, **kwargs):
        self._client.set_channel(self._channel, 0)

    async def async_update(self):
        # pull current local value
        pass
