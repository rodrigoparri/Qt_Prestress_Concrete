from abc import ABC, abstractmethod
from math import exp, log
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

    def Wx(self, h: float):
        """elastic section modulus considering the inertia from the centroid to the
        top fibre.
        :param h: mm distance from centroid to the top or bottom fibre
        """
        return self.Ix0() / h


class ConcreteSection(Section):

    DEFAULT_fck = 25
    DEFAULT_fyk = 500
    DEFAULT_fpk = 1860
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
    DEFAULT_N = 0
    DEFAULT_M = 0

    def __init__(self, **kwargs):
        #MATERIAL
        self.fck = kwargs.get('fck')
        self.fyk = kwargs.get('fyk')
        self.fpk = kwargs.get('fpk')
        self.Ecm = 22 * pow(self.fcm() * 0.1, 0.3)
        self.Es = kwargs.get('Es') #210,000Mpa
        self.Ep = kwargs.get('Ep') #195,000Mpa
        self.ns = self.Es / self.Ecm
        self.np = self.Ep / self.Ecm

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
        self.h1 = 0
        self.h2 = 0

        #REINFORCEMENT POSITIONS
        self.ds1 = kwargs.get('ds1')
        self.ds2 = kwargs.get('ds2')
        self.dp = kwargs.get('dp')
        self.dc = self.ycentroid()

        #LOADS
        self.N = kwargs.get('N')
        self.M = kwargs.get('M')

    @abstractmethod
    def hmgSection(self):
        """dictionary {area, first moment of inertia, second moment of inertia}
        from the top fibre"""
        pass

    @abstractmethod
    def magnelTensionLimit(self, Mi: float, Mf: float, t: float, s: float):
        """
        checks if a section meets tension limits according to magnel diagrams.
        this is a short-term check.
        :param Mi: mm*N initial moment (at the instant of prestress)
        :param Mf: mm*N complete moment under service loads
        :param t: days time of prestress from concrete pouring
        :param s: non-dimensional. cement type
        """
        pass

    @staticmethod
    def Bcc(t: float, s: float):
        """time dependent scalar that reduces concrete strength for a time t
        between 3 and 28 days
        :param t: time 0-28 days
        :param s: cement type 0.20, 0.25, 0.38
        """
        return exp(s * (1 - pow(28 / t, 0.5)))

    def fcm(self):
        """ average concrete compression strength"""
        return self.fck + 8

    def fcmt(self, t: float, s: float):
        """time dependent average concrete compression strength"""
        return ConcreteSection.Bcc(t, s) * self.fcm()

    def fctm(self):
        """average concrete tensile strength"""
        if self.fck <= 50:
            return 0.30 * pow(self.fck, 2 / 3)
        else:
            return 2.12 * log(1 + self.fcm() * 0.1)

    def fctmt(self, t: float, s: float):
        """average time dependent concrete tensile strength"""
        return ConcreteSection.Bcc(t, s) * self.fctm()
    def fckt(self, t: float, s: float):
        """time dependent concrete characteristic compression strength. t in days
        """
        return ConcreteSection.Bcc(t, s) * self.fck

    def Ecmt(self, t: float, s: float):
        """time dependent secant concrete elastic modulus"""
        return pow(self.fcmt(t, s) / self.fcm(), 0.3) * self.Ecm

    def e(self):
        """distance from the centroid to the pre-tensioned steel centroid"""
        return self.dp - self.ycentroid()


class RectConcSect(ConcreteSection):
    """
        :param fck: concrete characteristic strength
        :param fyk: steel characteristic strength
        :param fpk: pre-tensioned steel characteristic strength
        :param Ecm: secant elastic modulus
        :param Es: reinforcement steel elastic modulus
        :param Ep: pre-tensioned steel elastic modulus
        :param gc: concrete strength reduction coefficient
        :param gs: passive steel strength reduction coefficient
        :param gp: active steel strength reduction coefficient
        :param As1: top steel reinforcement area
        :param As2: bottom steel reinforcement area
        :param Ap: pre-tensioned steel area
        :param b: width
        :param h: height
        :param ds1: distance from top fibre to As1 centroid
        :param ds2: distance from top fibre to As2 centroid
        :param dp: distance from top fibre to Ap centroid
        :param N: axial load
        :param M: torque
    """
    def __init__(self, **kwargs):

        super().__init__(
            fck=kwargs.get('fck', ConcreteSection.DEFAULT_fck),
            fyk=kwargs.get('fyk', ConcreteSection.DEFAULT_fyk),
            fpk=kwargs.get('fpk', ConcreteSection.DEFAULT_fpk),
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
            dp=kwargs.get('dp', ConcreteSection.DEFAULT_dp),
            N=kwargs.get('N', ConcreteSection.DEFAULT_N),
            M=kwargs.get('M', ConcreteSection.DEFAULT_M)

        )
        self.h1 = self.h / 2
        self.h2 = self.h1
        pass

    def bruteArea(self) -> float():
        return self.b * self.h

    def xcentroid(self):
        return self.b / 2

    def ycentroid(self):
        return self.h / 2

    def Ix0(self):
        return pow(self.h, 3) * self.b / 12

    def Ix(self, d):
        return self.Ix0() + self.bruteArea() * pow(d, 2)

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

        hmgIA = self.Ix(self.h1)
        hmgIc1 = hmgQc1 * self.ds1
        hmgIc2 = hmgQc2 * self.ds2
        hmgIcp = hmgQcp * self.dp
        hmgI = hmgIA + hmgIc1 + hmgIc2 + hmgIcp
        hmg['hmgArea'] = hmgArea
        hmg['hmgQ'] = hmgQ
        hmg['hmgI'] = hmgI
        return hmg

    def magnelTensionLimit(self, Mi: float, Mf: float, t: float, s: float) -> bool():
        Ac = self.bruteArea()
        Wx1 = self.Wx(self.h1) # top fibre
        Wx2 = self.Wx(self.h2)
        Pe = self.N * self.e()

        #Magnel inequations
        emptyTopFibre = -self.N / Ac + (Pe - Mi) / Wx1 <= self.fctmt(t, s)
        emptyBottomFibre = -self.N / Ac + (-Pe + Mi) / Wx2 >= -0.45 * self.fckt(t, s)
        loadedTopFibre = -self.N / Ac + (Pe - Mf) / Wx1 >= -0.45 * self.fck
        loadedBottomFibre = -self.N / Ac + (-Pe + Mf) / Wx2 <= self.fctm()

        return emptyTopFibre and emptyBottomFibre and loadedTopFibre and loadedBottomFibre


class TConcSect(ConcreteSection):
    DEFAULT_t1 = 200 #FLANGE THICKNESS
    DEFAULT_t = 250 #WEB THICKNESS

    def __init__(self, **kwargs):
        self.t1 = kwargs.get('t1', TConcSect.DEFAULT_t1)
        self.t = kwargs.get('t', TConcSect.DEFAULT_t)
        super().__init__(
            fck=kwargs.get('fck', ConcreteSection.DEFAULT_fck),
            fyk=kwargs.get('fyk', ConcreteSection.DEFAULT_fyk),
            fpk=kwargs.get('fpk', ConcreteSection.DEFAULT_fpk),
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
            dp=kwargs.get('dp', ConcreteSection.DEFAULT_dp),
            N=kwargs.get('N', ConcreteSection.DEFAULT_N),
            M=kwargs.get('M', ConcreteSection.DEFAULT_M)
        )

    def bruteArea(self):
        return (self.b - self.t) * self.t1 + self.h * self.t

    def xcentroid(self):
        return self.b / 2

    def ycentroid(self):
        Q1 = (self.b - self.t) * pow(self.t1, 2) / 2
        Q2 = self.t * pow(self.h, 2) / 2
        return (Q1 + Q2) / self.bruteArea()

    def Ix0(self):
        y = self.ycentroid()
        flangeHeight = self.h - self.t1
        # flange inertia from flange centroid
        Ifx0 = self.b * pow(self.t1, 3) / 12
        # steiner term for flange inertia
        Ifst = self.b * self.t1 * pow(y - self.t1 / 2, 2)
        # web inertia from web centroid
        Iwxo = self.t * pow(flangeHeight, 3) / 12
        # steiner term form web inertia
        IWst = self.t * flangeHeight * pow(self.h - y - flangeHeight / 2, 2)

        return Ifx0 + Ifst + Iwxo + IWst

    def Ix(self, d: float):
        pass

    def hmgSection(self):
        pass

    def magnelTensionLimit(self, Mi: float, Mf: float, t: float, s: float):
        pass


if __name__ == "__main__":
   # defaultRectConcBeam = RectConcSect()
   # print(defaultRectConcBeam.hmgSection())
    defaultTConcBeam = TConcSect(b=750)
    print(defaultTConcBeam.bruteArea())
    print(defaultTConcBeam.ycentroid())
    print(defaultTConcBeam.Ix0())
