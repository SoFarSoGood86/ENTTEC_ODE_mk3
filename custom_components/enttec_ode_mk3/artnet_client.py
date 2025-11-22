import asyncio
import socket
import time
from .const import MAX_CHANNELS

class ArtNetClient:
    def __init__(self, host: str, port: int, universe: int):
        self.host = host
        self.port = port
        self.universe = universe
        self.sock = None
        self.channels = [0] * MAX_CHANNELS
        self.connected = False
        self.last_packet_time = None
        self._hass = None
        self._lock = asyncio.Lock()
        self._listeners = []

    async def connect(self, hass=None):
        self._hass = hass
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connected = True
        return True

    async def disconnect(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
        self.connected = False

    def register_listener(self, cb):
        if cb not in self._listeners:
            self._listeners.append(cb)

    def unregister_listener(self, cb):
        if cb in self._listeners:
            self._listeners.remove(cb)

    def _notify(self, channel, value):
        for cb in list(self._listeners):
            try:
                cb(channel, value)
            except Exception:
                pass

    def set_channel(self, channel: int, value: int):
        if 1 <= channel <= MAX_CHANNELS:
            self.channels[channel-1] = max(0, min(255, int(value)))
            self._send_artdmx()
            self._notify(channel, self.channels[channel-1])

    def get_channel(self, channel: int) -> int:
        if 1 <= channel <= MAX_CHANNELS:
            return self.channels[channel-1]
        return 0

    def _send_artdmx(self):
        # Build a minimal ArtDMX packet
        header = b'Art-Net\x00'
        opcode = (0x5000).to_bytes(2, 'little')  # OpCode ArtDMX
        prot = (14).to_bytes(2, 'little')
        seq = (0).to_bytes(1, 'little')
        phys = (0).to_bytes(1, 'little')
        uni = int(self.universe).to_bytes(2, 'little')
        length = (len(self.channels)).to_bytes(2, 'big')
        data = bytes(self.channels)
        packet = header + opcode + prot + seq + phys + uni + length + data
        try:
            self.sock.sendto(packet, (self.host, self.port))
            self.last_packet_time = time.time()
        except Exception:
            pass
