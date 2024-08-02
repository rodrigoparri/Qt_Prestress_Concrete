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
                        11.82,
                        12.12,
                        12.43,
                        12.73,
                        13.04,
                        13.35,
                        13.65,
                        13.96,
                        14.26,
                        14.57,
                        14.87,
                        15.18,
                        15.49,
                        15.79,
                        16.1,
                        16.4,
                        16.71,
                        17.02,
                        17.32,
                        17.63,
                        17.93,
                        18.24,
                        18.54,
                        18.85,
                        19.32,
                        19.79,
                        20.26,
                        20.73,
                        21.19,
                        21.66,
                        22.13,
                        22.6,
                        23.07,
                        23.54,
                        24.01,
                        24.48,
                        24.94,
                        25.41,
                        25.88,
                        26.35,
                        26.82,
                        27.29,
                        27.76,
                        28.23,
                        28.69,
                        29.16,
                        29.63,
                        30.1,
                        30.21,
                        30.31,
                        30.42,
                        30.52,
                        30.62,
                        30.73,
                        30.84,
                        30.94,
                        31.04,
                        31.15,
                        31.26,
                        31.36,
                        31.46,
                        31.57,
                        31.68,
                        31.78,
                        31.88,
                        31.99,
                        32.09,
                        32.2,
                        32.3,
                        32.41,
                        32.51,
                        32.62,
                        32.6,
                        32.59,
                        32.57,
                        32.56,
                        32.54,
                        32.52,
                        32.51,
                        32.49,
                        32.48,
                        32.46,
                        32.45,
                        32.43,
                        32.41,
                        32.4,
                        32.38,
                        32.37,
                        32.35,
                        32.34,
                        32.32,
                        32.3,
                        32.29,
                        32.27,
                        32.26,
                        32.24,
                        32.16,
                        32.09,
                        32.01,
                        31.94,
                        31.86,
                        31.79,
                        31.71,
                        31.64,
                        31.56,
                        31.49,
                        31.41,
                        31.34,
                        31.26,
                        31.18,
                        31.11,
                        31.03,
                        30.96,
                        30.88,
                        30.81,
                        30.73,
                        30.66,
                        30.58,
                        30.51,
                        30.43,
                        30.35,
                        30.27,
                        30.2,
                        30.12,
                        30.04,
                        29.96,
                        29.88,
                        29.81,
                        29.73,
                        29.65,
                        29.57,
                        29.49,
                        29.42,
                        29.34,
                        29.26,
                        29.18,
                        29.11,
                        29.03,
                        28.95,
                        28.87,
                        28.79,
                        28.72,
                        28.64,
                        28.56,
                        28.47,
                        28.38,
                        28.3,
                        28.21,
                        28.12,
                        28.03,
                        27.95,
                        27.86,
                        27.77,
                        27.68,
                        27.6,
                        27.51,
                        27.42,
                        27.34,
                        27.25,
                        27.16,
                        27.07,
                        26.98,
                        26.9,
                        26.81,
                        26.72,
                        26.63,
                        26.55,
                        26.46,
                        26.43,
                        26.39,
                        26.36,
                        26.33,
                        26.3,
                        26.26,
                        26.23,
                        26.2,
                        26.16,
                        26.13,
                        26.1,
                        26.07,
                        26.03,
                        26.0,
                        25.97,
                        25.93,
                        25.9,
                        25.87,
                        25.83,
                        25.8,
                        25.77,
                        25.74,
                        25.7,
                        25.67,
                        25.54,
                        25.41,
                        25.28,
                        25.16,
                        25.03,
                        24.9,
                        24.77,
                        24.64,
                        24.51,
                        24.38,
                        24.25,
                        24.12,
                        24.0,
                        23.87,
                        23.74,
                        23.61,
                        23.48,
                        23.35,
                        23.22,
                        23.09,
                        22.97,
                        22.84,
                        22.71,
                        22.58,
                        22.54,
                        22.5,
                        22.46,
                        22.42,
                        22.38,
                        22.34,
                        22.3,
                        22.26,
                        22.22,
                        22.18,
                        22.14,
                        22.09,
                        22.05,
                        22.01,
                        21.97,
                        21.93,
                        21.89,
                        21.85,
                        21.81,
                        21.77,
                        21.73,
                        21.69,
                        21.65,
                        21.61,
                        21.55,
                        21.5,
                        21.44,
                        21.39,
                        21.33,
                        21.27,
                        21.22,
                        21.16,
                        21.11,
                        21.05,
                        21.0,
                        20.94,
                        20.88,
                        20.83,
                        20.77,
                        20.72,
                        20.66,
                        20.61,
                        20.55,
                        20.49,
                        20.44,
                        20.38,
                        20.33,
                        20.27,
                        20.21,
                        20.16,
                        20.1,
                        20.04,
                        19.99,
                        19.93,
                        19.88,
                        19.82,
                        19.76,
                        19.71,
                        19.65,
                        19.59,
                        19.54,
                        19.48,
                        19.43,
                        19.37,
                        19.31,
                        19.26,
                        19.2,
                        19.15,
                        19.09,
                        19.03,
                        18.98,
                        18.92,
                        18.87,
                        18.81,
                        18.76,
                        18.71,
                        18.65,
                        18.6,
                        18.54,
                        18.49,
                        18.44,
                        18.38,
                        18.33,
                        18.27,
                        18.22,
                        18.17,
                        18.11,
                        18.06,
                        18.01,
                        17.95,
                        17.9,
                        17.84,
                        17.79,
                        17.74,
                        17.68,
                        17.63,
                        17.62,
                        17.61,
                        17.61,
                        17.6,
                        17.59,
                        17.58,
                        17.57,
                        17.57,
                        17.56,
                        17.55,
                        17.54,
                        17.54,
                        17.53,
                        17.52,
                        17.51,
                        17.5,
                        17.5,
                        17.49,
                        17.48,
                        17.47,
                        17.46,
                        17.46,
                        17.45,
                        17.44,
                        17.4,
                        17.35,
                        17.31,
                        17.27,
                        17.22,
                        17.18,
                        17.14,
                        17.09,
                        17.05,
                        17.01,
                        16.96,
                        16.92,
                        16.88,
                        16.83,
                        16.79,
                        16.75,
                        16.7,
                        16.66,
                        16.62,
                        16.57,
                        16.53,
                        16.49,
                        16.44,
                        16.4,
                        16.37,
                        16.34,
                        16.31,
                        16.28,
                        16.25,
                        16.22,
                        16.2,
                        16.17,
                        16.14,
                        16.11,
                        16.08,
                        16.05,
                        16.02,
                        15.99,
                        15.96,
                        15.93,
                        15.9,
                        15.87,
                        15.85,
                        15.82,
                        15.79,
                        15.76,
                        15.73,
                        15.7,
                        15.68,
                        15.66,
                        15.64,
                        15.62,
                        15.6,
                        15.58,
                        15.57,
                        15.55,
                        15.53,
                        15.51,
                        15.49,
                        15.47,
                        15.45,
                        15.43,
                        15.41,
                        15.39,
                        15.37,
                        15.36,
                        15.34,
                        15.32,
                        15.3,
                        15.28,
                        15.26,
                        15.24,
                        15.22,
                        15.2,
                        15.18,
                        15.16,
                        15.14,
                        15.12,
                        15.11,
                        15.09,
                        15.07,
                        15.05,
                        15.03,
                        15.01,
                        14.99,
                        14.97,
                        14.95,
                        14.93,
                        14.91,
                        14.89,
                        14.88,
                        14.86,
                        14.84,
                        14.82,
                        14.8,
                        14.78,
                        14.76,
                        14.74,
                        14.72,
                        14.7,
                        14.68,
                        14.66,
                        14.65,
                        14.63,
                        14.61,
                        14.59,
                        14.57,
                        14.55,
                        14.53,
                        14.51,
                        14.49,
                        14.47,
                        14.45,
                        14.44,
                        14.42,
                        14.4,
                        14.38,
                        14.36,
                        14.34,
                        14.32,
                        14.3,
                        14.28,
                        14.26,
                        14.24,
                        14.22,
                        14.21,
                        14.19,
                        14.17,
                        14.15,
                        14.13,
                        14.11,
                        14.09,
                        14.07,
                        14.05,
                        14.03,
                        14.01,
                        13.99,
                        13.97,
                        13.96,
                        13.94,
                        13.92,
                        13.9,
                        13.88,
                        13.86,
                        13.84,
                        13.82,
                        13.8,
                        13.78,
                        13.76,
                        13.74,
                        13.73,
                        13.71,
                        13.69,
                        13.67,
                        13.65,
                        13.63,
                        13.61,
                        13.59,
                        13.57,
                        13.55,
                        13.53,
                        13.52,
                        13.5,
                        13.48,
                        13.46,
                        13.44,
                        13.42,
                        13.4,
                        13.38,
                        13.37,
                        13.35,
                        13.34,
                        13.32,
                        13.3,
                        13.29,
                        13.27,
                        13.26,
                        13.24,
                        13.23,
                        13.21,
                        13.19,
                        13.18,
                        13.16,
                        13.15,
                        13.13,
                        13.12,
                        13.1,
                        13.08,
                        13.07,
                        13.05,
                        13.04,
                        13.02,
                        13.01,
                        12.99,
                        12.98,
                        12.96,
                        12.95,
                        12.93,
                        12.92,
                        12.9,
                        12.89,
                        12.87,
                        12.86,
                        12.84,
                        12.83,
                        12.82,
                        12.8,
                        12.79,
                        12.77,
                        12.76,
                        12.74,
                        12.73,
                        12.71,
                        12.7,
                        12.68,
                        12.67,
                        12.66,
                        12.66,
                        12.65,
                        12.64,
                        12.64,
                        12.63,
                        12.63,
                        12.62,
                        12.61,
                        12.61,
                        12.6,
                        12.59,
                        12.59,
                        12.58,
                        12.58,
                        12.57,
                        12.56,
                        12.56,
                        12.55,
                        12.54,
                        12.54,
                        12.53,
                        12.53,
                        12.52,
                        12.51,
                        12.51,
                        12.5,
                        12.49,
                        12.49,
                        12.48,
                        12.47,
                        12.47,
                        12.46,
                        12.45,
                        12.45,
                        12.44,
                        12.43,
                        12.43,
                        12.42,
                        12.41,
                        12.41,
                        12.4,
                        12.39,
                        12.39,
                        12.38,
                        12.37,
                        12.37,
                        12.36,
                        12.35,
                        12.35,
                        12.34,
                        12.33,
                        12.33,
                        12.32,
                        12.31,
                        12.31,
                        12.3,
                        12.29,
                        12.29,
                        12.28,
                        12.27,
                        12.27,
                        12.26,
                        12.25,
                        12.25,
                        12.24,
                        12.23,
                        12.23,
                        12.22,
                        12.21,
                        12.21,
                        12.2,
                        12.19,
                        12.19,
                        12.18,
                        12.17,
                        12.17,
                        12.16,
                        12.16,
                        12.15,
                        12.14,
                        12.14,
                        12.13,
                        12.12,
                        12.12,
                        12.11,
                        12.11,
                        12.1,
                        12.09,
                        12.09,
                        12.08,
                        12.08,
                        12.07,
                        12.06,
                        12.06,
                        12.05,
                        12.04,
                        12.04,
                        12.03,
                        12.02,
                        12.02,
                        12.01,
                        12.0,
                        12.0,
                        11.99,
                        11.98,
                        11.98,
                        11.97,
                        11.96,
                        11.96,
                        11.95,
                        11.94,
                        11.94,
                        11.93,
                        11.92,
                        11.92,
                        11.91,
                        11.9,
                        11.9,
                        11.89,
                        11.88,
                        11.88,
                        11.87,
                        11.86,
                        11.86,
                        11.85,
                        11.84,
                        11.84,
                        11.83,
                        11.82,
                        11.82,
                        11.81,
                        11.8,
                        11.8,
                        11.79,
                        11.78,
                        11.78,
                        11.77,
                        11.76,
                        11.76,
                        11.75,
                        11.74,
                        11.74),  # time-weighted average temperature the concrete will be exposed to
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
            self.assertEqual(self.concrete.t_0_cem, t0)
        else:
            self.fail()

        # set concrete to temperature dependent
        self.concrete.set(temperature_dependent=True)
        t_0T = np.sum(np.exp(-4000/(273+np.array(self.concrete.T_data[:24*self.concrete.prestress_time]))+13.65))
        print(t_0T)
        t0 = t_0T * pow(9 / (2 + t_0T ** 1.2) + 1, self.concrete.alpha_)
        if 0 < t0 <= 0.5:
            self.assertEqual(self.concrete.t_0T, t_0T)
            print(self.concrete.t_0_cem)
            self.assertEqual(self.concrete.t_0_cem, 0.5)
        elif t0 > 0.5:
            self.assertEqual(self.concrete.t_0T, t_0T)
            print(self.concrete.t_0_cem)
            self.assertEqual(self.concrete.t_0_cem, t0)
        else:
            self.fail()

    def test_Bc_t_returns_correctly(self):
        self.concrete.set(temperature_dependent=True)
        num = self.concrete.delayed_effects_time - self.concrete.t_0_cem
        dem = self.concrete.B_H() + num
        print(num)
        print(dem)
        print(pow(num / dem, 0.3))

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
        print(type(self.concrete.phi_0))
        print(type(self.concrete.B_ct))
        print(phi_t)
        self.assertEqual(self.concrete.phi_t, phi_t)

        self.concrete.set(temperature_dependent=False)
        phi_t = self.concrete.phi_0 * self.concrete.B_ct
        self.assertEqual(self.concrete.phi_t, phi_t)

    def test_phi_non_lin_returns_correctly(self):
        self.concrete.set(sigma_c=30)
        phi_nl = self.concrete.phi_t * exp(1.5 * (self.concrete.sigma_c / self.concrete.f_ckt - 0.45))
        self.assertEqual(self.concrete.phi_nl, phi_nl)
        self.concrete.set(sigma_c=0)
