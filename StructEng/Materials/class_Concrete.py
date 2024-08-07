from math import exp, log, sqrt
import numpy as np
# from StructEng.Materials.class_Material import Material


class Concrete:

    kwDefaults = {
        'fck': 30,
        'gc': 1.5,  # concrete safety coefficient
        'h0': 100,  # theoretical element dimension (mm). Must be changed to its actual value at section init
        'cem_type': 'N',  # cement type S, N, R
        'temperature_dependent': False,  # set to True if temperature effects have to be taken into account
        'prestress_time': 7,  # time in days from concrete pouring when prestress is applied
        'T_data': tuple(),  # daily concrete temperature data during curing
        'HR': 25,
        'delayed_effects_time': 25550  # time in days to calculate delayed time effects. 70 years in days by default
    }

    def __init__(self, **kwargs):
        self.fck: int = kwargs.get('fck', self.kwDefaults['fck'])
        self.gc: float = kwargs.get('gc', self.kwDefaults['gc'])
        self.h0: float = kwargs.get('h0', self.kwDefaults['h0'])
        self.prestress_time: int = kwargs.get('prestress_time', self.kwDefaults['prestress_time'])
        self.cem_type: str = kwargs.get('cem_type', self.kwDefaults['cem_type'])
        self.HR: int = kwargs.get('HR', self.kwDefaults['HR'])
        self.T_data: tuple = kwargs.get('T_data', self.kwDefaults['T_data'])
        self.temperature_dependent: bool = kwargs.get('temperature_dependent', self.kwDefaults['temperature_dependent'])
        self.delayed_effects_time: int = kwargs.get('delayed_effects_time', self.kwDefaults['delayed_effects_time'])

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

        self.__init_t_0()  # initialize prestress time adjusted to cement type

        # terms for basic creep coefficient
        self.phi_HR = self.phiHR()
        self.B_fcm = self.Bfcm()
        self.B_t0 = self.Bt0(self.t_0_cem)
        self.B_ct = self.Bc_t(self.delayed_effects_time, self.t_0_cem)
        # basic creep coefficient
        self.phi_0 = self.phi0(self.t_0_cem)
        # linear creep coefficient
        self.phi_t = self.phi_time(self.delayed_effects_time, self.t_0_cem)
        # non-linear creep coefficient
        self.phi_nl = self.phi_non_lin(self.delayed_effects_time, self.t_0_cem)

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
        t_0_cem: cement dependent initial loading time.............................{self.t_0_cem} days
        t_0T: age at loading time corrected as a function of temperature...........{self.t_0T} days
        
        alpha_: cement type-dependent exponent.....................................{self.alpha_} -adim-
        alpha_1: factor taking into account concrete strength......................{self.alpha_1} -adim-
        alpha_2: factor taking into account concrete strength......................{self.alpha_2} -adim-
        alpha_3: factor taking into account concrete strength......................{self.alpha_3} -adim-
        """

        return string

    def __updt_dep_attrs(self) -> None:
        """update all dependent attributes"""
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

        self.__init_t_0()

        # terms for basic creep coefficient
        self.phi_HR = self.phiHR()
        self.B_fcm = self.Bfcm()
        self.B_t0 = self.Bt0(self.t_0_cem)
        self.B_ct = self.Bc_t(self.delayed_effects_time, self.t_0_cem)
        # basic creep coefficient
        self.phi_0 = self.phi0(self.t_0_cem)
        # linear creep coefficient
        self.phi_t = self.phi_time(self.delayed_effects_time, self.t_0_cem)
        # non-linear creep coefficient
        self.phi_nl = self.phi_non_lin(self.delayed_effects_time, self.t_0_cem)

    def __init_t_0(self) -> None:  # ultimate responsible for temperature dependent calculations
        """private t_0 (cement-dependent initial prestress time) attribute initialization"""
        if self.temperature_dependent:
            if self.T_data == self.kwDefaults['T_data']:
                raise AttributeError('set -T_data- attribute to your daily temperature data')
            else:
                # set t_0T using the temperature data from concrete pouring to prestress application
                self.t_0T = self.tT(self.T_data[:self.prestress_time])
                self.t_0_cem = self.t0_cem(self.t_0T)  # set t_0_cem to temperature dependent value
        else:
            self.t_0T = 0
            self.t_0_cem = self.t0_cem(self.prestress_time)  # initial prestress time adjusted to cement type

    def set(self, default: bool=False, **kwargs) -> None:
        """sets attributes to default or to the passed kwargs
        :param default: indicate if you want to set default values of not"""
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
    def alpha(self) -> int:
        """ exponent that depends on the cement type"""
        if self.cem_type == 'S':
            return -1
        elif self.cem_type == 'N':
            return 0
        elif self.cem_type == 'R':
            return 1
        else:
            raise ValueError('not a valid cement type. try S, N or R introduced as strings')

    def alpha_n(self, n:float) -> float:
        """factors that take into account the influence of concrete's strength
        :param n: can be 0.7, 0.2, 0.5"""
        return pow(35/self.f_cm, n)

    def phiHR(self) -> float:
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

    def Bfcm(self) -> float:
        """coefficient that takes into account the concrete's strength over the
        basic creep coefficient"""
        return 16.8 / sqrt(self.f_cm)

    def Bt0(self, t0: float) -> float:
        """coefficient that takes into account the loading age over the
        basic creep coefficient
        :param t0: time prestress after concrete pouring in days. t0 can be temperature dependent"""
        return 1 / (0.1 + pow(t0, 0.2))

    def B_H(self) -> float:
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

    def Bc_t(self, t: int, t0: float) -> float:
        """coefficient describing creep development over time after loading
        :param t: concrete's age in days when creep is being calculated
        :param t0: concrete's age in days when load is applied"""
        num = t - t0
        dem = self.B_H() + num
        return pow(num / dem, 0.3)

    def t0_cem(self, t0T: float) -> float:
        """the cement type effects over the creep coefficient can be taken into account modifying the loading age
        t0 according to the next expression
        :param t0T: concrete age in days can be temperature adjusted or not"""
        to = t0T * pow(9 / (2 + pow(t0T, 1.2)) + 1, self.alpha_)
        if to >= 0.5:
            return to
        elif 0 <= to < 0.5:
            return 0.5
        else:
            raise ValueError

    def tT(self, T_data: tuple) -> float:  # open to change until data format is known
        """temperature-adjusted loading age that replaces t in the corresponding equations. Data of time and
        temperature at each time T(t) must be provided. To calculate t_0T you should sum from the first data point
        (at concrete pouring) to the point at prestress application.
         :param T_data: daily temperature data during concrete curing as numpy ndarray.
         """
        np_T_data = np.array(T_data)
        exponential_vector = np.exp(-4000/(273+np_T_data)+13.65)
        return np.sum(exponential_vector).item()

    def phi0(self, t0: float) -> float:
        """basic creep coefficient according to spanish structural code
        :param t0: concrete's age in days when load is applied"""
        return self.phi_HR * self.B_fcm * self.Bt0(t0)

    def phi_time(self, t: int, t0: float) -> float:
        """time dependent creep coefficient
            :param t: concrete's age in days when creep is being calculated
            :param t0: concrete's age in days when load is applied"""
        return self.phi0(t0) * self.Bc_t(t, t0)

    def phi_non_lin(self, t: int, t0: float) -> float:
        """time dependent non-linear creep coefficient
                :param t: concrete's age in days when creep is being calculated
                :param t0: concrete's age in days when load is applied"""
        return self.phi_time(t, t0) * exp(1.5 * (self.sigma_c / self.f_ckt - 0.45))

# SHRINKAGE METHODS

def interpolate(data: tuple, n: int):
    """
    :param data: tuple to interpolate
    :param n: number of steps between each original data point
    :return: list of interpalated data
    """
    interpolated_data = []
    i = 0
    while i < len(data)-1:
        interpolated_data.append(data[i])
        for j in range(1, n):
            t = j / n
            new_data_point = data[i] * (1 - t) + data[i+1] * (t)
            interpolated_data.append(new_data_point)
        i += 1

    return interpolated_data

if __name__ == '__main__':
    #attrs = {
    #    'fck': 40,
    #    'gc': 1.5,  # concrete safety coefficient
    #    'h0': 300,
    #    's': 'N',  # S, N, R
    #    'prestress_time': 5,
    #    'HR': 45,
    #    'T': 17,  # time-weighted average temperature the concrete will be exposed to
    #    'life_exp': 50  # life expectancy in years
    #}
    #concrete = Concrete(**attrs)

    T_data = (11.51,
        18.85,
        30.10,
        32.62,
        32.24,
        30.43,
        28.56,
        26.46,
        25.67,
        22.58,
        21.61,
        20.27,
        18.92,
        17.63,
        17.44,
        16.40,
        15.70,
        15.24,
        14.78,
        14.32,
        13.86,
        13.40,
        13.02,
        12.67,
        12.52,
        12.36,
        12.20,
        12.05,
        11.89,
        11.73)
    inter_data = interpolate(T_data, 24)
    #print(len(T_data))
    print("(")
    for n in inter_data:
        print(f"{round(n, 2)},")
    print(")")
    #print(len(inter_data))

