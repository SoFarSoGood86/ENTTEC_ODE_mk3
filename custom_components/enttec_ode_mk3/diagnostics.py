# Diagnostics helper for ENTTEC integration
def get_diagnostics(client):
    return {
        'host': client.host,
        'universe': client.universe,
        'connected': client.connected,
        'last_packet': client.last_packet_time,
    }
