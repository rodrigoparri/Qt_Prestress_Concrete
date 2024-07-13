from StructEng.class_ConcreteSection import ConcreteSection


class TConcSect(ConcreteSection):
    kwTSectDefaults = {
        't2': 200,  # FLANGE SLOPE HEIGHT
        't1': 200,  # FLANGE THICKNESS
        't': 250  # WEB THICKNESS
    }

    def __init__(self, **kwargs):
        self.t2 = kwargs.get('t2', TConcSect.kwTSectDefaults['t2'])  # SLOPE PORTION HEIGHT
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
        # top rectangle area
        A1 = self.b * self.t1
        # slope section area
        A2 = self.t2 * (self.t + self.b) / 2
        # bottom rectangle area
        A3 = self.t * (self.h - self.t1 - self.t2)
        return A1 + A2 + A3

    def xcentroid(self):
        return self.b / 2

    def ycentroid(self):
        Q1 = (self.b - self.t) * pow(self.t1, 2) / 2  # top flange static moment
        Q2 = self.t * 0.5 * (pow(self.h, 2) - pow(self.t1 + self.t2, 2))  # web static moment
        # flange slope static moment
        Q3 = self.t2 * (3 * (self.b * self.t1 + self.t * self.t1) + self.b * self.t2 + 2 * self.t2 * self.t) / 6
        return (Q1 + Q2 + Q3) / self.Ac

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
        # top rectangle inertia
        I_1 = self.b * pow(self.t1, 3) / 3
        # trapezoid inertia
        I_2 = (-2*pow(self.t1,4)*(self.b+self.t) + 6*pow(self.t1*self.t2,2)*(self.t-3*self.b) +
               4*self.t1*pow(self.t2,3)*(2*self.t -5*self.b) + pow(self.t2,4)*(3*self.t-7*self.b)) / (12*self.t2)
        # bottom rectangle inertia
        I_3 = self.t * (pow(self.h, 3) - pow(self.t1, 3)) / 3
        return I_1 + I_2 + I_3

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

#---------------- y DEPENDENT FUNCTIONS---------------------------
    def A_y(self, y):
        if y <= self.t1:
            return self.b * y
        elif self.t1 < y < self.t1 + self.t2:
            return self.b * self.t1 + ConcreteSection.A_yg(y, self.b, self.t, self.t1, self.t2) - \
                    ConcreteSection.A_yg(self.t1, self.b, self.t, self.t1, self.t2)
        else:
            return self.b * self.t1 + ConcreteSection.A_yg(self.t1 + self.t2, self.b, self.t, self.t1, self.t2) - \
                    ConcreteSection.A_yg(self.t1, self.b, self.t, self.t1, self.t2) + self.t * (y - self.t1 - self.t2)

    def Q_y(self, y):
        if y < self.t1:
            return self.b * pow(y, 2) * 0.5
        elif self.t1 < y < self.t1 + self.t2:
            # value of Q(t1) used in integration result Q(y) - Q(t1)
            Q_t1 = ConcreteSection.Q_yg(self.t1, self.b, self.t, self.t1, self.t2)
            # value of Q(y) used in integration result Q(y) - Q(t1)
            Qy = ConcreteSection.Q_yg(self.t1 + y, self.b, self.t, self.t1, self.t2)
            return  self.b * self.t1 + Qy - Q_t1
        else:
            # value of Q(t1) used in integration result Q(y) - Q(t1)
            Q_t1 = ConcreteSection.Q_yg(self.t1, self.b, self.t, self.t1, self.t2)
            # value of Q(y) used in integration result Q(y) - Q(t1)
            Qy = ConcreteSection.Q_yg(self.t1 + self.t2, self.b, self.t, self.t1, self.t2)
            return self.b * pow(self.t1, 2) * 0.5 + Q_t1 + Qy + self.t * pow(y - self.t, 2)

    def I_y(self, y):
        if 0 < y <= self.t1:
            return self.b * pow(y, 3) / 3
        elif self.t1 < y < self.t1 + self.t2:
            I_1 = self.b * pow(self.t1, 3) / 3
            I_2 = ConcreteSection.I_yg(y, self.b, self.t, self.t1, self.t2) - \
                  ConcreteSection.I_yg(self.t1, self.b, self.t, self.t1, self.t2)
            return I_1 + I_2
        else:
            I_1 = self.b * pow(self.t1, 3) / 3
            I_2 = ConcreteSection.I_yg(self.t1 + self.t2, self.b, self.t, self.t1, self.t2) - \
                  ConcreteSection.I_yg(self.t1, self.b, self.t, self.t1, self.t2)
            I_3 = self.t / 3 * (pow(y, 3) - pow(self.t1 + self.t2, 3))
            print(f"{I_1, I_2, I_3}")
            return I_1 + I_2 + I_3

    def ycentroid_y(self, y):
        return self.Q_y(y) / self.A_y(y)

if __name__ == '__main__':
    myTsect = TConcSect(b=500, h=1000, t=250, t1=150, t2=200, As2=2000)
   #print(myTsect.ycentroid())
   #print(myTsect.bruteArea())
    #print(myTsect.A_y(myTsect.t1 + myTsect.t2))
    print(myTsect.I_y(myTsect.h))


