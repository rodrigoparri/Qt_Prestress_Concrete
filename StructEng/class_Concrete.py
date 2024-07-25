from math import exp, log, sqrt
from class_Material import Material


class Concrete(Material):

    kwDefaults = {
        's': 0.25,
        'prestress_time': 7,
        'HR': 25
    }
    def __init__(self,fck, h0, **kwargs):
        self.h_0 = h0

        self.s = kwargs.get('s', self.kwDefaults['s'])
        self.prestress_time = kwargs.get('prestress_time', self.kwDefaults['prestress_time'])
        self.HR = kwargs.get('HR', self.kwDefaults['HR'])

        super().__init__(fck, **kwargs)

        self.B_cc = self.Bcc()
        self.f_ckt = self.fck_t()
        self.f_cm = self.fcm()
        self.f_cmt = self.fcm_t()
        self.f_ctm = self.fctm()
        self.f_ctmt = self.fctm_t()
        self.E_cm = self.Ecm()
        self.E_cmt = self.Ecm_t()

        self.alpha_1 = self.alpha_n(0.7)
        self.alpha_2 = self.alpha_n(0.2)
        self.alpha_3 = self.alpha_n(0.5)

        self.phi_HR = self.phiHR()

    def set(self,fck, **kwargs):
        self.__init__(fck, **kwargs)


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

    def Ecm(self):
        """average concrete elastic modulus"""
        return 22 * pow(self.f_cm * 0.1, 0.3) * 1E3

    def Ecm_t(self):
        """time-dependent average concrete elastic modulus"""
        return pow(self.f_cmt / self.f_cm, 0.3) * self.E_cm

    def alpha_n(self, n):
        """factors that take into account the influence of concrete's strength
        :param n: can be 0.7, 0.2, 0.5"""
        return pow(35/self.f_cm, n)

    def phiHR(self):
        """coefficient that takes into account the relative humidity over the
        basic creep coefficient"""
        num = 1 - self.HR * 0.01
        dem = 0.1 * pow(self.h_0, 1 / 3)

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
        return  1 / (0.1 + pow(self.prestress_time, 0.2))

    def B_H(self, h0):
        """Coefficient depending on relative humidity (%) and the theoretical
        element size (mm)"""
        a = 1.5 * (1 + pow(0.012 * self.HR, 18) * h0)
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

    def Bc_t(self, t):
        num = t - self.prestress_time
        dem = self.B_H(self.h_0) + t - self.prestress_time
        return pow(num / dem, 0.3)

    def phi_t(self, t):
        pass