from abc import ABC, abstractmethod

"""
---------UNITS--------------------
length: mm
force: N
stress: N/mm
---------ORIGING-----------------
section origin is defined in the top right corner
"""


class Section(ABC):
    @abstractmethod
    def bruteArea(self):
        """ Cross-section area calculation"""
        pass

    @abstractmethod
    def xcentroid(self):
        """x position of the section's centroid from the left side"""
        pass

    @abstractmethod
    def ycentroid(self):
        """y position of the section's centroid from the top fibre"""
        pass

    @abstractmethod
    def Ix0(self):
        """Moment of inertia from the x-axis through the origin"""
        pass

    @abstractmethod
    def Ix(self, d: float):
        """Moment of inertia af the original section (considered concrete-massive)
        from an arbitrary axis parallel to the x-axis
        :param d: mm distance from x-axis through the section's centroid"""
        pass

    @staticmethod
    def Q(A, d):
        """Stactic area moment from an arbitrary axis
        :param A: Area to calculate the moment of
        :param d: Distance measured orthogonally to the reference axis
        """
        return A * d


if __name__ == "__main__":
    pass

