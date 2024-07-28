from StructEng.Sections.class_Section import Section
from StructEng.Materials.class_Concrete import Concrete
from StructEng.Materials.class_ReinforcementSteel import ReinforcementSteel
from StructEng.Materials.class_PrestressSteel import PrestressSteel


class ConcreteSection(Section):
    concrete_default = Concrete()
    passive_steel_default = ReinforcementSteel()
    prestress_steel_default = PrestressSteel()
    kwDefaults = {
        'As1': 0,
        'As2': 0,
        'Ap': 0,
        'b': 500,
        'h': 1000,
        'ds1': 50,
        'ds2': 950,
        'dp': 850,
        'N': 0,
        'M': 0
    }

    def __init__(self, concrete: Concrete = concrete_default,
                 steel_s: ReinforcementSteel = passive_steel_default,
                 steel_p: PrestressSteel = prestress_steel_default,
                 **kwargs):

        # MATERIAL
        self.concrete = concrete
        self.passive_steel = steel_s
        self.prestress_steel = steel_p

        self.ns = self.passive_steel.Es / self.concrete.Ecm
        self.n_st = self.passive_steel.Es / self.concrete.E_cmt
        self.np = self.prestress_steel.Ep / self.concrete.Ecm
        self.n_pt = self.prestress_steel.Ep / self.concrete.E_cmt

        # REINFORCEMENT AREA
        self.As1 = kwargs.get('As1', self.kwDefaults['As1'])
        self.As2 = kwargs.get('As2', self.kwDefaults['As2'])
        self.Ap = kwargs.get('Ap', self.kwDefaults['Ap'])

        # DIMENSIONS
        self.b = kwargs.get('b', self.kwDefaults['b'])
        self.h = kwargs.get('h', self.kwDefaults['h'])
        self.Ac = self.bruteArea()
        self.Q_xtop = self.Qx_top()
        self.y_cen = self.ycentroid()
        self.I_xtop = self.Ix_top()
        self.Ixo = self.Ix0()
        self.Wxo1 = self.Wx01()
        self.Wxo2 = self.Wx02()

        # REINFORCEMENT POSITIONS
        self.ds1 = kwargs.get('ds1', self.kwDefaults['ds1'])
        self.ds2 = kwargs.get('ds2', self.kwDefaults['ds2'])
        self.dp = kwargs.get('dp', self.kwDefaults['dp'])
        self.dc = 0
        self.y0 = 0
        self.ecc = self.e()  # active reinforcement eccentricity

        # HOMOGENIZED SECTION
        self.hmgSect = self.hmgSection()
        self.hmgSect_t = self.hmgSection_t()
        self.hmgSect_y = self.hmgSection_y(self.y0)

        # LOADS
        self.N = kwargs.get('N', self.kwDefaults['N'])
        self.M = kwargs.get('M', self.kwDefaults['M'])

        # STRAIN
        self.crv = self.k()  # CURVATURE
        self.crv_t = self.k_t()  # time-dep curvature
        self.crv_cr = self.k_cr()  # cracked curvature
        self.epsilon_c0 = self.eps_0()  # TOP FIBRE'S STRAIN
        self.epsilon_c0t = self.eps_0_t()  # time-dep top fibre's strain
        self.epsilon_c0cr = self.eps_0_cr()  # cracked section top fibre's strain

    def __str__(self):
        string = f"""
        ########################################################################################
        BEAM INFO
        ########################################################################################
        
        -------------------------------MATERIALS------------------------------------------------
        CONCRETE
        {self.concrete.__str__()}
        
        PASSIVE STEEL REINFORCEMENT
        {self.passive_steel.__str__()}
        
        PRESTRESS STEEL REINFORCEMENT
        {self.prestress_steel.__str__()}
        
        MISCELLANEOUS
        ns: passive steel homogenization coefficient...............................{self.ns} -adim-
        n_st: time dependent passive steel homogenization coefficient..............{self.n_st} -adim-
        np: pre-stress steel homogenization coefficient............................{self.np} -adim-
        n_pt: time dependent active steel homogenization coefficient...............{self.n_pt} -adim-
        
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
        hmgA: homogenized area.....................................................{self.hmgSect['A']} mm2
        hmgQ_xtop: homogenized static moment from top fibre........................{self.hmgSect['Q']} mm3
        hmgI_xtop: homogenized moment of inertia from top fibre....................{self.hmgSect['I']} mm4
        hmgI_xo: homogenized moment of inertia from centroid.......................{self.hmgSect['Ixo']} mm4
        hmg_y_cen: homogenized centroid y coordinate form top fibre................{self.hmgSect['y_cen']} mm
        hmg_ecc: homogenized active reinforcement eccentricity.....................{self.hmgSect['ecc']} mm
        hmg_Wxo1:homogenized elastic modulus (top fibre)...........................{self.hmgSect['Wxo1']} mm3
        hmg_Wxo2: homogenized elastic modulus (bottom fibre).......................{self.hmgSect['Wxo2']} mm3
        
        TIME DEPENDENT HOMOGENIZED SECTION
        time-dep hmgA:.............................................................{self.hmgSect_t['A']} mm2
        time-dep hmgQ_xtop:........................................................{self.hmgSect_t['Q']} mm3
        time-dep hmgI_xtop:........................................................{self.hmgSect_t['I']} mm4
        time-dep hmgI_xo:..........................................................{self.hmgSect_t['Ixo']} mm4
        time-dep hmg_y_cen:........................................................{self.hmgSect_t['y_cen']} mm
        time-dep hmg_ecc: homogenized active reinforcement eccentricity............{self.hmgSect['ecc']} mm
        time-dep hmg_Wxo1:.........................................................{self.hmgSect_t['Wxo1']} mm3
        time-dep hmg_Wxo2:.........................................................{self.hmgSect_t['Wxo2']} mm3
        
        CRACKED HOMOGENIZED SECTION
        hmgA: cracked homogenized area.............................................{self.hmgSect_y['A']} mm2
        hmgQ_xtop: cracked homogenized static moment from top fibre................{self.hmgSect_y['Q']} mm3
        hmgI_xtop: cracked homogenized moment of inertia from top fibre............{self.hmgSect_y['I']} mm4
        hmgI_xo: cracked homogenized moment of inertia from centroid...............{self.hmgSect_y['Ixo']} mm4
        hmg_y_cen: cracked homogenized centroid y coordinate form top fibre........{self.hmgSect_y['y_cen']} mm
        hmg_ecc: cracked homogenized active reinforcement eccentricity.............{self.hmgSect_y['ecc']} mm
        hmg_Wxo1: cracked homogenized elastic modulus (top fibre)..................{self.hmgSect_y['Wxo1']} mm3
        hmg_Wxo2: cracked homogenized elastic modulus (bottom fibre)...............{self.hmgSect_y['Wxo2']} mm3
        
        -------------------------------LOADS------------------------------------------------
        N: normal force applied in the section's centroid..........................{self.N} N
        M: total moment applied to the section.....................................{self.M} mm*N
        
        ------------------------------STRAINS-----------------------------------------------
        y0: height of the non-cracked section form the top fibre...................{self.y0} mm
        k: signed curvature of the section.........................................{self.crv} mm-1
        eps_0: signed strain of top fibre..........................................{self.epsilon_c0} -admin-
        """
        return string

    def __updt_dep__attrs(self) -> None:
        """updates dependent attrs"""
        self.ns = self.passive_steel.Es / self.concrete.Ecm
        self.n_st = self.passive_steel.Es / self.concrete.E_cmt
        self.np = self.prestress_steel.Ep / self.concrete.Ecm
        self.n_pt = self.prestress_steel.Ep / self.concrete.E_cmt

        self.Ac = self.bruteArea()
        self.Q_xtop = self.Qx_top()
        self.y_cen = self.ycentroid()
        self.I_xtop = self.Ix_top()
        self.Ixo = self.Ix0()
        self.Wxo1 = self.Wx01()
        self.Wxo2 = self.Wx02()
        self.ecc = self.e()

        self.hmgSect = self.hmgSection()
        self.hmgSect_t = self.hmgSection_t()
        self.hmgSect_y = self.hmgSection_y(self.y0)

        self.crv = self.k()  # CURVATURE
        self.crv_t = self.k_t()  # time-dep curvature
        self.crv_cr = self.k_cr()  # cracked curvature
        self.epsilon_c0 = self.eps_0()  # TOP FIBRE'S STRAIN
        self.epsilon_c0t = self.eps_0_t()  # time-dep top fibre's strain
        self.epsilon_c0cr = self.eps_0_cr()  # cracked section top fibre's strain

    def set(self, default=False, concrete: Concrete = concrete_default,
            passive_steel: ReinforcementSteel = passive_steel_default,
            prestress_steel: PrestressSteel = prestress_steel_default,
            **kwargs):
        """sets attributes to the values passed in a dict"""
        if default:
            for k in self.kwDefaults:
                self.__dict__[k] = self.kwDefaults[k]
        else:
            for k in kwargs:
                self.__dict__[k] = kwargs[k]

    # -------------ABSTRACT METHODS--------------

    # -----------STATIC METHODS------------------------
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
            return b * y + (t - b) / t2 * (pow(y, 2) / 2 - t1 * y)
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
            return b * pow(y, 2) / 2 + (t - b) / t2 * (pow(y, 3) / 3 - t1 * pow(y, 2) / 2)
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
            return b * pow(y, 3) / 3 + (t - b) / t2 * (pow(y, 4) / 4 - t1 * pow(y, 3) / 3)
        else:
            return 0

    # ------------CONCRETE METHODS---------------------

    def e(self):
        """distance from the centroid to the pre-tensioned steel centroid"""
        return self.dp - self.y_cen

    # -----------STRAIN SECTION METHODS ------------------

    def k(self):
        """signed curvature of the section"""
        num = self.N * self.hmgSect['Q'] - self.M * self.hmgSect['A']
        dem = self.concrete.E_cm * (pow(self.hmgSect['Q'], 2) - self.hmgSect['A'] * self.hmgSect['I'])
        return num / dem

    def k_t(self):
        """time-dependet signed curvature of the section"""
        num = self.N * self.hmgSect_t['Q'] - self.M * self.hmgSect_t['A']
        dem = self.concrete.E_cmt * (pow(self.hmgSect_t['Q'], 2) - self.hmgSect_t['A'] * self.hmgSect_t['I'])
        return num / dem

    def k_cr(self):
        """curvature of the cracked section"""
        num = self.hmgSect_y['Q'] * self.N - self.hmgSect_y['A']
        dem = self.concrete.E_cm * (pow(self.hmgSect_y['Q'], 2) - self.hmgSect_y['A'] * self.hmgSect_y['I'])
        return num / dem

    def eps_0(self):  # test
        """signed strain of top fibre"""
        num = self.M * self.hmgSect['Q'] - self.hmgSect['I'] * self.N
        dem = self.concrete.E_cm * (pow(self.hmgSect['Q'], 2) - self.hmgSect['A'] * self.hmgSect['I'])
        return num / dem

    def eps_0_t(self):  # test
        """time-dependet signed strain of top fibre"""
        num = self.M * self.hmgSect_t['Q'] - self.hmgSect_t['I'] * self.N
        dem = self.concrete.E_cm * (pow(self.hmgSect_t['Q'], 2) - self.hmgSect_t['A'] * self.hmgSect_t['I'])
        return num / dem

    def eps_0_cr(self):
        num = self.hmgSect_y['Q'] * self.M - self.hmgSect_y['I'] * self.N
        dem = self.concrete.E_cm * (pow(self.hmgSect_y['Q'], 2) - self.hmgSect_y['A'] * self.hmgSect_y['I'])
        return num / dem

    def eps(self, y):
        """strain at any point y of section's height
        :param y: distance from top fibre to evaluate strain at
        """
        return self.epsilon_c0 + self.crv * y

    def eps_t(self, y):
        """time-dep strain at any point y to section's height"""
        return self.epsilon_c0t + self.crv_t * y

    def eps_cr(self, y):
        """strain at any point y of the section's height. The section is cracked, being the non-cracked portion
        height y0. M, N are the whole moment and normal force applied to the section respectively. before using
        this function change self.M, self.N to the correct values
        :param y: point of the section's height to evaluate eps_y() at"""

        return self.eps_0_cr() + self.crv_cr * y

    # STRESS METHODS
    def stress(self, y):
        """stress at any point y to section's height"""
        return self.eps(y) * self.concrete.E_cm

    def stress_t(self, y):
        """stress at any point y to section's height"""
        return self.eps_t(y) * self.concrete.E_cmt

    # HOMOGENIZED SECTION METHODS
    def hmgSection(self):
        """dictionary {area, first moment of inertia, second moment of inertia}
        from the top fibre of the homogenized section"""

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
        # homogenized active reinforcement eccentricity
        hmg_ecc = self.dp - hmg_y_cen
        # homogenized section's inertia from centroid
        hmgI0 = hmgI - hmgA * pow(hmg_y_cen, 2)
        # homogenized section's elastic modulus
        hmg_W01 = hmgI0 / hmg_y_cen
        hmg_W02 = hmgI0 / (self.h - hmg_y_cen)

        hmg['A'] = hmgArea
        hmg['Q'] = hmgQ
        hmg['I'] = hmgI
        hmg['Ixo'] = hmgI0
        hmg['y_cen'] = hmg_y_cen
        hmg['ecc'] = hmg_ecc
        hmg['Wxo1'] = hmg_W01
        hmg['Wxo2'] = hmg_W02

        return hmg

    def hmgSection_y(self, y):
        """dictionary {Area, First moment of inertia, Second moment of inertia}
        from the top fibre to an arbitrary fibre a distance y from the top surface
        of the homogenized section. All homogenized area of steel reinforcement (passive and active)
        is taken into account whatever the param y. that is because this function is used in cracked section
        checks"""

        hmg = dict()
        # only brute area properties A,Q,I and derived results  is affected by the param y
        hmgA = self.A_y(y)
        hmgAc1 = self.As1 * (self.ns - 1)
        hmgAc2 = self.As2 * (self.ns - 1)
        hmgAcp = self.Ap * (self.np - 1)
        hmgArea = hmgA + hmgAc1 + hmgAc2 + hmgAcp

        # brute section's static moment
        hmgQA = self.Q_y(y)
        # reinforcement's static moment
        hmgQc1 = hmgAc1 * self.ds1
        hmgQc2 = hmgAc2 * self.ds2
        hmgQcp = hmgAcp * self.dp
        hmgQ = hmgQA + hmgQc1 + hmgQc2 + hmgQcp

        hmgIA = self.I_y(y)
        hmgIc1 = hmgQc1 * self.ds1
        hmgIc2 = hmgQc2 * self.ds2
        hmgIcp = hmgQcp * self.dp
        hmgI = hmgIA + hmgIc1 + hmgIc2 + hmgIcp

        # homogenized section's centroid
        hmg_y_cen = hmgQ / hmgA
        # homogenized active reinforcement eccentricity
        hmg_ecc = self.dp - hmg_y_cen
        # homogenized section's inertia from centroid
        hmgI0 = hmgI - hmgA * pow(hmg_y_cen, 2)
        # homogenized section's elastic modulus
        hmg_W01 = hmgI0 / hmg_y_cen
        hmg_W02 = hmgI0 / (self.h - hmg_y_cen)

        hmg['A'] = hmgArea
        hmg['Q'] = hmgQ
        hmg['I'] = hmgI
        hmg['Ixo'] = hmgI0
        hmg['y_cen'] = hmg_y_cen
        hmg['ecc'] = hmg_ecc
        hmg['Wxo1'] = hmg_W01
        hmg['Wxo2'] = hmg_W02

        return hmg

    def hmgSection_t(self):
        """dictionary {area, first moment of inertia, second moment of inertia}
        from the top fibre  of the homogenized section"""

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
        # homogenized active reinforcement eccentricity
        hmg_ecc = self.dp - hmg_y_cen
        # homogenized section's inertia from centroid
        hmgI0 = hmgI - hmgA * pow(hmg_y_cen, 2)
        # homogenized section's elastic modulus
        hmg_W01 = hmgI0 / hmg_y_cen
        hmg_W02 = hmgI0 / (self.h - hmg_y_cen)

        hmg['A'] = hmgArea
        hmg['Q'] = hmgQ
        hmg['I'] = hmgI
        hmg['Ixo'] = hmgI0
        hmg['y_cen'] = hmg_y_cen
        hmg['ecc'] = hmg_ecc
        hmg['Wxo1'] = hmg_W01
        hmg['Wxo2'] = hmg_W02
        return hmg

    # MAGNEL STRESS LIMIT
    def magnel_stress_limit(self, Mi: float, Mf: float) -> bool:
        """checks if a section meets tension limits according to spanish
        structural code. This is a short-term check. No cracking is taken into account.
        :param Mi: mm*N initial whole moment (external + prestress moments from top fibre
        . at the instant of prestress)
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

        init_top_check = (-0.45 * self.concrete.f_ckt) < init_top_stress < self.concrete.f_ctmt
        init_bottom_check = (-0.45 * self.concrete.f_ckt) < init_bottom_stress < self.concrete.f_ctmt
        final_top_check = (-0.45 * self.concrete.fck) < final_top_stress < self.concrete.f_ctm
        final_bottom_check = (-0.45 * self.concrete.fck) < final_bottom_stress < self.concrete.f_ctm

        return init_top_check and init_bottom_check and final_top_check and final_bottom_check

    # ----------SECTION MODULUS------------
    def Wx01(self) -> float():  # text
        """elastic section modulus considering the inertia from the centroid
         and the distance from the centroid to the top fibre"""
        return self.Ixo / self.y_cen

    def Wx02(self) -> float():  # test
        """elastic section modulus considering the inertia
        and the distance from the centroid to the top fibre"""
        return self.Ixo / (self.h - self.y_cen)
