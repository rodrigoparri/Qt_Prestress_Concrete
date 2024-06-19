from StructEng.class_ConcreteSection import ConcreteSection

class RectConcSect(ConcreteSection):
    """
        :param fck: concrete characteristic strength
        :param fyk: steel characteristic strength
        :param fpk: pre-tensioned steel characteristic strength
        :param Ecm: secant elastic modulus
        :param Es: reinforcement steel elastic modulus
        :param Ep: pre-tensioned steel elastic modulus
        :param s: cement type for time-dependent strength calculations 0.2, 0.25, 0.38
        :param prestress_time: days after concrete pouring when pre-stress is applied
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
            s=kwargs.get('s', ConcreteSection.DEFAULT_s),
            prestress_time=kwargs.get('prestress_time', ConcreteSection.DEFAULT_prestress_time),
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

    def __str__(self):
        return super().__str__()

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

        y = self.ycentroid()

        hmgA = self.bruteArea()
        hmgAc1 = self.As1 * (self.ns - 1)
        hmgAc2 = self.As2 * (self.ns - 1)
        hmgAcp = self.Ap * (self.np - 1)
        hmgArea = hmgA + hmgAc1 + hmgAc2 + hmgAcp

        hmgQA = hmgA * y
        hmgQc1 = hmgAc1 * self.ds1
        hmgQc2 = hmgAc2 * self.ds2
        hmgQcp = hmgAcp * self.dp
        hmgQ = hmgQA + hmgQc1 + hmgQc2 + hmgQcp

        hmgIA = self.Ix(y)
        hmgIc1 = hmgQc1 * self.ds1
        hmgIc2 = hmgQc2 * self.ds2
        hmgIcp = hmgQcp * self.dp
        hmgI = hmgIA + hmgIc1 + hmgIc2 + hmgIcp
        hmg['A'] = hmgArea
        hmg['Q'] = hmgQ
        hmg['I'] = hmgI
        return hmg

    def magnelTensionLimit(self, Mi: float, Mf: float) -> bool():
        Ac = self.bruteArea()
        Wx1 = self.Wx01() # top fibre
        Wx2 = self.Wx02()
        Pe = self.N * self.e()

        #Magnel inequations
        emptyTopFibre = -self.N / Ac + (Pe - Mi) / Wx1 <= self.fctm_t()
        emptyBottomFibre = -self.N / Ac + (-Pe + Mi) / Wx2 >= -0.45 * self.fck_t()
        loadedTopFibre = -self.N / Ac + (Pe - Mf) / Wx1 >= -0.45 * self.fck
        loadedBottomFibre = -self.N / Ac + (-Pe + Mf) / Wx2 <= self.fctm()

        return emptyTopFibre and emptyBottomFibre and loadedTopFibre and loadedBottomFibre


if __name__ == "__main__":
    beam = RectConcSect(
        fck=20,
        fyk=400,
        fpk=1750,
        Es=200E3,
        Ep=195E3,
        s=0.25,
        t=7,
        gc=1.5,
        gs=1.15,
        gp=1.15,
        As1=900,
        As2=1800,
        Ap=1000,
        b=300,
        h=800,
        ds1=60,
        ds2=740,
        dp=600,
        N=-1350E3,
        M=-710E6
    )

    print(beam.__dict__)