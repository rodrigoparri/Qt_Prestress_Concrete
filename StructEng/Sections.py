from abc import ABC, abstractmethod
"""
---------UNITS--------------------
length: mm
force: N
stress: N/mm
"""

class Section(ABC):
    @abstractmethod
    def bruteArea(self):
        """ Cross-section area calculation"""
        pass

    @abstractmethod
    def bruteIx(self):
        """Moment of inertia from x-axis through the section's centroid"""
        pass



class ConcreteSection(Section):

    DEFAULT_fck = 25
    DEFAULT_fyk = 500
    DEFAULT_fpk = 1860
    DEFAULT_Ecm = 31
    DEFAULT_Es = 21E4
    DEFAULT_Ep = 195E3
    DEFAULT_gc = 1.5
    DEFAULT_gs = 1.15
    DEFAULT_gp = 1.15
    DEFAULT_As1 = 0
    DEFAULT_As2 = 0
    DEFAULT_Ap = 0
    DEFAULT_b = 500
    DEFAULT_h = 1000
    DEFAULT_ds1 = 50
    DEFAULT_ds2 = DEFAULT_h - DEFAULT_ds1
    DEFAULT_dp = DEFAULT_h - 150

    def __init__(self, **kwargs):
        #MATERIAL
        self.fck = kwargs.get('fck', ConcreteSection.DEFAULT_fck)
        self.fyk = kwargs.get('fyk', ConcreteSection.DEFAULT_fyk)
        self.fpk = kwargs.get('fpk', ConcreteSection.DEFAULT_fpk)
        self.Ecm = kwargs.get('Ecm', ConcreteSection.DEFAULT_Ecm)
        self.Es = kwargs.get('Es', ConcreteSection.DEFAULT_Es) #210,000Mpa
        self.Ep = kwargs.get('Ep', ConcreteSection.DEFAULT_Ep) #195,000Mpa
        self.ns = self.Ecm / self.Es
        self.np = self.Ecm / self.Ep

        #MATERIAL COEFFICIENTS
        self.gc = kwargs.get('gc', ConcreteSection.DEFAULT_gc)
        self.gs = kwargs.get('gs', ConcreteSection.DEFAULT_gs)
        self.gp = kwargs.get('gp', ConcreteSection.DEFAULT_gp)

        #REINFORCEMENT AREA
        self.As1 = kwargs.get('As1', ConcreteSection.DEFAULT_As1)
        self.As2 = kwargs.get('As2', ConcreteSection.DEFAULT_As2)
        self.Ap = kwargs.get('Ap', ConcreteSection.DEFAULT_Ap)

        #DIMENSIONS
        self.b = kwargs.get('b', ConcreteSection.DEFAULT_b)
        self.h = kwargs.get('h', ConcreteSection.DEFAULT_h)

        #REINFORCEMENT POSITIONS
        self.ds1 = kwargs.get('ds1', ConcreteSection.DEFAULT_ds1)
        self.ds2 = kwargs.get('ds2', ConcreteSection.DEFAULT_ds2)
        self.dp = kwargs.get('dp', ConcreteSection.DEFAULT_dp)
        self.dc = self.ycentroid()

    @abstractmethod
    def ycentroid(self):
        pass
    @abstractmethod
    def hmgSection(self):
        pass


class RectConcSect(ConcreteSection):
    """b: width
        h: height
        fck: concrete characteristic strength
        fyk: steel characteristic strength
        fpk: pre-tensioned steel characteristic strength
        Ecm: secant elastic modulus
        Es: reinforcement steel elastic modulus
        Ep: pre-tensioned steel elastic modulus

        As1: top steel reinforcement area
        As2: bottom steel reinforcement area
        Ap: pre-tensioned steel area
        ds1: distance from top fibre to As1 centroid
        ds2: distance from top fibre to As2 centroid
        """
    def __init__(self, **kwargs):
        super().__init__(fck=kwargs['fck'], As1=kwargs['As1'], As2=kwargs['As2'],
            fyk=kwargs['fyk'], Ap=kwargs['Ap'], fpk=kwargs['fpk'], ds1=kwargs['ds1'],
            ds2=kwargs['ds2'], b=kwargs['b'], h=kwargs['h'])

    def bruteArea(self):
        return self.b * self.h

    def bruteIx(self):
        return pow(self.h, 3) * self.b / 12

    def hmgSection(self):
        hmg = dict()
        hmgA = self.bruteArea()
        hmgAc1 = self.As1 * (self.ns - 1)
        hmgAc2 = self.As2 * (self.ns - 1)
        hmgAcp = self.Ap * (self.np - 1)
        hmgArea = hmgA + hmgAc1 + hmgAc2 + hmgAcp

        hmgQA = hmgA * self.dc
        hmgQc1 = hmgAc1 * self.ds1
        hmgQc2 = hmgAc2 * self.ds2
        hmgQcp = hmgAcp * self.dp
        hmgQ = hmgQA + hmgQc1 + hmgQc2 + hmgQcp

        hmgI = self.bruteIx
        hmg['hmgArea'] = hmgArea
        hmg['hmgQ'] = hmgQ
        hmg['hmgI'] = hmgI
        return hmg

