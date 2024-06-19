from abc import abstractmethod
from math import exp, log
from StructEng.class_Section import Section


class ConcreteSection(Section):

    DEFAULT_fck = 25
    DEFAULT_fyk = 500
    DEFAULT_fpk = 1860
    DEFAULT_Es = 21E4
    DEFAULT_Ep = 195E3
    DEFAULT_s = 0.2
    DEFAULT_prestress_time = 5
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
        self.Ecm = 22 * pow(self.fcm() * 0.1, 0.3) * 1E3
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

        #STRAIN
        self.crv = self.k() # CURVATURE
        self.eps_0 = self.eps_0() # TOP FIBRE'S STRAIN

    def __str__(self):
        str = f"""
        fck: concrete characteristic strength......................................{self.fck} Mpa
        fyk: passive steel characteristic strength.................................{self.fyk} Mpa
        fpk: pre-stress steel characteristic strength..............................{self.fpk} Mpa
        Ecm: concrete average Young's modulus......................................{self.Ecm} Mpa
        Es: passive steel Young's modulus..........................................{self.Es} Mpa
        Ep: pre-stress steel Young's modulus.......................................{self.Ep} Mpa
        ns: passive steel homogenization coefficient...............................{self.ns} -adim-
        np: pre-stress steel homogenization coefficient............................{self.np} -adim-
        s: cement type for time-dependent calculations (0.2, 0.25, 0.38)...........{self.s} -adim-
        prestress_time: days after concrete pouring when pre-stress is applied.....{self.prestress_time} days
        gc: concrete strength reduction coefficient................................{self.gc} -adim-
        gs: steel strength reduction coefficient...................................{self.gs} -adim-
        gp: pre-stress steel strength reduction coefficient........................{self.gp} -adim-
        As1: passive steel area in the compression part of the beam................{self.As1} mm2
        As2: passive steel area in the tension part of the beam....................{self.As2} mm2
        Ap: pre-stress steel area..................................................{self.Ap} mm2
        b: width of the smallest bounding box that contains the section............{self.b} mm
        h: height of the smallest bounding box that contains the section...........{self.h} mm
        ds1: distance from the top fibre to the centroid of As1....................{self.ds1} mm
        ds2: distance from the top fibre to the centroid of As1....................{self.ds2} mm
        dp: distance from the top fibre to the centroid of Ap......................{self.dp} mm
        dc: distance from the top fibre to the resultant force in the concrete.....{self.dc} mm
        homogenized_section:..............................{self.hmgSect} mm2, mm3, mm4
        N: normal force applied in the section's centroid..........................{self.N} N
        M: total moment applied to the section.....................................{self.M} mm*N
        k: signed curvature of the section.........................................{self.crv} mm-1
        eps_0: signed strain of top fibre..........................................{self.eps_0} -admin-
        """
        return str

    def set_DEFAULT(self):
        """set all class attributes to defaults"""

        self.fck = self.DEFAULT_fck
        self.fyk = self.DEFAULT_fyk
        self.fpk = self.DEFAULT_fpk
        self.Ecm = 22 * pow(self.fcm() * 0.1, 0.3) * 1E3
        self.Es = self.DEFAULT_Es
        self.Ep = self.DEFAULT_Ep
        self.ns = self.Es / self.Ecm
        self.np = self.Ep / self.Ecm
        self.s = self.DEFAULT_s
        self.prestress_time = self.DEFAULT_prestress_time

        # MATERIAL COEFFICIENTS
        self.gc = self.DEFAULT_gc
        self.gs = self.DEFAULT_gs
        self.gp = self.DEFAULT_gp

        # REINFORCEMENT AREA
        self.As1 = self.DEFAULT_As1
        self.As2 = self.DEFAULT_As2
        self.Ap = self.DEFAULT_Ap

        # DIMENSIONS
        self.b = self.DEFAULT_b
        self.h = self.DEFAULT_h

        # REINFORCEMENT POSITIONS
        self.ds1 = self.DEFAULT_ds1
        self.ds2 = self.DEFAULT_ds2
        self.dp = self.DEFAULT_dp
        self.dc = 0

        # HOMOGENIZED SECTIONS
        self.hmgSect = self.hmgSection()

        # LOADS
        self.N = self.DEFAULT_N
        self.M = self.DEFAULT_M

        # STRAIN
        self.crv = self.k()  # CURVATURE
        self.eps_0 = self.eps_0()  # TOP FIBRE'S STRAIN

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

    def fcm_t(self):
        """time-dependent average concrete compression strength"""
        return self.Bcc() * self.fcm()

    def fctm(self):
        """average concrete tensile strength"""
        if self.fck <= 50:
            return 0.30 * pow(self.fck, 2 / 3)
        else:
            return 2.12 * log(1 + self.fcm() * 0.1)

    def fctm_t(self):
        """average time-dependent concrete tensile strength"""
        return self.Bcc() * self.fctm()

    def fck_t(self):
        """time-dependent concrete characteristic compression strength. t in days
        """
        return self.Bcc() * self.fck

    def Ecm_t(self):
        """time-dependent secant concrete elastic modulus"""
        return pow(self.fcm_t() / self.fcm(), 0.3) * self.Ecm

    def e(self):
        """distance from the centroid to the pre-tensioned steel centroid"""
        return self.dp - self.ycentroid()

#-----------STRAIN SECTION METHODS ------------------

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