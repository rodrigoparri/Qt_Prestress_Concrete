from StructEng.Sections.class_ConcreteSection import ConcreteSection

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
        super().__init__(**kwargs)

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

    def Qx_top(self):
        return self.b * pow(self.h, 2) * 0.5

    def Ix_top(self):
        return self.b * pow(self.h, 3) / 3

    def b_y(self, y):
        return self.b

    def A_y(self, y):
        return self.b * y

    def Q_y(self, y):
        return self.b * pow(y, 2) * 0.5

    def I_y(self, y):
        return self.b * pow(y, 3) / 3

    def ycentroid_y(self, y):
        return y / 2


if __name__ == "__main__":
    kwargs = {
        'fck': 20,
        'fyk': 400,
        'fpk': 1750,
        'Es': 200E3,
        'Ep': 200E3,
        's': 0.25,
        't': 7,
        'gc': 1.5,
        'gs': 1.15,
        'gp': 1.15,
        'As1': 900,
        'As2': 1800,
        'Ap' : 1000,
        'b' : 300,
        'h' : 800,
        'ds1' : 60,
        'ds2': 740,
        'dp' : 600,
        'N' : -1350E3,
        'M' : -710E6
    }
    kwargs2 = {
        'fck' : 35,
        'fyk' : 400,
        'fpk' : 1750,
        'Es' : 200E3,
        'Ep' : 195E3,
        's' : 0.25,
        'prestress_time' : 7,
        'gc' : 1.5,
        'gs' : 1.15,
        'gp' : 1.15,
        'As1' : 900,
        'As2' : 1800,
        'Ap' : 1000,
        'b' : 500,
        'h' : 1000,
        'ds1' : 60,
        'ds2' : 740,
        'dp' : 600,
        'N' : -1350E3,
        'M' : -310E6,
    }
    #{'b': 500, 'h': 1000, 'dp': 600, 'fck': 35, 'N': -1350E3}
    beam = RectConcSect(**kwargs2)
    #print(beam)
    print(beam.eps_0())
    print(beam.k())
    print(beam.stress_t(0))
    print(beam.stress(beam.h))