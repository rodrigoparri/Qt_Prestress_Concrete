import unittest
from math import exp, log
from StructEng.Materials.class_Concrete import Concrete


class TestConcrete(unittest.TestCase):
    kwattrs = {
            'fck': 25,
            'gc': 1.5,  # concrete safety coefficient
            'h0': 330,
            'cem_type': 'S',  # cement type S, N, R
            'prestress_time': 5,
            'HR': 50,
            'T': 15,  # time-weighted average temperature the concrete will be exposed to
            'life_exp': 70  # life expectancy in years
    }

    concrete = Concrete(**kwattrs)
    default_concrete = Concrete()

    def test_instance_correctly_initialized(self):
        self.assertIsInstance(self.concrete, Concrete)
        self.assertIsInstance(self.default_concrete, Concrete)

    def test_set_sets_correctly(self):
        default_dict = self.default_concrete.__dict__
        # set default concrete to kwattrs
        self.default_concrete.set(**self.kwattrs)
        # check if default_concrete and concrete have the same attrs
        self.assertEqual(self.default_concrete.__dict__, self.concrete.__dict__)

        # set default concrete to Concrete defaults
        self.default_concrete.set(default=True)
        # check if default_concrete has returned to its original state
        self.assertEqual(self.default_concrete.__dict__, default_dict)

    def test_s_cem_returns_correctly(self):
        if self.concrete.cem_type == 'R':
            self.assertEqual(self.concrete.s, 0.2)
        elif self.concrete.cem_type == 'N':
            self.assertEqual(self.concrete.s, 0.25)
        elif self.concrete.cem_type == 'S':
            self.assertEqual(self.concrete.s, 0.38)
        else:
            self.assertRaises(ValueError)

    def test_Bcc_returns_correct_value(self):
        result = self.concrete.Bcc()
        Bcc = exp(self.concrete.s * (1 - pow(28/self.concrete.prestress_time, 0.5)))
        self.assertEqual(result, Bcc)

    def test_fcm_returns_correct_value(self):
        self.assertEqual(self.concrete.f_cm, self.kwattrs['fck'] + 8)
        self.concrete.set(fck=60)
        self.assertEqual(self.concrete.f_cm, 68)
        self.concrete.set(default=True)

    def test_fcm_t_returns_correct_value(self):
        self.assertEqual(self.concrete.f_cmt, self.concrete.B_cc * self.concrete.f_cm)

    def test_fctm_returns_correct_value(self):
        self.assertTrue(self.concrete.f_ctm, 0.3 * pow(self.concrete.fck, 2/3))

        self.concrete.set(fck=60)
        self.assertEqual(self.concrete.f_ctm, 2.12 * log(1 + self.concrete.f_cm * 0.1))

        self.concrete.set(default=True)

    def test_fctm_t_returns_correct_value(self):
        self.assertEqual(self.default_concrete.f_ctmt, self.default_concrete.B_cc * self.default_concrete.f_ctm)
        self.assertEqual(self.concrete.f_ctmt, self.concrete.B_cc * self.concrete.f_ctm)
        self.concrete.set(fck=50)
        self.assertEqual(self.concrete.f_ctmt, self.concrete.B_cc * self.concrete.f_ctm)
        self.concrete.set(**self.kwattrs)

    def test_fck_t_returns_correct_value(self):
        self.assertEqual(self.default_concrete.f_ckt, self.default_concrete.B_cc * self.default_concrete.fck)
        self.assertEqual(self.concrete.f_ckt, self.concrete.B_cc * self.concrete.fck)

    def test_Ecm_t_returns_correct_value(self):
        self.assertEqual(self.default_concrete.E_cmt, pow(self.default_concrete.f_cmt / self.default_concrete.fcm(), 0.3)\
                                                        * self.default_concrete.E_cm)
        self.assertEqual(self.concrete.E_cmt, pow(self.concrete.f_cmt / self.concrete.fcm(), 0.3) * self.concrete.E_cm)

