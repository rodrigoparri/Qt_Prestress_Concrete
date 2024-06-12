from abc import ABC, abstractmethod
"""
---------UNITS--------------------
length: mm
force: N
stress: N/mm
---------ORIGING-----------------
beam origin is defined in the top right corner
"""


class Section(ABC):
    @abstractmethod
    def bruteArea(self):
        """ Cross-section area calculation"""
        pass

    @abstractmethod
    def xcentroid(self):
        """x position of the section's centroid"""
        pass

    @abstractmethod
    def ycentroid(self):
        """y position of the section's centroid"""
        pass

    @abstractmethod
    def bruteIx(self):
        """Moment of inertia from x-axis through the section's centroid"""
        pass

    @abstractmethod
    def steinerIx(self, d):
        """Moment of inertia af the original section (considered concrete-massive)
        from an arbitrary axis parallel to the x-axis
        d: distance from x-axis through the section's centroid"""
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
        self.fck = kwargs.get('fck')
        self.fyk = kwargs.get('fyk')
        self.fpk = kwargs.get('fpk')
        self.Ecm = kwargs.get('Ecm')
        self.Es = kwargs.get('Es') #210,000Mpa
        self.Ep = kwargs.get('Ep') #195,000Mpa
        self.ns = self.Ecm / self.Es
        self.np = self.Ecm / self.Ep

        #MATERIAL COEFFICIENTS
        self.gc = kwargs.get('gc')
        self.gs = kwargs.get('gs')
        self.gp = kwargs.get('gp')

        #REINFORCEMENT AREA
        self.As1 = kwargs.get('As1')
        self.As2 = kwargs.get('As2')
        self.Ap = kwargs.get('Ap')

        #DIMENSIONS
        self.b = kwargs.get('b')
        self.h = kwargs.get('h')

        #REINFORCEMENT POSITIONS
        self.ds1 = kwargs.get('ds1')
        self.ds2 = kwargs.get('ds2')
        self.dp = kwargs.get('dp')
        self.dc = self.ycentroid()

        #

    @abstractmethod
    def hmgSection(self):
        """dictionary {area, first moment of inertia, second moment of inertia}
        from the top fibre"""
        pass

    @abstractmethod
    def magnelTensionLimit(self, **kwargs):
        """
        checks if a section meets tension limits according to magnel diagrams.
        this is a short-term check.
        :param P: effective pretension force (after short-term losses)
        """
        pass

class RectConcSect(ConcreteSection):
    """
        fck: concrete characteristic strength
        fyk: steel characteristic strength
        fpk: pre-tensioned steel characteristic strength
        Ecm: secant elastic modulus
        Es: reinforcement steel elastic modulus
        Ep: pre-tensioned steel elastic modulus
        gc: concrete strength reduction coefficient
        gs: passive steel strength reduction coefficient
        gp: active steel strength reduction coefficient
        As1: top steel reinforcement area
        As2: bottom steel reinforcement area
        Ap: pre-tensioned steel area
        b: width
        h: height
        ds1: distance from top fibre to As1 centroid
        ds2: distance from top fibre to As2 centroid
        dp: distance from top fibre to Ap centroid
    """
    def __init__(self, **kwargs):
        super().__init__(
            fck=kwargs.get('fck', ConcreteSection.DEFAULT_fck),
            fyk=kwargs.get('fyk', ConcreteSection.DEFAULT_fyk),
            fpk=kwargs.get('fpk', ConcreteSection.DEFAULT_fpk),
            Ecm=kwargs.get('Ecm', ConcreteSection.DEFAULT_Ecm),
            Es=kwargs.get('Es', ConcreteSection.DEFAULT_Es),
            Ep=kwargs.get('Ep', ConcreteSection.DEFAULT_Ep),
            gc=kwargs.get('gc', ConcreteSection.DEFAULT_gc),
            gs=kwargs.get('gs', ConcreteSection.DEFAULT_gs),
            gp=kwargs.get('gp', ConcreteSection.DEFAULT_gp),
            As1=kwargs.get('As1', ConcreteSection.DEFAULT_As1),
            As2=kwargs.get('As2', ConcreteSection.DEFAULT_As2),
            Ap=kwargs.get('Ap', ConcreteSection.DEFAULT_Ap),
            b=kwargs.get('b', ConcreteSection.DEFAULT_b),
            h=kwargs.get('h', ConcreteSection.DEFAULT_h),
            ds1=kwargs.get('ds1', ConcreteSection.DEFAULT_ds1),
            ds2=kwargs.get('ds2', ConcreteSection.DEFAULT_ds2),
            dp=kwargs.get('dp', ConcreteSection.DEFAULT_dp)
        )

    def bruteArea(self):
        return self.b * self.h

    def xcentroid(self):
        return self.b / 2

    def ycentroid(self):
        return self.h / 2

    def bruteIx(self):
        return pow(self.h, 3) * self.b / 12

    def steinerIx(self, d):
        return self.bruteIx() + self.bruteArea() * pow(d, 2)

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

        hmgIA = self.steinerIx(self.h/2)
        hmgIc1 = hmgQc1 * self.ds1
        hmgIc2 = hmgQc2 * self.ds2
        hmgIcp = hmgQcp * self.dp
        hmgI = hmgIA + hmgIc1 + hmgIc2 + hmgIcp
        hmg['hmgArea'] = hmgArea
        hmg['hmgQ'] = hmgQ
        hmg['hmgI'] = hmgI
        return hmg

    def magnelTensionLimit(self, **kwargs):


if __name__ == "__main__":
    defaultConcBeam = RectConcSect()
    print(defaultConcBeam.hmgSection())

