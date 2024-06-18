from abc import abstractmethod
from math import exp, log
import Section


class ConcreteSection(Section):

    DEFAULT_fck = 25
    DEFAULT_fyk = 500
    DEFAULT_fpk = 1860
    DEFAULT_Es = 21E4
    DEFAULT_Ep = 195E3
    DEFAULT_s = 0.2
    DEFAULT_t = 5
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
        self.s = kwargs.get('s')
        self.prestress_time = kwargs.get('prestress_time')

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
        self.dc = 0

        #HOMOGENIZED SECTIONS
        self.hmgSect = self.hmgSection()

        #LOADS
        self.N = kwargs.get('N')
        self.M = kwargs.get('M')

        #NEUTRAL FIBRE
        self.h1 = self.h1()
        self.h2 = self.h - self.h1

#------------SETTERS-----------------

    def set_gc(self, gc):
        self.gc = gc

    def set_gs(self, gs):
        self.gs = gs

    def set_gp(self, gp):
        self.gp = gp

    def set_As1(self, As1):
        self.As1 = As1

    def set_As2(self, As2):
        self.As2 = As2

    def set_Ap(self, Ap):
        self.Ap = Ap

    def set_ds1(self, ds1):
        self.ds1 = ds1

    def set_ds2(self, ds2):
        self.ds2 = ds2

    def set_dp(self, dp):
        self.dp = dp

    def set_N(self, N):
        self.N = N

    def set_M(self, M):
        self.M = M

    @abstractmethod
    def hmgSection(self):
        """dictionary {area, first moment of inertia, second moment of inertia}
        from the top fibre"""
        pass

    @abstractmethod
    def magnelTensionLimit(self, Mi: float, Mf: float):
        """
        checks if a section meets tension limits according to magnel diagrams.
        this is a short-term check.
        :param Mi: mm*N initial moment (at the instant of prestress)
        :param Mf: mm*N complete moment under service loads
        """
        pass


#------------CONCRETE METHODS---------------------
    def Bcc(self):
        """time dependent scalar that reduces concrete strength for a time t
        between 3 and 28 days
        """
        return exp(self.s * (1 - pow(28 / self.prestress_time, 0.5)))

    def fcm(self):
        """ average concrete compression strength"""
        return self.fck + 8

    def fcmt(self):
        """time dependent average concrete compression strength"""
        return self.Bcc() * self.fcm()

    def fctm(self):
        """average concrete tensile strength"""
        if self.fck <= 50:
            return 0.30 * pow(self.fck, 2 / 3)
        else:
            return 2.12 * log(1 + self.fcm() * 0.1)

    def fctmt(self):
        """average time dependent concrete tensile strength"""
        return self.Bcc() * self.fctm()

    def fckt(self):
        """time dependent concrete characteristic compression strength. t in days
        """
        return self.Bcc() * self.fck

    def Ecmt(self):
        """time dependent secant concrete elastic modulus"""
        return pow(self.fcmt() / self.fcm(), 0.3) * self.Ecm

    def e(self):
        """distance from the centroid to the pre-tensioned steel centroid"""
        return self.dp - self.ycentroid()

#-----------STRAIN SECTION METHODS ------------------
    def h1(self): #test
        """signed distance of neutral fibre from the top fibre"""
        num = self.M * self.hmgSect['Q'] - self.N * self.hmgSect['I']
        dem = self.M * self.hmgSect['A'] - self.N * self.hmgSect['Q']
        return num / dem

    def k(self): # test
        """signed curvature of the section"""
        num = self.N * self.hmgSect['Q'] - self.M * self.hmgSect['A']
        dem = self.Ecm * (pow(self.hmgSect['Q'], 2) - self.hmgSect['A'] * self.hmgSect['I'])
        return num / dem

    def eps_0(self): # test
        """signed strain of top fibre"""
        num = self.M * self.hmgSect['Q'] - self.hmgSect['I'] * self.N
        dem = self.Ecm * (pow(self.hmgSect['Q'], 2) - self.hmgSect['A'] * self.hmgSect['I'])
        return num / dem

#----------MODULOS RESITENTES------------
    def Wx01(self) -> float(): #text
        """elastic section modulus considering the inertia from the centroid to the
        top fibre and the distance from the centroid to the top fibre"""
        return self.Ix0() / self.ycentroid()

    def Wx02(self) ->float(): #test
        """elastic section modulus considering the inertia from the centroid to the
        top fibre and the distance from the centroid to the top fibre"""
        return self.Ix0() / (self.h - self.ycentroid())