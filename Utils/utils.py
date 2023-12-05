import math


def ra_dec_to_alt_az(ra_deg, dec_deg, lat_deg, long_deg, t):
    ra = ra_deg * math.pi/180
    dec = dec_deg * math.pi/180
    lat = ((lat_deg * -1) + 90.0) * math.pi/180
    long = long_deg * math.pi/180

    # All angles in radians
    gmst = t.gmst
    local_sidereal_time = js_modulo(gmst + long, 2 * math.pi)

    h = local_sidereal_time - ra
    if h < 0:
        h += 2 * math.pi
    if h > math.pi:
        h = h - 2 * math.pi

    az = (math.atan2(math.sin(h), math.cos(h)*math.sin(lat) - math.tan(dec)*math.cos(lat)))
    a = (math.asin(math.sin(lat)*math.sin(dec) + math.cos(lat)*math.cos(dec)*math.cos(h)))
    az -= math.pi

    if az < 0:
        az += 2 * math.pi

    az *= 180/math.pi
    a *= 180/math.pi

    return az, a, local_sidereal_time, h


def js_modulo(x, m):
    return (x % m) * x/abs(x)