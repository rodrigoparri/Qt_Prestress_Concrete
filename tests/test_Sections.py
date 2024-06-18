import unittest

from StructEng import RectConcSect, TConcSect


class TestConcSect(unittest.TestCase):
    RectBeam_default = RectConcSect()
    Beam_fck_60 = RectConcSect(fck=60)
    TBeam = TConcSect()

    def test_Bcc_returns_correct_value(self):

        result = self.RectBeam_default.Bcc()
        self.assertTrue(0.7608 < result < 0.7609)

        result = self.RectBeam_default.Bcc()
        self.assertTrue(0.7788 < result < 0.7789)

        result = self.RectBeam_default.Bcc()
        self.assertTrue(result == 1)

    def test_fcm_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fcm(), 33)

    def test_fcmt_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fcmt(),
        self.RectBeam_default.Bcc() * self.RectBeam_default.fcm())

    def test_fctm_returns_correct_value(self):
        self.assertTrue(2.5594 < self.RectBeam_default.fctm() < 25595)

        self.assertTrue(4.354 < self.Beam_fck_60.fctm() < 4.355)

    def test_fctmt_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fctmt(), self.RectBeam_default.Bcc() * self.RectBeam_default.fctmt())

    def test_fckt_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fckt(), self.RectBeam_default.Bcc() * self.RectBeam_default.fckt())

    def test_Ecmt_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.Ecmt(), pow(self.RectBeam_default.fcmt() / self.RectBeam_default.fcm(), 0.3) \
                                                       * self.RectBeam_default.Ecm)

    def test_e_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.e(), self.RectBeam_default.dp - self.RectBeam_default.ycentroid())

class TestRectSect(unittest.TestCase):
    RectBeam = RectConcSect(
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

    def test_RectConcSect_created_correctly(self):
        self.assertEqual(self.RectBeam.fck, 20)

    def test_mangelTensionLimit_returns_correctly(self):
        pass

    def test_h1_returns_correct_value(self):
        self.assertEqual(self.RectBeam.h1(), 100)

    def test_k_return_correct_value(self):
        self.assertEqual(self.RectBeam.k(), 0.378E-6)

    def test_eps_0_returns_correct_value(self):
        self.assertEqual(self.RectBeam.eps_0(), -25.4E-6)

if __name__=='__main__':
    unittest.main()
