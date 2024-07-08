from StructEng.class_ConcreteSection import ConcreteSection


class TConcSect(ConcreteSection):
    kwTSectDefaults = {
        't1': 200,  # FLANGE THICKNESS
        't': 250  # WEB THICKNESS
    }

    def __init__(self, **kwargs):
        self.t1 = kwargs.get('t1', TConcSect.kwTSectDefaults['t1'])  # FLANGE THICKNESS
        self.t = kwargs.get('t', TConcSect.kwTSectDefaults['t'])  # WEB THICKNESS
        super().__init__(**kwargs)

    def __str__(self):
        str =  f"""
        -----------------------PARTICULAR PROPERTIES-----------------------------------------
        t1: flange thickness.......................................................{self.fck} mm
        t: web thickness...........................................................{self.fck} mm
        """
        return super().__str__() + str

    def set(self, kwargs):
        if kwargs != None:
            self.t1 = kwargs.get('t1', self.kwTSectDefaults['t1'])
            self.t = kwargs.get('t', self.kwTSectDefaults['t'])
        else:
            self.t1 = self.kwTSectDefaults['t1']
            self.t = self.kwTSectDefaults['t']

        super().set(kwargs)

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

    def Ix_top(self):
        top_rect = self.b * pow(self.t1, 3) / 3
        bottom_rect = self.t * (pow(self.h, 3) - pow(self.t1, 3)) / 3
        return top_rect + bottom_rect

    def A_y(self, y):
        if y < self.t1:
            return self.b * y
        else:
            return self.b * self.t1 + self.t * (y - self.t1)

    def Q_y(self, y):
        if y < self.t1:
            return self.b * pow(y,2) * 0.5
        else:
            return self.b * pow(self.t1,2) * 0.5 + self.t * pow(y - self.t, 2)

    def ycentroid_y(self, y):
        return self.Q_y(y) / self.A_y(y)

    def hmgSection(self):
        hmg = dict()

        y = self.y_cen

        hmgA = self.Ac
        hmgAc1 = self.As1 * (self.ns - 1)
        hmgAc2 = self.As2 * (self.ns - 1)
        hmgAcp = self.Ap * (self.np - 1)
        hmgArea = hmgA + hmgAc1 + hmgAc2 + hmgAcp

        hmgQA = hmgA * y
        hmgQc1 = hmgAc1 * self.ds1
        hmgQc2 = hmgAc2 * self.ds2
        hmgQcp = hmgAcp * self.dp
        hmgQ = hmgQA + hmgQc1 + hmgQc2 + hmgQcp

        hmgIA = self.Ixt
        hmgIc1 = hmgQc1 * self.ds1
        hmgIc2 = hmgQc2 * self.ds2
        hmgIcp = hmgQcp * self.dp
        hmgI = hmgIA + hmgIc1 + hmgIc2 + hmgIcp
        hmg['A'] = hmgArea
        hmg['Q'] = hmgQ
        hmg['I'] = hmgI
        return hmg

if __name__ == '__main__':
    myTsect = TConcSect(b=250, h=500, t=80, t1=80, As2=2000)
    print(myTsect.ycentroid())
    print(myTsect.bruteArea())
    print(myTsect.Ix0())
    print(myTsect.Ix_top())
    print(myTsect)

