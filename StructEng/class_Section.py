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


    #@abstractmethod
    #def b_y(self):
    #    """function that describes the width of the section as a function of y
    #    with the origin at the top"""
    #    pass

    @abstractmethod
    def A_y(self, y):
        """area of a portion of the section defined between the top and an arbitrary
        horizontal axis at distance y from the top
        :param y: distance from the top to the axis that limits the section's portion
        """
        pass

    @abstractmethod
    def Q_y(self, y):
        """static moment of area of a portion of the section defined between the top and an arbitrary
        horizontal axis at distance y from the top
        :param y: distance from the top to the axis that limits the section's portion
        """
        pass

    @abstractmethod
    def I_y(self, y):
        """moment of inertia of area of a portion of the section defined between the top and an arbitrary
        horizontal axis at distance y from the top
        :param y: distance from the top to the axis that limits the section's portion"""

    @abstractmethod
    def ycentroid_y(self, y):
        """ y coordinate of the centroid of a portion of the section defined between the top and an arbitrary
        horizontal axis at distance y from the top
        :param y: distance from the top to the axis that limits the section's portion
        """
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
    def Ix_top(self):
        """Moment of inertia af the original section from the top fibre"""
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

