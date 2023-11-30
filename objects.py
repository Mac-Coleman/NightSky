# This Python file uses the following encoding: utf-8

from abc import ABC, abstractmethod
from skyfield.positionlib import position_of_radec

class Object(ABC):
    @abstractmethod
    def toWidget(self):
        pass

class MessierObject(Object):
    def __init__(self, m: str, alt_name: str, t: str, mag: float, ra_h: float, dec: float, cons: str, width: float, height: float, dist_ly: float):
        self.m = m
        self.alt_name = alt_name
        self.type = t
        self.magnitude = mag
        self.position = position_of_radec(ra_h * 24.0/360.0, dec, dist_ly * 63241.14275736)
        self.constellation = cons
        self.width = width
        self.height = height
        self.search_text = self.alt_name

        self.favorited = False

    def __str__(self):
        ra, dec, dist = self.position.radec()
        return " ".join([self.m, self.alt_name, self.type, str(ra), str(dec), str(dist)])

    def __repr__(self):
        return self.__str__()

    def toWidget(self):
        from object_widgets import MessierObjectCard
        MessierObjectCard(self)

class SolarSystemObject(Object):
    def __init__(self, favorited: bool, ephemeris: str, name: str, key: str, search_text: str):
        self.favorited = favorited
        self.ephemeris = ephemeris
        self.name = name
        self.key = key
        self.search_text = search_text

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()
    
    def toWidget(self):
        from object_widgets import SolarSystemObjectCard
        SolarSystemObjectCard(self)

# if __name__ == "__main__":
#     pass
