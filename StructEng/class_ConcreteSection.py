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
        self.fck = kwargs.get('fck', self.kwDefaults['fck'])
        self.s = kwargs.get('s', self.kwDefaults['s'])  # cement type
        self.prestress_time = kwargs.get('prestress_time', self.kwDefaults['prestress_time'])
        self.B_cc = self.Bcc()
        self.f_ckt = self.fck_t()  # time dependent characteristic strength
        self.f_cm = self.fcm()  # average strength
        self.f_cmt = self.fcm_t()  # time dependent average strength
        self.f_ctm = self.fctm()  # average tension strength
        self.f_ctmt = self.fctm_t()  # time dependent average tension strength
        self.fyk = kwargs.get('fyk', self.kwDefaults['fyk'])
        self.fpk = kwargs.get('fpk', self.kwDefaults['fpk'])
        self.Ecm = 22 * pow(self.fcm() * 0.1, 0.3) * 1E3  # secant Young's modulus
        self.E_cmt = self.Ecm_t()  # time dependent secant Young's modulus
        self.Es = kwargs.get('Es', self.kwDefaults['Es']) #210,000Mpa
        self.Ep = kwargs.get('Ep', self.kwDefaults['Ep']) #195,000Mpa
        self.ns = self.Es / self.Ecm
        self.n_st = self.Es / self.E_cmt
        self.np = self.Ep / self.Ecm
        self.n_pt = self.Ep / self.E_cmt

        #MATERIAL COEFFICIENTS
        self.gc = kwargs.get('gc', self.kwDefaults['gc'])
        self.gs = kwargs.get('gs', self.kwDefaults['gs'])
        self.gp = kwargs.get('gp', self.kwDefaults['gp'])

        #REINFORCEMENT AREA
        self.As1 = kwargs.get('As1', self.kwDefaults['As1'])
        self.As2 = kwargs.get('As2', self.kwDefaults['As2'])
        self.Ap = kwargs.get('Ap', self.kwDefaults['Ap'])

        #DIMENSIONS
        self.b = kwargs.get('b', self.kwDefaults['b'])
        self.h = kwargs.get('h', self.kwDefaults['h'])
        self.Ac = self.bruteArea()
        self.Q_xtop = self.Qx_top()
        self.y_cen = self.ycentroid()
        self.I_xtop = self.Ix_top()
        self.Ixo = self.Ix0()
        self.Wxo1 = self.Wx01()
        self.Wxo2 = self.Wx02()

        #REINFORCEMENT POSITIONS
        self.ds1 = kwargs.get('ds1', self.kwDefaults['ds1'])
        self.ds2 = kwargs.get('ds2', self.kwDefaults['ds2'])
        self.dp = kwargs.get('dp', self.kwDefaults['dp'])
        self.dc = 0
        self.ecc = self.e()  # active reinforcement eccentricity

        #HOMOGENIZED SECTION
        self.hmgSect = self.hmgSection()
        self.hmgSect_t = self.hmgSection_t()

        #LOADS
        self.N = kwargs.get('N', self.kwDefaults['N'])
        self.M = kwargs.get('M', self.kwDefaults['M'])

        #STRAIN
        self.crv = self.k() # CURVATURE
        self.crv_t = self.k_t()  # time-dep curvature
        self.epsilon_c0 = self.eps_0()  # TOP FIBRE'S STRAIN
        self.epsilon_c0t = self.eps_0_t()  # time-dep top fibre's strain

    def __str__(self):
        str = f"""
        ########################################################################################
        BEAM INFO
        ########################################################################################
        
        -------------------------------MATERIALS------------------------------------------------
        STRENGTH
        fck: concrete characteristic strength......................................{self.fck} Mpa
        fck_t: concrete characteristic compression strength. t in days.............{self.f_ckt} Mpa
        fcm: average concrete compression strength.................................{self.f_cm} Mpa
        fcm_t: time-dependent average concrete compression strength................{self.f_cmt} Mpa
        fctm: average concrete tensile strength....................................{self.f_ctm} Mpa
        fctm_t: average time-dependent concrete tensile strength...................{self.f_ctmt} Mpa
        Bcc: time dependent scalar for time-dependent calculations.................{self.B_cc} -adim-
        fyk: passive steel characteristic strength.................................{self.fyk} Mpa
        fpk: pre-stress steel characteristic strength..............................{self.fpk} Mpa
        
        YOUNG'S MODULUS
        Ecm: concrete average Young's modulus......................................{self.Ecm} Mpa
        Ecm_t: time-dependent secant concrete elastic modulus......................{self.E_cmt} Mpa
        Es: passive steel Young's modulus..........................................{self.Es} Mpa
        Ep: pre-stress steel Young's modulus.......................................{self.Ep} Mpa
        
        MISCELLANEOUS
        ns: passive steel homogenization coefficient...............................{self.ns} -adim-
        n_st: time dependent passive steel homogenization coefficient..............{self.n_st} -adim-
        np: pre-stress steel homogenization coefficient............................{self.np} -adim-
        n_pt: time dependent active steel homogenization coefficient...............{self.n_pt} -adim-
        s: cement type for time-dependent calculations (0.2, 0.25, 0.38)...........{self.s} -adim-
        prestress_time: days after concrete pouring when pre-stress is applied.....{self.prestress_time} days
        gc: concrete strength reduction coefficient................................{self.gc} -adim-
        gs: steel strength reduction coefficient...................................{self.gs} -adim-
        gp: pre-stress steel strength reduction coefficient........................{self.gp} -adim-
        
        REINFORECEMENT
        As1: passive steel area in the compression part of the beam................{self.As1} mm2
        As2: passive steel area in the tension part of the beam....................{self.As2} mm2
        Ap: pre-stress steel area..................................................{self.Ap} mm2
        
        -------------------------------SECTION GEOMETRY-----------------------------------------
        b: width of the smallest bounding box that contains the section............{self.b} mm
        h: height of the smallest bounding box that contains the section...........{self.h} mm
        y_cen: y coordinate of the centroid from the top fibre.....................{self.y_cen} mm
        Ac: brute area of the section..............................................{self.Ac} mm2
        Q_xtop: static moment from the top fibre...................................{self.Q_xtop} mm3 
        Ixo: moment of inertia around axis through the centroid....................{self.Ixo} mm4
        I_xtop: moment of inertia around axis through the top fibre................{self.I_xtop} mm4
        Wxo1: elastic section modulus from centroid to top fibre...................{self.Wxo1} mm3
        Wxo2: elastic section modulus from centroid to bottom fibre................{self.Wxo2} mm3
        ds1: distance from the top fibre to the centroid of As1....................{self.ds1} mm
        ds2: distance from the top fibre to the centroid of As2....................{self.ds2} mm
        dp: distance from the top fibre to the centroid of Ap......................{self.dp} mm
        ecc: signed eccentricity of active reinforcement...........................{self.ecc} mm
        
        HOMOGENIZED SECTION
        hmgA:......................................................................{self.hmgSect['A']} mm2
        hmgQ:......................................................................{self.hmgSect['Q']} mm3
        hmgI:......................................................................{self.hmgSect['I']} mm4
        hmg_y_cen:.................................................................{self.hmgSect['y_cen']}mm
        hmg_Wxo1...................................................................{self.hmgSect['Wxo1']}mm3
        hmg_Wxo2...................................................................{self.hmgSect['Wxo2']}mm3
        
        TIME DEPENDENT HOMOGENIZED SECTION
        time-dep hmga:.............................................................{self.hmgSect_t['A']} mm2
        time-dep hmgQ:.............................................................{self.hmgSect_t['Q']} mm3
        time-dep hmgI:.............................................................{self.hmgSect_t['I']} mm4
        time-dep hmg_y_cen:........................................................{self.hmgSect_t['y_cen']}mm
        time-dep hmg_Wxo1:.........................................................{self.hmgSect_t['Wxo1']}mm3
        time-dep hmg_Wxo2:.........................................................{self.hmgSect_t['Wxo2']}mm3
        
        -------------------------------LOADS------------------------------------------------
        N: normal force applied in the section's centroid..........................{self.N} N
        M: total moment applied to the section.....................................{self.M} mm*N
        k: signed curvature of the section.........................................{self.crv} mm-1
        eps_0: signed strain of top fibre..........................................{self.epsilon_c0} -admin-
        """
        return str

    def __upd_dep_attrs(self):
        """ updates all dependent attributes"""

        self.B_cc = self.Bcc()
        self.f_ckt = self.fck_t()
        self.f_cm = self.fcm()
        self.f_cm = self.fcm()  # average strength
        self.f_cmt = self.fcm_t()  # time dependent average strength
        self.f_ctm = self.fctm()  # average tension strength
        self.f_ctmt = self.fctm_t()  # time dependent average tension strength
        self.Ecm = 22 * pow(self.fcm() * 0.1, 0.3) * 1E3
        self.E_cmt = self.Ecm_t()  # time dependent secant Young's modulus
        self.ns = self.Es / self.Ecm
        self.np = self.Ep / self.Ecm
        self.n_st = self.Es / self.E_cmt
        self.n_pt = self.Ep / self.E_cmt
        self.Ac = self.bruteArea()
        self.Q_xtop = self.Qx_top()
        self.I_xtop = self.Ix_top()
        self.y_cen = self.ycentroid()
        self.ecc = self.e()
        self.Ixo = self.Ix0()
        self.Wxo1 = self.Wx01()
        self.Wxo2 = self.Wx02()
        self.hmgSect = self.hmgSection()
        self.hmgSect_t = self.hmgSection_t()
        self.crv = self.k()  # CURVATURE
        self.crv_t = self.k_t()
        self.epsilon_c0 = self.eps_0()  # TOP FIBRE'S STRAIN
        self.epsilon_c0t = self.eps_0_t()  # time-dep top fibre's strain

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


#-----------STATIC METHODS------------------------
    @staticmethod
    def A_yg(y, b, t, t1, t2):
        """area inside a portion of the section where the function b(y) has constant slope != 0
        up to a value y. the function b(y) for this portion is calculated as b*y + (t-b)/t2 * (y^2/2 - t1*y).
        To calulate the area of a portion between t1 and t2 write __A_yg(t1+t2) - __A_yg(t1).
        :param y: value you want to calculate the area of the section up to
        :param t1: value of y at the START of the portion you want to calculate the area of
        :param t2: length of the portion. The value of y at the END of the portion will be t1 + t2
        :param b: value of b(t1) corresponds with the value of b(y) at the START of the portion you want to
         calculate the area of
        :param t: value of b(t2) corresponds with the value of b(y) at the END of the portion you want to
         calculate the area of
        """
        if 0 < t2:
            return b * y + (t - b)/t2 * (pow(y, 2)/2 - t1*y)
        else:
            return 0

    @staticmethod
    def Q_yg(y, b, t, t1, t2):
        """ static moment of a portion of the section where b(y) has constant slope. Q(y) = Integral(x*b(y)dy)
        this function calculates the value of such function Q(y) for a given y
        :param y: value where you want to calculate the static moment of the section
        :param t1: value of y at the START of the portion you want to calculate the static moment of
        :param t2: length of the portion. The value of y at the END of the portion will be t1 + t2
        :param b: value of b(t1) corresponds with the value of b(y) at the START of the portion you want to
         calculate the static moment of
        :param t: value of b(t2) corresponds with the value of b(y) at the END of the portion you want to
         calculate the static moment of
        """
        if 0 < t2:
            return b*pow(y, 2)/2 + (t-b)/t2 * (pow(y, 3)/3 - t1*pow(y, 2)/2)
        else:
            return 0

    @staticmethod
    def I_yg(y, b, t, t1, t2):
        """ moment of inertia of a portion of the section  b(y) has constant slope. I(y) = Integral(x^2*b(y)dy)
        this function calculates the value of such function I(y) for a given y
        :param y: value where you want to calculate moment of inertia of the section
        :param t1: value of y at the START of the portion you want to calculate the moment of inertia of
        :param t2: length of the portion. The value of y at the END of the portion will be t1 + t2
        :param b: value of b(t1) corresponds with the value of b(y) at the START of the portion you want to
         calculate the moment of inertia of
        :param t: value of b(t2) corresponds with the value of b(y) at the END of the portion you want to
         calculate the moment of inertia of
        """
        if 0 < t2:
            return b*pow(y,3)/3 + (t-b)/t2 * (pow(y,4)/4 - t1*pow(y,3)/3)
        else:
            return 0

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
        return self.B_cc * self.f_cm

    def fctm(self):
        """average concrete tensile strength"""
        if self.fck <= 50:
            return 0.30 * pow(self.fck, 2 / 3)
        else:
            return 2.12 * log(1 + self.f_cm * 0.1)

    def fctm_t(self):
        """average time-dependent concrete tensile strength"""
        return self.B_cc * self.f_ctm

    def fck_t(self):
        """time-dependent concrete characteristic compression strength. t in days"""
        return self.B_cc * self.fck

    def Ecm_t(self):
        """time-dependent secant concrete elastic modulus"""
        return pow(self.f_cmt / self.f_cm, 0.3) * self.Ecm

    def e(self):
        """distance from the centroid to the pre-tensioned steel centroid"""
        return self.dp - self.y_cen

#-----------STRAIN SECTION METHODS ------------------

    def k(self):
        """signed curvature of the section"""
        num = self.N * self.hmgSect['Q'] - self.M * self.hmgSect['A']
        dem = self.Ecm * (pow(self.hmgSect['Q'], 2) - self.hmgSect['A'] * self.hmgSect['I'])
        return num / dem

    def k_t(self):
        """time-dependet signed curvature of the section"""
        num = self.N * self.hmgSect_t['Q'] - self.M * self.hmgSect_t['A']
        dem = self.E_cmt * (pow(self.hmgSect_t['Q'], 2) - self.hmgSect_t['A'] * self.hmgSect_t['I'])
        return num / dem

    def eps_0(self): # test
        """signed strain of top fibre"""
        num = self.M * self.hmgSect['Q'] - self.hmgSect['I'] * self.N
        dem = self.Ecm * (pow(self.hmgSect['Q'], 2) - self.hmgSect['A'] * self.hmgSect['I'])
        return num / dem

    def eps_0_t(self): # test
        """time-dependet signed strain of top fibre"""
        num = self.M * self.hmgSect_t['Q'] - self.hmgSect_t['I'] * self.N
        dem = self.Ecm * (pow(self.hmgSect_t['Q'], 2) - self.hmgSect_t['A'] * self.hmgSect_t['I'])
        return num / dem

    def eps(self, y):
        """strain in any point y to section's height"""
        return self.epsilon_c0 + self.crv * y

    def eps_t(self, y):
        """time-dep strain in any point y to section's height"""
        return self.epsilon_c0t + self.crv_t * y

    def stress(self, y):
        """stress in any point y to section's height"""
        return self.eps(y) * self.Ecm

    def stress_t(self, y):
        """stress in any point y to section's height"""
        return self.eps_t(y) * self.E_cmt

    def hmgSection(self):
        """dictionary {area, first moment of inertia, second moment of inertia}
        from the top fibre"""

        hmg = dict()
        hmgA = self.Ac
        hmgAc1 = self.As1 * (self.ns - 1)
        hmgAc2 = self.As2 * (self.ns - 1)
        hmgAcp = self.Ap * (self.np - 1)
        hmgArea = hmgA + hmgAc1 + hmgAc2 + hmgAcp

        # brure section static moment
        hmgQA = self.Q_xtop
        # reinforcement static moment
        hmgQc1 = hmgAc1 * self.ds1
        hmgQc2 = hmgAc2 * self.ds2
        hmgQcp = hmgAcp * self.dp
        hmgQ = hmgQA + hmgQc1 + hmgQc2 + hmgQcp

        hmgIA = self.I_xtop
        hmgIc1 = hmgQc1 * self.ds1
        hmgIc2 = hmgQc2 * self.ds2
        hmgIcp = hmgQcp * self.dp
        hmgI = hmgIA + hmgIc1 + hmgIc2 + hmgIcp

        # homogenized section's centroid
        hmg_y_cen = hmgQ / hmgA
        # homogenized section's elastic modulus
        hmg_W01 = hmgI / hmg_y_cen
        hmg_W02 = hmgI / (self.h - hmg_y_cen)

        hmg['A'] = hmgArea
        hmg['Q'] = hmgQ
        hmg['I'] = hmgI
        hmg['y_cen'] = hmg_y_cen
        hmg['Wxo1'] = hmg_W01
        hmg['Wxo2'] = hmg_W02

        return hmg

    def hmgSection_t(self):
        """dictionary {area, first moment of inertia, second moment of inertia}
        from the top fibre"""

        hmg = dict()
        hmgA = self.Ac
        hmgAc1 = self.As1 * (self.n_st - 1)
        hmgAc2 = self.As2 * (self.n_st - 1)
        hmgAcp = self.Ap * (self.n_pt - 1)
        hmgArea = hmgA + hmgAc1 + hmgAc2 + hmgAcp

        # brure section static moment
        hmgQA = self.Q_xtop
        # reinforcement static moment
        hmgQc1 = hmgAc1 * self.ds1
        hmgQc2 = hmgAc2 * self.ds2
        hmgQcp = hmgAcp * self.dp
        hmgQ = hmgQA + hmgQc1 + hmgQc2 + hmgQcp

        hmgIA = self.I_xtop
        hmgIc1 = hmgQc1 * self.ds1
        hmgIc2 = hmgQc2 * self.ds2
        hmgIcp = hmgQcp * self.dp
        hmgI = hmgIA + hmgIc1 + hmgIc2 + hmgIcp

        # homogenized section's centroid
        hmg_y_cen = hmgQ / hmgA
        # homogenized section's elastic modulus
        hmg_W01 = hmgI / hmg_y_cen
        hmg_W02 = hmgI / (self.h - hmg_y_cen)

        hmg['A'] = hmgArea
        hmg['Q'] = hmgQ
        hmg['I'] = hmgI
        hmg['y_cen'] = hmg_y_cen
        hmg['Wxo1'] = hmg_W01
        hmg['Wxo2'] = hmg_W02
        return hmg

    def ycentroid_hmg(self):
        """y coordinate of the centroid of the homogenized section from the top fibre """
        return self.hmgSect['Q'] / self.hmgSect['A']

    def ycentroid_hmg_t(self):
        """y coordinate of the centroid of the time-dependent homogenized section from the top fibre"""
        return self.hmgSect_t['Q'] / self.hmgSect_t['A']

    def magnel_stress_limit(self, Mi: float, Mf: float):
        """checks if a section meets tension limits according to spanish
        structural code. This is a short-term check. No cracking is taken into account.
        :param Mi: mm*N initial moment (at the instant of prestress)
        :param Mf: mm*N complete moment under service loads
        """
        # security coefficients must already been taken into account
        # loads introduced must be the total loads applied to the section (sum all your moments and normal forces)
        # moments must be calculated from the top fibre
        # initial load case stress
        self.M = Mi
        init_top_stress = self.stress_t(0)
        init_bottom_stress = self.stress_t(self.h)

        # final load case stress
        self.M = Mf
        final_top_stress = self.stress(0)
        final_bottom_stress = self.stress(self.h)

        init_top_check = (-0.45 * self.f_ckt) < init_top_stress < self.f_ctmt
        init_bottom_check = (-0.45 * self.f_ckt) < init_bottom_stress < self.f_ctmt
        final_top_check = (-0.45 * self.fck) < final_top_stress < self.f_ctm
        final_bottom_check = (-0.45 * self.fck) < final_bottom_stress < self.f_ctm

        return init_top_check and init_bottom_check and final_top_check and final_bottom_check

#----------SECTION MODULUS------------
    def Wx01(self) -> float(): #text
        """elastic section modulus considering the inertia from the centroid
         and the distance from the centroid to the top fibre"""
        return self.Ixo / self.y_cen

    def Wx02(self) ->float(): #test
        """elastic section modulus considering the inertia
        and the distance from the centroid to the top fibre"""
        return self.Ixo / (self.h - self.y_cen)
