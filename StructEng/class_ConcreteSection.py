from abc import abstractmethod
from math import exp, log
from StructEng.class_Section import Section


class ConcreteSection(Section):
    kwDefaults = {
        'fck' : 25,
        'fyk' : 500,
        'fpk' : 1860,
        'Es' : 21E4,
        'Ep' : 195E3,
        's' : 0.2,
        'prestress_time' : 5,
        'gc' : 1.5,
        'gs' : 1.15,
        'gp' : 1.15,
        'As1' : 0,
        'As2' : 0,
        'Ap' : 0,
        'b' : 500,
        'h' : 1000,
        'ds1' : 50,
        'ds2' : 950,
        'dp' : 850,
        'N' : 0,
        'M' : 0
    }

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
        self.epsilon_c0 = self.eps_0() # TOP FIBRE'S STRAIN

    def __str__(self):
        str = f"""
        fck: concrete characteristic strength......................................{self.fck} Mpa
        fck_t: concrete characteristic compression strength. t in days.............{self.fck_t()} Mpa
        fcm: average concrete compression strength.................................{self.fcm()} Mpa
        fcm_t: time-dependent average concrete compression strength................{self.fcm_t()} Mpa
        fctm: average concrete tensile strength....................................{self.fctm()} Mpa
        fctm_t: average time-dependent concrete tensile strength...................{self.fctm_t()} Mpa
        fyk: passive steel characteristic strength.................................{self.fyk} Mpa
        fpk: pre-stress steel characteristic strength..............................{self.fpk} Mpa
        Ecm: concrete average Young's modulus......................................{self.Ecm} Mpa
        Ecm_t: time-dependent secant concrete elastic modulus......................{self.Ecm_t()} Mpa
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
        homogenized_section:...........{self.hmgSect} mm2, mm3, mm4
        N: normal force applied in the section's centroid..........................{self.N} N
        M: total moment applied to the section.....................................{self.M} mm*N
        k: signed curvature of the section.........................................{self.crv} mm-1
        eps_0: signed strain of top fibre..........................................{self.epsilon_c0} -admin-
        """
        return str

    def __upd_dep_attrs(self):
        """ updates all dependent attributes"""

        self.Ecm = 22 * pow(self.fcm() * 0.1, 0.3) * 1E3
        self.ns = self.Es / self.Ecm
        self.np = self.Ep / self.Ecm
        self.hmgSect = self.hmgSection()
        self.crv = self.k() # CURVATURE
        self.epsilon_c0 = self.eps_0() # TOP FIBRE'S STRAIN

    def set(self, kwargs):
        """sets attributes to the values passed in a dict"""

        if kwargs != None:
            for key in kwargs:
                self.__dict__[key] = kwargs[key]

        else:
            for key in self.kwDefaults:
                self.__dict__[key] = self.kwDefaults[key]

        self.__upd_dep_attrs()

#-------------ABSTRACT METHODS--------------
    @abstractmethod
    def hmgSection(self):
        """dictionary {area, first moment of inertia, second moment of inertia}
        from the top fibre"""
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
        """time-dependent concrete characteristic compression strength. t in days"""
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

    def eps(self, y):
        """strain in any point y to section's height"""
        return self.epsilon_c0 + self.crv * y

    def stress(self, y):
        """stress in any point y to section's height"""
        return self.eps(y) * self.Ecm

    def magnelTensionLimit(self, Mi: float, Mf: float):
        """checks if a section meets tension limits according to spanish
        structural code. This is a short-term check. No cracking is taken into account.
        :param Mi: mm*N initial moment (at the instant of prestress)
        :param Mf: mm*N complete moment under service loads
        """
        # initial load case stress
        self.M = Mi
        init_top_stress = self.stress(0)
        init_bottom_stress = self.stress(self.h)

        # final load case stress
        self.M = Mf
        final_top_stress = self.stress(0)
        final_bottom_stress = self.stress(self.h)

        init_top_check = -0.45 * self.fck_t() < init_top_stress < self.fctm_t()
        init_bottom_check = -0.45 * self.fck_t() < init_bottom_stress < self.fctm_t()
        final_top_check = -0.45 * self.fck() < final_top_stress < self.fctm()
        final_bottpom_check = -0.45 * self.fck() < final_bottom_stress < self.fctm()

        return init_top_check and init_bottom_check and final_top_check and final_bottpom_check

#----------SECTION MODULUS------------
    def Wx01(self) -> float(): #text
        """elastic section modulus considering the inertia from the centroid to the
        top fibre and the distance from the centroid to the top fibre"""
        return self.Ix0() / self.ycentroid()

    def Wx02(self) ->float(): #test
        """elastic section modulus considering the inertia from the centroid to the
        top fibre and the distance from the centroid to the top fibre"""
        return self.Ix0() / (self.h - self.ycentroid())
