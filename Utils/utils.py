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


def get_pole(alt, az):
    return alt * -1, (180 + az) % 360


def alt_az_to_unit_vector(alt, az):
    # Angles in degrees
    az_corrected = az * math.pi / 180.0
    alt_corrected = ((alt * -1) + 90) * math.pi / 180.0
    x = math.sin(alt_corrected) * math.cos(az_corrected)
    y = math.sin(alt_corrected) * math.sin(az_corrected)
    z = math.cos(alt_corrected)
    return x, y, z


def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def zenith_angle_to_pole(pole_alt, pole_az, alt, az):
    a = alt_az_to_unit_vector(pole_alt, pole_az)
    b = alt_az_to_unit_vector(alt, az)
    return math.acos(dot_product(a, b))


def azimuth_angle_to_pole(pole_alt, pole_az, alt, az):
    az1 = pole_az * math.pi/180
    az2 = az * math.pi/180

    alt1 = pole_alt * math.pi/180
    alt2 = alt * math.pi/180

    y = math.sin(az2 - az1) * math.cos(alt2)
    x = math.cos(alt1) * math.sin(alt2) - math.sin(alt1) * math.cos(alt2) * math.cos(az2 - az1)
    return math.atan2(y, x)


def spherical_to_stereographic(phi, theta):
    return math.sin(phi)/(1 - math.cos(phi)), theta

def polar_to_cartesian(r, theta):
    return r * math.cos(theta), r*math.sin(theta)
