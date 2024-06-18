from class_ConcreteSection import ConcreteSection


class TConcSect(ConcreteSection):
    DEFAULT_t1 = 200
    DEFAULT_t = 250

    def __init__(self, **kwargs):
        self.t1 = kwargs.get('t1', TConcSect.DEFAULT_t1)  # FLANGE THICKNESS
        self.t = kwargs.get('t', TConcSect.DEFAULT_t)  # WEB THICKNESS
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

    def magnelTensionLimit(self, Mi: float, Mf: float):
        pass