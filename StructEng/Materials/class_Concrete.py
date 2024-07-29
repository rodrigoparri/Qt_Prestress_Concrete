from math import exp, log, sqrt
# from StructEng.Materials.class_Material import Material


class Concrete:

    kwDefaults = {
        'fck': 30,
        'gc': 1.5,  # concrete safety coefficient
        'h0': 100,  # theoretical element dimension (mm). Must be changed to its actual value at section init
        'cem_type': 'N',  # cement type S, N, R
        'prestress_time': 7,
        'HR': 25,
        'T': 25,  # time-weighted average temperature the concrete will be exposed to
        'life_exp': 100  # life expectancy in years
    }

    def __init__(self, **kwargs):
        self.fck = kwargs.get('fck', self.kwDefaults['fck'])
        self.gc = kwargs.get('gc', self.kwDefaults['gc'])
        self.h0 = kwargs.get('h0', self.kwDefaults['h0'])
        self.prestress_time = kwargs.get('prestress_time', self.kwDefaults['prestress_time'])
        self.cem_type = kwargs.get('cem_type', self.kwDefaults['cem_type'])
        self.HR = kwargs.get('HR', self.kwDefaults['HR'])
        self.T = kwargs.get('T', self.kwDefaults['T'])
        self.life_exp = kwargs.get('life_exp', self.kwDefaults['life_exp'])

        # current stress applied to the material
        self.sigma_c = 0
        # strength attributes
        self.s = self.s_cem()
        self.B_cc = self.Bcc()
        self.f_ckt = self.fck_t()
        self.f_cm = self.fcm()
        self.f_cmt = self.fcm_t()
        self.f_ctm = self.fctm()
        self.f_ctmt = self.fctm_t()
        # Young modulus attrs
        self.E_cm = self.Ecm()
        self.E_c = self.Ec()
        self.E_cmt = self.Ecm_t()
        # stain attrs
        self.epsilon_c2 = self.eps_c2()
        # strength modifier attrs (used in creep calculations)
        self.alpha_ = self.alpha()
        self.alpha_1 = self.alpha_n(0.7)
        self.alpha_2 = self.alpha_n(0.2)
        self.alpha_3 = self.alpha_n(0.5)

        self.t_0T = self.t0T()
        self.t_0 = self.t0()

        # terms for basic creep coefficient
        self.phi_HR = self.phiHR()
        self.B_fcm = self.Bfcm()
        self.B_t0 = self.Bt0()
        self.B_ct = self.Bc_t()
        # basic creep coefficient
        self.phi_0 = self.phi0()
        # linear creep coefficient
        self.phi_t = self.phi_time()
        # non-linear creep coefficient
        self.phi_nl = self.phi_non_lin()

    def __str__(self):
        string = f"""
        STRENGTH
        fck_t: concrete characteristic compression strength. t in days.............{self.f_ckt} Mpa
        fcm: average concrete compression strength.................................{self.f_cm} Mpa
        fcm_t: time-dependent average concrete compression strength................{self.f_cmt} Mpa
        fctm: average concrete tensile strength....................................{self.f_ctm} Mpa
        fctm_t: average time-dependent concrete tensile strength...................{self.f_ctmt} Mpa
        Bcc: time dependent scalar for time-dependent calculations.................{self.B_cc} -adim-
        
        YOUNG'S MODULUS
        Ecm: concrete average Young's modulus......................................{self.Ecm} Mpa
        Ec: concrete secant Young's modulus........................................{self.Ec} Mpa
        Ecm_t: time-dependent secant concrete elastic modulus......................{self.E_cmt} Mpa

        YIELD STRAIN
        epsilon_c2: concrete yield strain parable-rectangle model..................{self.epsilon_c2} -adim-
                
        CREEP METHODS AND ATTRIBUTES
        phi_t: time-dependent creep coefficient....................................{self.phi_t} -adim-
        phi_nl: time-dependent non-linear creep coefficient........................{self.phi_nl} -adim-
        phi_0: basic creep coefficient.............................................{self.phi_0} -adim-
        B_ct: time dependent scalar of time-dependent creep coefficient............{self.B_ct} -adim-
        phi_HR: relative humidity component of the basic creep coefficient.........{self.phi_HR} -adim-
        B_fcm: strength component of the basic creep coefficient...................{self.B_fcm} -adim-
        B_t0: initial loading time component of the basic creep coefficient........{self.B_t0} -adim-
        t_0: cement dependent initial loading time.................................{self.t_0} days
        t_0T: age at loading time correct as a function of temperature.............{self.t_0T} days
        
        alpha_: cement type-dependent exponent...................................{self.alpha_} -adim-
        alpha_1: factor taking into account concrete strength....................{self.alpha_1} -adim-
        alpha_2: factor taking into account concrete strength....................{self.alpha_2} -adim-
        alpha_3: factor taking into account concrete strength....................{self.alpha_3} -adim-
        """

        return string

    def __updt_dep_attrs(self) -> None:
        self.s = self.s_cem()
        self.B_cc = self.Bcc()
        self.f_ckt = self.fck_t()
        self.f_cm = self.fcm()
        self.f_cmt = self.fcm_t()
        self.f_ctm = self.fctm()
        self.f_ctmt = self.fctm_t()
        # Young modulus attrs
        self.E_cm = self.Ecm()
        self.E_c = self.Ec()
        self.E_cmt = self.Ecm_t()
        # stain attrs
        self.epsilon_c2 = self.eps_c2()
        # strength modifier attrs (used in creep calculations)
        self.alpha_ = self.alpha()
        self.alpha_1 = self.alpha_n(0.7)
        self.alpha_2 = self.alpha_n(0.2)
        self.alpha_3 = self.alpha_n(0.5)

        self.t_0T = self.t0T()
        self.t_0 = self.t0()

        # terms for basic creep coefficient
        self.phi_HR = self.phiHR()
        self.B_fcm = self.Bfcm()
        self.B_t0 = self.Bt0()
        self.B_ct = self.Bc_t()
        # basic creep coefficient
        self.phi_0 = self.phi0()
        # linear creep coefficient
        self.phi_t = self.phi_time()
        # non-linear creep coefficient
        self.phi_nl = self.phi_non_lin()

    def set(self, default: bool=False, **kwargs) -> None:
        if default:
            for k in self.kwDefaults:
                self.__dict__[k] = self.kwDefaults[k]
        else:
            for k in kwargs:
                self.__dict__[k] = kwargs[k]

        self.__updt_dep_attrs()

    def s_cem(self) -> float:
        """coefficient that depends on cement type"""
        if self.cem_type == 'R':
            return 0.2
        elif self.cem_type == 'N':
            return 0.25
        elif self.cem_type == 'S':
            return 0.38
        else:
            raise ValueError

    def Bcc(self) -> float:
        """time dependent scalar that reduces concrete strength for a time t
        between 3 and 28 days
        """
        return exp(self.s * (1 - pow(28 / self.prestress_time, 0.5)))

    def fcm(self) -> int:
        """ average concrete compression strength"""
        return self.fck + 8

    def fcm_t(self):
        """time-dependent average concrete compression strength"""
        return self.B_cc * self.f_cm

    def fctm(self):
        """average concrete tensile strength"""
        if 0 < self.fck <= 50:
            return 0.30 * pow(self.fck, 2 / 3)
        elif self.fck > 50:
            return 2.12 * log(1 + self.f_cm * 0.1)
        else:
            raise ValueError

    def fctm_t(self):
        """average time-dependent concrete tensile strength"""
        return self.B_cc * self.f_ctm

    def fck_t(self):
        """time-dependent concrete characteristic compression strength. t in days"""
        return self.B_cc * self.fck

    def Ecm(self):
        """average concrete elastic modulus"""
        return 22 * pow(self.f_cm * 0.1, 0.3) * 1E3

    def Ec(self):
        return  1.05 * self.E_cm

    def Ecm_t(self):
        """time-dependent average concrete elastic modulus"""
        return pow(self.f_cmt / self.f_cm, 0.3) * self.E_cm

    def eps_c2(self):
        """yield strain according to spanish Código Estructural parable-rectangle stress-strain model"""
        if self.fck <= 50:
            return 0.002
        else:
            return 2 + 0.85 * pow(self.fck - 50, 0.53)

# CREEP METHODS
    def alpha(self):
        if self.cem_type == 'S':
            return -1
        elif self.cem_type == 'N':
            return 0
        elif self.cem_type == 'R':
            return 1
        else:
            raise ValueError

    def alpha_n(self, n):
        """factors that take into account the influence of concrete's strength
        :param n: can be 0.7, 0.2, 0.5"""
        return pow(35/self.f_cm, n)

    def phiHR(self):
        """coefficient that takes into account the relative humidity over the
        basic creep coefficient"""
        num = 1 - self.HR * 0.01
        dem = 0.1 * pow(self.h0, 1 / 3)

        if 0 < self.f_cm <= 35:
            return 1 + num / dem
        elif self.f_cm > 35:
            return (1 + num / dem * self.alpha_1) * self.alpha_2
        else:
            raise ValueError

    def Bfcm(self):
        """coefficient that takes into account the concrete's strength over the
        basic creep coefficient"""
        return 16.8 / sqrt(self.f_cm)

    def Bt0(self):
        """coefficient that takes into account the loading age over the
        basic creep coefficient"""
        return 1 / (0.1 + pow(self.t_0, 0.2))

    def B_H(self):
        """Coefficient depending on relative humidity (%) and the theoretical
        element size (mm)"""
        a = 1.5 * (1 + pow(0.012 * self.HR, 18) * self.h0)
        Bh = a + 250
        if 0 < self.f_cm <= 35:
            if Bh <= 1500:
                return Bh
            else:
                return 1500
        elif self.f_cm > 35:
            Bh = a + 250 * self.alpha_3
            a = 1500 * self.alpha_3
            if Bh <= a:
                return Bh
            else:
                return a

    def Bc_t(self):
        """coefficient describing creep development over time after loading"""
        num = self.t_0T - self.t_0
        dem = self.B_H() + num
        return pow(num / dem, 0.3)

    def t0(self):
        """the cement type effects over the creep coefficient can be taken into account modifying the loading age
        t0 according to the next expression"""
        to = self.t_0T * pow(9 / (2 + pow(self.t_0T, 1.2)) + 1, self.alpha_)
        if to >= 0.5:
            return to
        elif 0 <= to < 0.5:
            return 0.5
        else:
            raise ValueError

    def t0T(self):
        """loading age adjusted that replaces t in the corresponding equations"""
        return exp(-(4000 / (273 + self.T) - 13.65)) * (28 - self.prestress_time)

    def phi0(self):
        return self.phi_HR * self.B_fcm * self.B_t0

    def phi_time(self):
        return self.phi_0 * self.B_ct

    def phi_non_lin(self):
        return self.phi_t * exp(1.5 * (self.sigma_c / self.f_ckt - 0.45))

# SHRINKAGE METHODS


if __name__ == '__main__':
    attrs = {
        'fck': 40,
        'gc': 1.5,  # concrete safety coefficient
        'h0': 300,
        's': 'N',  # S, N, R
        'prestress_time': 5,
        'HR': 45,
        'T': 17,  # time-weighted average temperature the concrete will be exposed to
        'life_exp': 50  # life expectancy in years
    }
    concrete = Concrete(**attrs)
