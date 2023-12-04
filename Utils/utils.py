import math


def ra_dec_to_alt_az(ra, dec, lat, long, jd):
    # All angles in radians
    gmst = greenwich_mean_sidereal_time(jd)
    local_sidereal_time = (gmst + long) % (2 * math.pi)

    h = local_sidereal_time - ra
    if h < 0:
        h += 2 * math.pi
    if h > math.pi:
        h = h - 2 * math.pi

    az = math.atan2(math.sin(h), math.cos(h)*math.sin(lat) - math.tan(dec)*math.cos(lat))
    a = math.asin(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(h))
    az -= math.pi

    if az < 0:
        az += 2 * math.pi

    return az, a, local_sidereal_time, h


def greenwich_mean_sidereal_time(jd):
    t = (jd - 2451545.0) / 36525.0
    gmst = earth_rotation_angle(jd) +\
           (0.014506 + 4612.156534*t + 1.3915817*t*t - 0.00000044 *t*t*t - 0.000029956*t*t*t*t - 0.0000000368*t*t*t*t*t)
    gmst /= 60
    gmst /= 60
    gmst *= math.pi / 180.0
    gmst %= 2 * math.pi

    if gmst < 0:
        gmst += 2 * math.pi

    return gmst


def earth_rotation_angle(jd):
    t = jd - 2451545.0
    f = jd % 1.0

    theta = 2 * math.pi * (f + 0.7790572732640 + 0.00273781191135448 * t)
    theta %= 2 * math.pi
    if theta < 0:
        theta += 2 * math.pi

    return theta
