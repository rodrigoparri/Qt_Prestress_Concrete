import unittest
from math import exp, log, sqrt
import numpy as np
from StructEng.Materials.class_Concrete import Concrete


class TestConcrete(unittest.TestCase):
    kwattrs = {
            'fck': 25,
            'gc': 1.5,  # concrete safety coefficient
            'h0': 330,
            'cem_type': 'S',  # cement type S, N, R
            'prestress_time': 5,
            'HR': 50,
            'temperature_dependent': False,
            'T_data': (11.51,
        18.85,
        30.10,
        32.62,
        32.24,
        30.43,
        28.56,
        26.46,
        25.67,
        22.58,
        21.61,
        20.27,
        18.92,
        17.63,
        17.44,
        16.40,
        15.70,
        15.24,
        14.78,
        14.32,
        13.86,
        13.40,
        13.02,
        12.67,
        12.52,
        12.36,
        12.20,
        12.05,
        11.89,
        11.73),  # time-weighted average temperature the concrete will be exposed to
            'delayed_effects_time': 70  # life expectancy in years
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
        # make sure  concrete is set to kwargs
        self.concrete.set(**self.kwattrs)
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

    def test_eps_c2_returns_correctly(self):
        self.concrete.set(fck=50)
        self.assertTrue(self.concrete.epsilon_c2 == 0.002)
        self.concrete.set(fck=60)
        eps_c2 = 2 + 0.85 * pow(self.concrete.fck - 50, 0.53)
        self.assertEqual(self.concrete.epsilon_c2, eps_c2)
        self.concrete.set(**self.kwattrs)

    def test_alpha_returns_correctly(self):
        self.concrete.set(cem_type='S')
        self.assertEqual(self.concrete.alpha_, -1)
        self.concrete.set(cem_type='N')
        self.assertEqual(self.concrete.alpha_, 0)
        self.concrete.set(cem_type='R')
        self.assertEqual(self.concrete.alpha_, 1)

    def test_alpha_n(self):
        n = (0.7, 0.2, 0.5)
        for i in n:
            self.assertEqual(self.concrete.alpha_n(i), pow(35/self.concrete.f_cm, i))

    def test_phiHR_returns_correctly(self):
        num = 1 - self.concrete.HR * 0.01
        dem = 0.1 * pow(self.concrete.h0, 1/3)
        self.concrete.set(fck=25)
        self.assertEqual(self.concrete.phi_HR, 1 + num / dem)

        self.concrete.set(fck=30)
        num = 1 - self.concrete.HR * 0.01
        dem = 0.1 * pow(self.concrete.h0, 1/3)
        self.assertEqual(self.concrete.phi_HR, (1 + num / dem * self.concrete.alpha_1) * self.concrete.alpha_2)
        self.concrete.set(**self.kwattrs)

    def test_Bfcm_returns_correctly(self):
        self.assertEqual(self.concrete.B_fcm, 16.8 / sqrt(self.concrete.f_cm))

    def test_Bt0_returns_correctly(self):
        self.assertEqual(self.concrete.B_t0, 1 / (0.1 + pow(self.concrete.t_0_cem, 0.2)))

    def test_B_H_returns_correctly(self):
        self.concrete.set(fck=25)
        a = 1.5 * (1 + pow(0.012 * self.concrete.HR, 18) * self.concrete.h0)
        Bh = a + 250
        if Bh >= 1500:
            Bh = 1500
        self.assertEqual(self.concrete.B_H(), Bh)

        self.concrete.set(fck=30)
        a = 1.5 * (1 + pow(0.012 * self.concrete.HR, 18) * self.concrete.h0)
        Bh = a + 250 * self.concrete.alpha_3
        if Bh >= 1500 * self.concrete.alpha_3:
            Bh = 1500 * self.concrete.alpha_3
        print(self.concrete.B_H())
        self.assertEqual(self.concrete.B_H(), Bh)

        self.concrete.set(**self.kwattrs)

    def test_t0_cem_returns_correctly(self):  # tT is already being tested in this test
        # set concrete to non temperature dependent
        self.concrete.set(temperature_dependent=False)
        # calculate non temperature dependent t0
        t0 = self.concrete.prestress_time * pow(9/(2+self.concrete.prestress_time ** 1.2)+1, self.concrete.alpha_)
        if 0 < t0 <= 0.5:
            self.assertEqual(self.concrete.t_0T, 0)
            self.assertEqual(self.concrete.t_0_cem, 0.5)
        elif t0 > 0.5:
            self.assertEqual(self.concrete.t_0T, 0)
            print(f'non temp dep: {t0}')
            self.assertEqual(self.concrete.t_0_cem, t0)
        else:
            self.fail()

        # set concrete to temperature dependent
        self.concrete.set(temperature_dependent=True)
        t_0T = np.sum(np.exp(-4000/(273+np.array(self.concrete.T_data[:self.concrete.prestress_time]))+13.65))
        t0 = t_0T * pow(9 / (2 + t_0T ** 1.2) + 1, self.concrete.alpha_)
        if 0 < t0 <= 0.5:
            self.assertEqual(self.concrete.t_0T, t_0T)
            print(self.concrete.t_0_cem)
            self.assertEqual(self.concrete.t_0_cem, 0.5)
        elif t0 > 0.5:
            self.assertEqual(self.concrete.t_0T, t_0T)
            print(f'non temp dep: {t0}')
            self.assertEqual(self.concrete.t_0_cem, t0)
        else:
            self.fail()

    def test_Bc_t_returns_correctly(self):
        self.concrete.set(temperature_dependent=True)
        num = self.concrete.delayed_effects_time - self.concrete.t_0_cem
        dem = self.concrete.B_H() + num

        self.assertGreater(num, 0)
        self.assertEqual(self.concrete.B_ct, pow(num / dem, 0.3))

        self.concrete.set(temperature_dependent=False)
        num = self.concrete.delayed_effects_time - self.concrete.t_0_cem
        dem = self.concrete.B_H() + num

        self.assertEqual(self.concrete.B_ct, pow(num / dem, 0.3))

    def test_phi0_returns_correctly(self):
        self.concrete.set(temperature_dependent=True)
        phi0 = self.concrete.phi_HR * self.concrete.B_fcm * self.concrete.B_t0

        self.assertEqual(self.concrete.phi_0, phi0)

        self.concrete.set(temperature_dependent=False)
        phi0 = self.concrete.phi_HR * self.concrete.B_fcm * self.concrete.B_t0
        self.assertEqual(self.concrete.phi_0, phi0)

    def test_phi_time_returns_correctly(self):
        self.concrete.set(temperature_dependent=True)
        phi_t = self.concrete.phi_0 * self.concrete.B_ct
        print(phi_t)
        self.assertEqual(self.concrete.phi_t, phi_t)

        self.concrete.set(temperature_dependent=False)
        phi_t = self.concrete.phi_0 * self.concrete.B_ct
        print(phi_t)
        self.assertEqual(self.concrete.phi_t, phi_t)

    def test_phi_non_lin_returns_correctly(self):
        self.concrete.set(sigma_c=30)
        phi_nl = self.concrete.phi_t * exp(1.5 * (self.concrete.sigma_c / self.concrete.f_ckt - 0.45))
        self.assertEqual(self.concrete.phi_nl, phi_nl)
        self.concrete.set(sigma_c=0)
