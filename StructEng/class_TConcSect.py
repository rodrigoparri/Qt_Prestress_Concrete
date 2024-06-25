from StructEng.class_ConcreteSection import ConcreteSection


class TConcSect(ConcreteSection):
    kwDefaults = {
        't1': 200,  # FLANGE THICKNESS
        't': 250  # WEB THICKNESS
    }

    def __init__(self, **kwargs):
        self.t1 = kwargs.get('t1', TConcSect.kwDefaults['t1'])  # FLANGE THICKNESS
        self.t = kwargs.get('t', TConcSect.kwDefaults['t'])  # WEB THICKNESS
        super().__init__(
            fck=kwargs.get('fck', ConcreteSection.kwDefaults['fck']),
            fyk=kwargs.get('fyk', ConcreteSection.kwDefaults['fyk']),
            fpk=kwargs.get('fpk', ConcreteSection.kwDefaults['fpk']),
            Es=kwargs.get('Es', ConcreteSection.kwDefaults['Es']),
            Ep=kwargs.get('Ep', ConcreteSection.kwDefaults['Ep']),
            s=kwargs.get('s', ConcreteSection.kwDefaults['s']),
            prestress_time=kwargs.get('prestress_time', ConcreteSection.kwDefaults['prestress_time']),
            gc=kwargs.get('gc', ConcreteSection.kwDefaults['gc']),
            gs=kwargs.get('gs', ConcreteSection.kwDefaults['gs']),
            gp=kwargs.get('gp', ConcreteSection.kwDefaults['gp']),
            As1=kwargs.get('As1', ConcreteSection.kwDefaults['As1']),
            As2=kwargs.get('As2', ConcreteSection.kwDefaults['As2']),
            Ap=kwargs.get('Ap', ConcreteSection.kwDefaults['Ap']),
            b=kwargs.get('b', ConcreteSection.kwDefaults['b']),
            h=kwargs.get('h', ConcreteSection.kwDefaults['h']),
            ds1=kwargs.get('ds1', ConcreteSection.kwDefaults['ds1']),
            ds2=kwargs.get('ds2', ConcreteSection.kwDefaults['ds2']),
            dp=kwargs.get('dp', ConcreteSection.kwDefaults['dp']),
            N=kwargs.get('N', ConcreteSection.kwDefaults['N']),
            M=kwargs.get('M', ConcreteSection.kwDefaults['M'])
        )

    def bruteArea(self):
        return (self.b - self.t) * self.t1 + self.h * self.t

    def A_y(self, y):
        pass

    def Q_y(self, y):
        pass

    def ycentroid_y(self, y):
        pass

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
