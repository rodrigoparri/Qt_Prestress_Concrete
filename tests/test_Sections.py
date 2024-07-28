import unittest
from StructEng.Sections.class_RectConcSect import RectConcSect
from StructEng.Sections.class_TConcSect import TConcSect

from scipy.integrate import quad


class TestConcSect(unittest.TestCase):
    RectBeam_default = RectConcSect()


    def test_e_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.e(), self.RectBeam_default.dp - self.RectBeam_default.ycentroid())


class TestRectSect(unittest.TestCase):
    kwargs = {
        'fck' : 20,
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
        'b' : 300,
        'h' : 800,
        'ds1' : 60,
        'ds2' : 740,
        'dp' : 600,
        'N' : -1350E3,
        'M' : -710E6
    }
    RectBeam = RectConcSect(**kwargs)
    RectBeam_default = RectConcSect()


    def test_RectConcSect_created_correctly(self):
        self.assertIsInstance(self.RectBeam, RectConcSect)
        for key, value in self.kwargs.items():
            self.assertIn(key, self.RectBeam.__dict__)
            self.assertEqual(value, self.RectBeam.__dict__[key])

    def test_set_works_correctly(self):
        current_attrs = self.RectBeam.__dict__
        self.RectBeam.set(default=True)
        self.assertEqual(self.RectBeam.__dict__, self.RectBeam_default.__dict__)

        self.RectBeam.set(self.kwargs)
        self.assertEqual(self.RectBeam.__dict__, current_attrs)

    def test_bruteArea_returns_correct_value(self):
        self.assertEqual(self.RectBeam.bruteArea(), self.kwargs['h'] * self.kwargs['b'])

    def test_xCentroid_returns_correct_value(self):
        self.assertEqual(self.RectBeam.xcentroid(), self.kwargs['b'] / 2)

    def test_yCentroid_returns_correct_value(self):
        self.assertEqual(self.RectBeam.ycentroid(), self.kwargs['h'] / 2)

    def test_Ix0_returns_correct_value(self):
        self.assertEqual(self.RectBeam.Ix0(), self.kwargs['b'] * pow(self.kwargs['h'], 3) / 12)

    def test_Ix_top_returns_correct_values(self):
        self.assertEqual(self.RectBeam.Ix_top(), self.RectBeam.Ix0() + self.RectBeam.bruteArea() \
                                                                 * pow(self.kwargs['h'] / 2, 2))

    def test_ns_is_correct(self):
        ns = self.kwargs['Es'] / self.RectBeam.Ecm
        self.assertEqual(self.RectBeam.ns, ns)

    def test_np_is_correct(self):
        np = self.kwargs['Ep'] / self.RectBeam.Ecm
        self.assertEqual(self.RectBeam.np, np)

    def test_hmgA_returns_correct_values(self):
        self.RectBeam.set(self.kwargs)
        hmgA = self.RectBeam.bruteArea() + (self.kwargs['As1'] + self.kwargs['As2']) * (self.RectBeam.ns - 1) \
        + self.kwargs['Ap'] * (self.RectBeam.np - 1)
        #print(hmgA)
        self.assertEqual(self.RectBeam.hmgSect['A'], hmgA)

    def test_hmgQ_returns_correct_values(self):
        self.RectBeam.set(self.kwargs)
        hmgQA = self.RectBeam.bruteArea() * self.kwargs['h'] / 2
        hmgQAs = (self.kwargs['As1'] * self.kwargs['ds1'] + self.kwargs['As2'] * self.kwargs['ds2']) \
        * (self.RectBeam.ns - 1)
        hmgQAp = self.kwargs['Ap'] * (self.RectBeam.np - 1) * self.kwargs['dp']
        hmgQ = hmgQA + hmgQAs + hmgQAp
        #print(hmgQ)
        self.assertEqual(self.RectBeam.hmgSect['Q'], hmgQ)

    def test_hmgI_returns_correct_values(self):
        self.RectBeam.set(self.kwargs)
        hmgIA = self.RectBeam.Ix_top()
        hmgIAs1 = self.kwargs['As1'] * (self.RectBeam.ns - 1) * pow(self.kwargs['ds1'], 2)
        hmgIAs2 = self.kwargs['As2'] * (self.RectBeam.ns - 1) * pow(self.kwargs['ds2'], 2)
        hmgIAp = self.kwargs['Ap'] * (self.RectBeam.np - 1) * pow(self.kwargs['dp'], 2)
        hmgI = hmgIA + hmgIAs1 + hmgIAs2 + hmgIAp
        #print(hmgI)
        self.assertEqual(self.RectBeam.hmgSect['I'], hmgI)

    def test_k_return_correct_value(self):
        self.RectBeam.set({'h':800, 'b':300, 'As1':900, 'As2':1800, 'Ap':1000, 'ds1':60, 'ds2':740, 'N':1350,
                           'M':710, 'Ep':200E3, 'Es':200E3})

        num = self.RectBeam.hmgSect['Q'] * self.RectBeam.N - self.RectBeam.M * self.RectBeam.hmgSect['A']
        dem = self.RectBeam.Ecm * (self.RectBeam.hmgSect['Q'] ** 2 - self.RectBeam.hmgSect['A'] * self.RectBeam.hmgSect['I'])

        self.assertEqual(self.RectBeam.crv, num / dem)
        self.RectBeam.set(self.kwargs)

    def test_eps_0_returns_correct_value(self):
        self.RectBeam.set(self.kwargs)
        num = self.RectBeam.hmgSect['Q'] * self.RectBeam.M - self.RectBeam.hmgSect['I'] * self.RectBeam.N
        dem = self.RectBeam.Ecm * (self.RectBeam.hmgSect['Q'] ** 2 - self.RectBeam.hmgSect['A'] * self.RectBeam.hmgSect['I'])
        eps = num / dem
        #print(eps)
        self.assertEqual(self.RectBeam.eps_0(), eps)

    def test_eps_y_returns_correct(self):
        self.RectBeam.set(self.kwargs)
        eps = self.RectBeam.epsilon_c0 + self.RectBeam.crv * self.RectBeam.h
        #print(eps)
        self.assertEqual(self.RectBeam.eps(self.RectBeam.h), eps)

    def test_stress_returns_correct_value(self):
        self.RectBeam.set(self.kwargs)
        stress_o = self.RectBeam.eps(0) * self.RectBeam.Ecm
        stress_h = self.RectBeam.eps(self.RectBeam.h) * self.RectBeam.Ecm
        #print(stress_o)
        #print(stress_h)

        self.assertEqual(self.RectBeam.stress(0), stress_o)
        self.assertEqual(self.RectBeam.stress(self.RectBeam.h), stress_h)

    def test_mangel_stress_limit_returns_correctly(self):
        # M0 and M1 are the moments from external loads
        M0 = 100E6
        M1 = 500E6
        # Mi Mf must be the whole moment applied to the section
        Mp = self.RectBeam.dp * self.RectBeam.N
        Mi = M0 + Mp
        Mf = M1 + Mp

        self.RectBeam.set(self.kwargs)
        self.assertFalse(self.RectBeam.magnel_stress_limit(Mi, Mf))

        self.RectBeam.set({'dp': 700, 'N': -1000, })
        #update moments
        Mp = self.RectBeam.dp * self.RectBeam.N
        Mi = M0 + Mp
        Mf = M1 + Mp
        self.assertFalse(self.RectBeam.magnel_stress_limit(Mi, Mf))

        self.RectBeam.set({
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
    })
        #print(type(self.RectBeam))
        print(self.RectBeam.stress(0))
        print(self.RectBeam.stress(self.RectBeam.h))
        #update moments
        Mp = self.RectBeam.dp * self.RectBeam.N
        Mi = M0 + Mp
        Mf = M1 + Mp
        self.assertTrue(self.RectBeam.magnel_stress_limit(Mi, Mf))


class TestTsect(unittest.TestCase):

    kwargs = {
        'fck' : 20,
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
        'b' : 300,
        'h' : 800,
        'ds1' : 60,
        'ds2' : 740,
        'dp' : 600,
        'N' : -1350E3,
        'M' : -710E6,
        't1': 80,
        't2': 80,
        't': 80
    }
    Tsect = TConcSect(**kwargs)
    Tsect_defaut = TConcSect()

    def test_TConcSect_created_correctly(self):
        self.assertIsInstance(self.Tsect, TConcSect)
        for key, value in self.kwargs.items():
            self.assertIn(key, self.Tsect.__dict__)
            self.assertEqual(value, self.Tsect.__dict__[key])

    def test_set_works_correctly(self):
        # save self.kwargs config
        current_attrs = self.Tsect.__dict__
        # set Tsect to default
        self.Tsect.set(None)
        self.maxDiff = None
        # check Tsect attributes equal default attributes
        self.assertEqual(self.Tsect.__dict__, self.Tsect_defaut.__dict__)

        #self.Tsect.set(self.kwargs)
        ## check current attributes equal self.kwargs attributes
        #self.assertEqual(self.Tsect.__dict__, current_attrs)

    def test_bruteArea_returns_correct_value(self):
        area = quad(self.Tsect.b_y, 0, self.Tsect.h)
        error = abs(area[0] - self.Tsect.bruteArea())
        self.assertTrue(error < 10, f'error: {error}')

    def test_xCentroid_returns_correct_value(self):
        self.assertEqual(self.Tsect.xcentroid(), self.Tsect.b / 2)
        self.assertEqual(self.Tsect_defaut.xcentroid(), TConcSect.kwDefaults['b'] / 2)

    def test_yCentroid_returns_correct_value(self):  #INCORRECT TEST
        self.assertEqual(self.Tsect.ycentroid(), self.Tsect.Q_xtop / self.Tsect.Ac)

    def test_Ix0_returns_correct_value(self):
        inertia = self.Tsect.I_xtop - self.Tsect.Ac * pow(self.Tsect.y_cen, 2)
        self.assertEqual(self.Tsect.Ix0(), inertia)

    def test_Qx_top_returns_correct_value(self):
        Q = quad(lambda y: y * self.Tsect.b_y(y), 0, self.Tsect.h)
        error = abs(Q[0] - self.Tsect.Qx_top())
        self.assertTrue(error < 100, f'error: {error}')

    def test_Ix_top_returns_correct_value(self):
        I = quad(lambda y: pow(y, 2) * self.Tsect.b_y(y), 0, self.Tsect.h)
        error = abs(I[0] - self.Tsect.Ix_top())
        self.assertTrue(error < 1000, f'error: {error}')

    def test_A_y_returns_correct_value(self):
        limits = (self.Tsect.t1 / 2, self.Tsect.t1 + self.Tsect.t2 / 2, self.Tsect.h - 100)
        for x in limits:
            area = quad(self.Tsect.b_y, 0, x)
            error = abs(area[0] - self.Tsect.A_y(x))
            self.assertTrue(error < 10, f'error: {error}')

        x = -100  # value want to calculate up to
        with self.assertRaises(ValueError):
            self.Tsect.A_y(x)
            x = self.Tsect.h + 100
            self.Tsect.A_y(x)

    def test_Q_y_returns_correct_value(self):
        limits = (self.Tsect.t1 / 2, self.Tsect.t1 + self.Tsect.t2 / 2, self.Tsect.h - 100)
        for x in limits:
            Q = quad(lambda y: y * self.Tsect.b_y(y), 0, x)
            error = abs(Q[0] - self.Tsect.Q_y(x))
            self.assertTrue(error < 10, f'error: {error}')

        x = -100
        with self.assertRaises(ValueError):
            self.Tsect.Q_y(x)
            x = self.Tsect.h + 100
            self.Tsect.Q_y(x)

    def test_I_y_returns_correct_value(self):
        limits = (self.Tsect.t1 / 2, self.Tsect.t1 + self.Tsect.t2 / 2, self.Tsect.h - 100)
        for x in limits:
            I = quad(lambda y: y**2 * self.Tsect.b_y(y), 0, x)
            error = abs(I[0] - self.Tsect.I_y(x))
            self.assertTrue(error < 10, f'error: {error}')

        y = -100
        with self.assertRaises(ValueError):
            self.Tsect.I_y(y)
            y = self.Tsect.h + 100
            self.Tsect.I_y(y)


if __name__=='__main__':
    unittest.main()
