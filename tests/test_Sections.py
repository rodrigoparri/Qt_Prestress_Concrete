import unittest

from StructEng import Sections


class TestConcSect(unittest.TestCase):
    RectBeam_default = Sections.RectConcSect()
    Beam_fck_60 = Sections.RectConcSect(fck=60)

    def test_Bcc_returns_correct_value(self):

        result = Sections.ConcreteSection.Bcc(5, 0.2)
        self.assertTrue(0.7608 < result < 0.7609)

        result = Sections.ConcreteSection.Bcc(7, 0.25)
        self.assertTrue(0.7788 < result < 0.7789)

        result = Sections.ConcreteSection.Bcc(28, 0.38)
        self.assertTrue(result == 1)

    def test_fcm_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fcm(), 33)

    def test_fcmt_returns_correct_value(self):
        self.assertEqual(self.RectBeam_default.fcmt(5, .2),
        self.RectBeam_default.Bcc(5, .2) * self.RectBeam_default.fcm())

    def test_fctm_returns_correct_value(self):
        self.assertTrue(2.5594 < self.RectBeam_default.fctm() < 25595)

        self.assertTrue(4.354 < self.Beam_fck_60.fctm() < 4.355)


class TestRectSect(unittest.TestCase):

    def setUp(self) -> None:
        self.RectBeam_bad = Sections.RectConcSect(
            b=250,
            h=500,
            fck=60,
            N=2000
        )

    def test_mangelTensionLimit_returns_correctly(self):
        self.assertTrue(self.RectBeam_bad.magnelTensionLimit(330, 1000, 5, .2) == False)



if __name__=='__main__':
    unittest.main()
