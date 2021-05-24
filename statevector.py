from datetime import datetime

# Method to convert StateVector to dict

def sv_to_dict(s):

    if not (s.time_position): return None

    d = {
        'icao24': s.icao24,
        'callsign': s.callsign,
        'origin_country': s.origin_country,
        'time_position': datetime.utcfromtimestamp(s.time_position).isoformat(),
        'last_contact': s.last_contact,
        'location': [ s.longitude, s.latitude],
        'geo_altitude': s.geo_altitude,
        'on_ground': s.on_ground,
        'velocity': s.velocity,
        'heading': s.heading,
        'vertical_rate': s.vertical_rate,
        'sensors': s.sensors,
        'baro_altitude': s.baro_altitude,
        'squawk': s.squawk,
        'spi': s.spi,
        'position_source': s.position_source
    }

    return d
