import unittest
from StructEng.class_RectConcSect import RectConcSect
from StructEng.class_TConcSect import TConcSect


class TestConcSect(unittest.TestCase):
    RectBeam_default = RectConcSect()

    def test_Bcc_returns_correct_value(self):

        result = self.RectBeam_default.Bcc()
        self.assertTrue(0.7608 < result < 0.7609)

    def test_fcm_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fcm(), 33)

    def test_fcm_t_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fcm_t(),
        self.RectBeam_default.Bcc() * self.RectBeam_default.fcm())

    def test_fctm_returns_correct_value(self):
        self.assertTrue(2.5649 < self.RectBeam_default.fctm() < 2.5650)
        self.RectBeam_default.fck = 60
        self.assertTrue(4.3547 < self.RectBeam_default.fctm() < 4.3548)
        self.RectBeam_default.set_DEFAULT()

    def test_fctm_t_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fctm_t(), self.RectBeam_default.Bcc() * self.RectBeam_default.fctm())

    def test_fck_t_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fck_t(), self.RectBeam_default.Bcc() * self.RectBeam_default.fck)

    def test_Ecm_t_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.Ecm_t(), pow(self.RectBeam_default.fcm_t() / self.RectBeam_default.fcm(), 0.3) \
                                                        * self.RectBeam_default.Ecm)

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

    def test_RectConcSect_created_correctly(self):
        self.assertIsInstance(self.RectBeam, RectConcSect)
        for key, value in self.kwargs.items():
            self.assertIn(key, self.RectBeam.__dict__)
            self.assertEqual(value, self.RectBeam.__dict__[key])

    def test_bruteArea_returns_correct_value(self):
        self.assertEqual(self.RectBeam.bruteArea(), self.kwargs['h'] * self.kwargs['b'])

    def test_xCentroid_returns_correct_value(self):
        self.assertEqual(self.RectBeam.xcentroid(), self.kwargs['b'] / 2)

    def test_yCentroid_returns_correct_value(self):
        self.assertEqual(self.RectBeam.ycentroid(), self.kwargs['h'] / 2)

    def test_Ix0_returns_correct_value(self):
        self.assertEqual(self.RectBeam.Ix0(), self.kwargs['b'] * pow(self.kwargs['h'], 3) / 12)

    def test_Ix_returns_correct_values(self):
        self.assertEqual(self.RectBeam.Ix(self.kwargs['h'] / 2), self.RectBeam.Ix0() + self.RectBeam.bruteArea() \
                                                                 * pow(self.kwargs['h'] / 2, 2))

    def test_ns_is_correct(self):
        ns = self.kwargs['Es'] / self.RectBeam.Ecm
        self.assertEqual(self.RectBeam.ns, ns)

    def test_np_is_correct(self):
        np = self.kwargs['Ep'] / self.RectBeam.Ecm
        self.assertEqual(self.RectBeam.np, np)

    def test_hmgA_returns_correct_values(self):
        hmgA = self.RectBeam.bruteArea() + (self.kwargs['As1'] + self.kwargs['As2']) * (self.RectBeam.ns - 1) \
        + self.kwargs['Ap'] * (self.RectBeam.np - 1)
        self.assertEqual(self.RectBeam.hmgSect['A'], hmgA)

    def test_hmgQ_returns_correct_values(self):
        hmgQA = self.RectBeam.bruteArea() * self.kwargs['h'] / 2
        hmgQAs = (self.kwargs['As1'] * self.kwargs['ds1'] + self.kwargs['As2'] * self.kwargs['ds2']) \
        * (self.RectBeam.ns - 1)
        hmgQAp = self.kwargs['Ap'] * (self.RectBeam.np - 1) * self.kwargs['dp']
        hmgQ = hmgQA + hmgQAs + hmgQAp
        self.assertEqual(self.RectBeam.hmgSect['Q'], hmgQ)

    def test_hmgI_returns_correct_values(self):
        hmgIA = self.RectBeam.Ix(self.kwargs['h'] / 2)
        hmgIAs1 = self.kwargs['As1'] * (self.RectBeam.ns - 1) * pow(self.kwargs['ds1'], 2)
        hmgIAs2 = self.kwargs['As2'] * (self.RectBeam.ns - 1) * pow(self.kwargs['ds2'], 2)
        hmgIAp = self.kwargs['Ap'] * (self.RectBeam.np - 1) * pow(self.kwargs['dp'], 2)
        hmgI = hmgIA + hmgIAs1 + hmgIAs2 + hmgIAp
        self.assertEqual(self.RectBeam.hmgSect['I'], hmgI)

    def test_mangelTensionLimit_returns_correctly(self):
        pass

    def test_k_return_correct_value(self):
        pass

    def test_eps_0_returns_correct_value(self):
        pass
if __name__=='__main__':
    unittest.main()
